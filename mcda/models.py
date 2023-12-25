from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    description = models.CharField(max_length=2000)
    is_available = models.BooleanField()
    group = models.IntegerField()

class Criterion(models.Model):
    name = models.CharField(max_length=200)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

class Option(models.Model):
    name = models.CharField(max_length=200)

class CriterionOption(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

class AppUser(User):
    group = models.IntegerField()

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    criterion_weight = models.FloatField()
    response = models.BinaryField()

class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    rank = models.IntegerField()
