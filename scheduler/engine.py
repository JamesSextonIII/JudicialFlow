import calendar
from datetime import date
from .models import Agent, Judge, RecurringCourtSlot, MonthlyAssignment, SpecialtyAssignment, TimeOffRequest


class ScheduleEngine:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        # Calculate number of days (e.g., 28, 30, 31)
        self.num_days = calendar.monthrange(year, month)[1]

        # This will hold our "Block List"
        self.block_matrix = {}

    def run(self):
        """
        The Master Function. Executing this generates the schedule.
        """
        print(f"⚙️ Running Scheduler for {self.month}/{self.year}...")

        # Step 1: Clean Slate
        MonthlyAssignment.objects.filter(
            date__year=self.year,
            date__month=self.month,
            is_locked=False
        ).delete()

        # Step 2: Build the 'No-Go' List
        self._build_block_matrix()

        # Step 3: Run Pass 1
        self._run_pass_1_specialists()

        # Step 4: Run Pass 2 (Coming soon)
        self._run_pass_2_general_pool()

        print("✅ Scheduling Complete.")

    def _build_block_matrix(self):
        """
        Pass 0: The Blocker Layer.
        Identifies Hard Constraints (Time Off & Report Days).
        """
        for day in range(1, self.num_days + 1):
            current_date = date(self.year, self.month, day)
            day_of_week = current_date.weekday()

            self.block_matrix[current_date] = []

            # Check 1: Time Off
            time_off_qs = TimeOffRequest.objects.filter(date=current_date)
            for req in time_off_qs:
                self.block_matrix[current_date].append(req.agent.id)

            # Check 2: Report Days
            active_agents = Agent.objects.filter(is_active=True)
            for agent in active_agents:
                if agent.recurring_report_day == day_of_week:
                    self.block_matrix[current_date].append(agent.id)

    def _run_pass_1_specialists(self):
        """
        Pass 1: The Specialist Layer.
        Assigns agents who have a specific link to a Judge.
        """
        for day in range(1, self.num_days + 1):
            current_date = date(self.year, self.month, day)
            day_of_week = current_date.weekday()

            # 1. Find slots today
            todays_slots = RecurringCourtSlot.objects.filter(day_of_week=day_of_week)

            for slot in todays_slots:
                # 2. Check for Specialist
                specialty_link = SpecialtyAssignment.objects.filter(judge=slot.judge).first()

                if specialty_link:
                    agent = specialty_link.agent

                    # 3. Conflict Check
                    if agent.id in self.block_matrix[current_date]:
                        print(f"   ⚠️ Conflict: Specialist {agent} is blocked on {current_date}. Skipping.")
                        continue

                        # 4. Create Assignment
                    MonthlyAssignment.objects.create(
                        date=current_date,
                        start_time=slot.start_time,
                        judge=slot.judge,
                        agent=agent,
                        is_generated=True
                    )

                    # 5. Mark as Busy
                    self.block_matrix[current_date].append(agent.id)

    def _run_pass_2_general_pool(self):
        """
        Pass 2: The General Pool.
        Fills any remaining empty slots with available agents.
        """
        import random

        for day in range(1, self.num_days + 1):
            current_date = date(self.year, self.month, day)
            day_of_week = current_date.weekday()

            # 1. Find all slots for today
            todays_slots = RecurringCourtSlot.objects.filter(day_of_week=day_of_week)

            for slot in todays_slots:
                # 2. Check if already filled (by Pass 1 or Manual Lock)
                if MonthlyAssignment.objects.filter(date=current_date, judge=slot.judge).exists():
                    continue

                    # 3. Find Candidates
                # Start with ALL active agents
                candidates = []
                all_agents = Agent.objects.filter(is_active=True)

                for agent in all_agents:
                    # Filter out anyone in the "Block Matrix" (Vacation, Report Day, or Already Working)
                    if agent.id not in self.block_matrix[current_date]:
                        candidates.append(agent)

                # 4. Pick a Winner
                if candidates:
                    # For V1, we pick randomly. In V2, we will pick based on "Fairness Score"
                    chosen_agent = random.choice(candidates)

                    MonthlyAssignment.objects.create(
                        date=current_date,
                        start_time=slot.start_time,
                        judge=slot.judge,
                        agent=chosen_agent,
                        is_generated=True
                    )

                    # 5. Mark as Busy so they aren't picked again today
                    self.block_matrix[current_date].append(chosen_agent.id)
                else:
                    print(f"   CRITICAL: No agents available for Judge {slot.judge.last_name} on {current_date}")