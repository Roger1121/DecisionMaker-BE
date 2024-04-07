from rest_framework import serializers
from .models import Problem, Criterion, Option, CriterionOption

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id",
            "name",
            "description",
            "description_preview",
            "is_available",
            "group"
        ]

class CriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterion
        fields = [
            "id",
            "name",
            "problem",
            "type"
        ]

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = [
            "id",
            "name",
            "problem"
        ]

class CriterionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriterionOption
        fields = [
            "id",
            "option",
            "criterion",
            "value"
        ]
