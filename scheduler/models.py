from django.db import models
from django.contrib.auth.models import AbstractUser


# --- 1. THE PEOPLE ---

class Supervisor(AbstractUser):
    """
    Custom user model for the application.
    Differentiates between Admins (can edit) and Viewers (read-only).
    """

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        VIEWER = 'VIEWER', 'Viewer'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)

    def __str__(self):
        return f"{self.username} ({self.role})"

## Creates the different types of users that we designed the admin who does the work and the agents who are viewing the schedule so they know when to go to Court (why is this its own class and not attributes of the user classes themselves?)

class Judge(models.Model):
    last_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=50, help_text="The courtroom this judge 'owns'.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Judge {self.last_name} ({self.room_number})"

## Creates the Judges for the application....it also determines if they are active and need to be scheduled for and where they reside in the Courthouse

class Agent(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # Logic: If specialized, they are handled in Pass 1 of the algorithm
    is_specialized = models.BooleanField(default=False)

    # Logic: The hard constraint - agent CANNOT work on this day
    recurring_report_day = models.IntegerField(
        choices=DayOfWeek.choices,
        null=True,
        blank=True,
        help_text="Day of the week the agent is unavailable due to reporting duties."
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


# --- 2. THE PATTERNS (Logic Engine) ---

## Creates the agents with all of their constraints and attributes so the app can accurately schedule them


class RecurringCourtSlot(models.Model):
    """
    Defines the standard weekly schedule.
    Example: Judge Smith sits every Tuesday at 9:00 AM.
    """

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'

    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    required_staff_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.judge.last_name} - {self.get_day_of_week_display()} @ {self.start_time}"


## creates the actual slots that need to be filled by agents each week....(why is this not done as attribute in the Judge class?)

class SpecialtyAssignment(models.Model):
    """
    Maps a Specialized Agent to a specific Judge.
    """

    class Type(models.TextChoices):
        HYBRID = 'HYBRID', 'Hybrid (Available for others)'
        EXCLUSIVE = 'EXCLUSIVE', 'Exclusive (Removed from general pool)'

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)
    assignment_type = models.CharField(max_length=20, choices=Type.choices, default=Type.HYBRID)

    def __str__(self):
        return f"{self.agent.last_name} -> {self.judge.last_name} ({self.assignment_type})"

## Creates the requirements of the specialized agents (again why is this not an attribute of the agent class?)

# --- 3. THE OPERATIONS (Transactions) ---

class MonthlyAssignment(models.Model):
    """
    The actual generated schedule for a specific date.
    """
    date = models.DateField()
    start_time = models.TimeField()
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    # If the algorithm generated it, this is True. If Boss changed it, this is False/Locked.
    is_generated = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date}: {self.agent.last_name} w/ {self.judge.last_name}"

##not sure i understand this one explain it to me line by line please


class TimeOffRequest(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.agent.last_name} OFF on {self.date}"

    ## this is a hard check to make sure agents are not scheduled when they are off duty