from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MonthlyAssignment
from .serializers import AssignmentSerializer
from .engine import ScheduleEngine
from django.shortcuts import render
from django.http import JsonResponse
from .models import Agent


@api_view(['GET'])
def get_schedule(request):
    """
    Returns the schedule for a specific month/year.
    Example: /api/schedule/?year=2026&month=2
    """
    year = int(request.query_params.get('year', 2026))
    month = int(request.query_params.get('month', 2))

    # 1. Grab the data from the database
    assignments = MonthlyAssignment.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date', 'start_time')

    # 2. Translate it to JSON
    serializer = AssignmentSerializer(assignments, many=True)

    # 3. Send it back
    return Response(serializer.data)


@api_view(['POST'])
def generate_schedule(request):
    """
    Triggers the Logic Engine to build a schedule.
    """
    year = int(request.data.get('year', 2026))
    month = int(request.data.get('month', 2))

    engine = ScheduleEngine(year, month)
    engine.run()

    return Response({"status": "success", "message": f"Schedule generated for {month}/{year}"})

def dashboard_view(request):
    return render(request, 'scheduler/dashboard.html')

def get_report_days(request):
    """
    Returns a list of agents grouped by their recurring report day.
    Used to populate the footer of the dashboard dynamically.
    """
    # Map the integer database value (0-4) to the string Day Name
    day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}

    # Create empty buckets for each day
    roster = {day: [] for day in day_map.values()}

    # Fetch all agents and sort them into buckets
    agents = Agent.objects.all().order_by('last_name')
    for agent in agents:
        if agent.recurring_report_day is not None and agent.recurring_report_day in day_map:
            day_name = day_map[agent.recurring_report_day]
            roster[day_name].append(agent.last_name)

    return JsonResponse(roster)