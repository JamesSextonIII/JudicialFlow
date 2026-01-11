from django.core.management.base import BaseCommand
from scheduler.models import Agent, Judge, RecurringCourtSlot, SpecialtyAssignment
import random


class Command(BaseCommand):
    help = 'Seeds the database with realistic mock data for testing.'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Starting Database Seed...")

        # 1. CLEAN SLATE: Delete old data to avoid duplicates
        # We delete in specific order to respect Foreign Keys
        SpecialtyAssignment.objects.all().delete()
        RecurringCourtSlot.objects.all().delete()
        Agent.objects.all().delete()
        Judge.objects.all().delete()

        # 2. CREATE JUDGES (The Demand)
        judge_names = ["Smith", "Jones", "Garcia", "Johnson", "Williams"]
        judges = []
        for name in judge_names:
            judge = Judge.objects.create(
                last_name=name,
                room_number=f"Room {random.randint(100, 500)}"
            )
            judges.append(judge)
            self.stdout.write(f"   Created Judge {name}")

        # 3. CREATE AGENTS (The Supply)
        # We create 10 agents
        first_names = ["James", "Sarah", "Mike", "Emily", "Robert", "Jessica", "David", "Ashley", "John", "Amanda"]
        agents = []
        for i, first in enumerate(first_names):
            # Make the first 2 agents "Specialized"
            is_special = i < 2

            # Make every 3rd agent have a Report Day on Tuesday (1)
            report_day = 1 if i % 3 == 0 else None

            agent = Agent.objects.create(
                first_name=first,
                last_name=f"Agent_{i + 1}",
                email=f"{first.lower()}@example.com",
                is_specialized=is_special,
                recurring_report_day=report_day
            )
            agents.append(agent)

        self.stdout.write(f"   Created {len(agents)} Agents")

        # 4. CREATE PATTERNS (Recurring Slots)
        # Give every Judge 3 recurring slots per week
        days = [0, 1, 2, 3, 4]  # Mon-Fri
        times = ["09:00", "13:30", "10:00"]

        slot_count = 0
        for judge in judges:
            # Pick 3 random days for this judge
            judge_days = random.sample(days, 3)
            for day in judge_days:
                RecurringCourtSlot.objects.create(
                    judge=judge,
                    day_of_week=day,
                    start_time=random.choice(times),
                    required_staff_count=1
                )
                slot_count += 1

        self.stdout.write(f"   Created {slot_count} Recurring Slots")

        # 5. ASSIGN SPECIALTIES
        # Link the first Specialized Agent to the first Judge (Hybrid)
        SpecialtyAssignment.objects.create(
            agent=agents[0],
            judge=judges[0],
            assignment_type='HYBRID'
        )
        self.stdout.write(f"   Created Specialty Assignment for {agents[0]}")

        self.stdout.write(self.style.SUCCESS('✅ Database successfully seeded!'))