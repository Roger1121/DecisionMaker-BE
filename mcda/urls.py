from django.urls import path
from mcda import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path("token", TokenObtainPairView.as_view()),
    path("register", views.UserRegisterView.as_view()),
    path("user/scale", views.UserScaleView.as_view()),
    path("user/group", views.UserGroupView.as_view()),
    path("user/privileges", views.UserPrivilegesView.as_view()),
    path("problem", views.ProblemListApiView.as_view()),
    path("problem/available", views.AvailableProblemListApiView.as_view()),
    path("problem/<problem_id>", views.ProblemDetailApiView.as_view()),
    path("criterion", views.CriterionListApiView.as_view()),
    path("criterion/weights", views.CriteriaWeightsApiView.as_view()),
    path("criterion/comparison", views.CriteriaComparisonApiView.as_view()),
    path("criterion/matrix", views.CriterionMatrixApiView.as_view()),
    path("criterion/<criterion_id>", views.CriterionDetailApiView.as_view()),
    path("option", views.OptionListApiView.as_view()),
    path("option/<option_id>", views.OptionDetailApiView.as_view()),
    path("crit-option", views.CriterionOptionListApiView.as_view()),
    path("crit-option/weights", views.CriterionOptionWeightsApiView.as_view()),
    path("crit-option/comparison", views.OptionComparisonApiView.as_view()),
    path("crit-option/martices", views.OptionMatrixApiView.as_view()),
    path("crit-option/<crit_option_id>", views.CriterionOptionDetailApiView.as_view()),
    path("solutions", views.IdealSolutionApiView.as_view()),
    path("solutions/hellwig", views.HellwigResultApiView.as_view()),
    path("solutions/stage", views.SolvingStageApiView.as_view()),
    path("survey/available", views.SurveyAvailableApiView.as_view()),
    path("survey", views.SurveyApiView.as_view()),
    path("question", views.QuestionApiView.as_view()),
    path("question/<question_id>", views.QuestionDetailsApiView.as_view()),
    path("password/recovery/request", views.UserPasswordRecoveryRequestView.as_view()),
    path("password/reset", views.UserPasswordResetView.as_view()),
]

