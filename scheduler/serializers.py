from rest_framework import serializers
from .models import MonthlyAssignment, Agent, Judge


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'first_name', 'last_name', 'email']


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = ['id', 'last_name', 'room_number']


class AssignmentSerializer(serializers.ModelSerializer):
    # Instead of just sending IDs (agent: 1), we send the full object (agent: {name: "Smith"...})
    # This makes the Frontend developer's life much easier.
    agent = AgentSerializer(read_only=True)
    judge = JudgeSerializer(read_only=True)

    class Meta:
        model = MonthlyAssignment
        fields = ['id', 'date', 'start_time', 'judge', 'agent', 'is_locked']