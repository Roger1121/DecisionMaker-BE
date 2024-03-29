from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class Problem(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    is_available = models.BooleanField()
    group = models.IntegerField()

class Criterion(models.Model):
    name = models.CharField(max_length=200)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)

class Option(models.Model):
    name = models.CharField(max_length=200)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

class CriterionOption(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)


class AppUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    training_group = models.IntegerField()
    scale_type = models.IntegerField()
    reset_token = models.CharField(max_length=40, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CriterionWeight(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    criterion_weight = models.FloatField()
    criterion_weight_normalized = models.FloatField()
    def __str__(self):
        return str(self.__dict__)

class CriterionOptionWeight(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    criterion_option = models.ForeignKey(CriterionOption, on_delete=models.CASCADE)
    numeric_value = models.FloatField()

class HellwigIdeal(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    criterion_option = models.ForeignKey(CriterionOption, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.__dict__)

class Rank(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    rank = models.FloatField()
    def __str__(self):
        return str(self.__dict__)

class SolvingStage(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    stage = models.IntegerField(default = 0)

class CriteriaComparison(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    criterion_a = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name='criterion_a_comparison')
    criterion_b = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name='criterion_b_comparison')
    value = models.IntegerField()
    def __str__(self):
        return f"criterionA: {self.criterion_a.id}, criterionB: {self.criterion_b.id}, value: {self.value}"

class OptionComparison(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    option_a = models.ForeignKey(CriterionOption, on_delete=models.CASCADE, related_name='option_a_comparison')
    option_b = models.ForeignKey(CriterionOption, on_delete=models.CASCADE, related_name='option_b_comparison')
    value = models.IntegerField()

class Question(models.Model):
    content = models.CharField(max_length=200)
    type = models.CharField(max_length=10)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class QuestionResponse(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)