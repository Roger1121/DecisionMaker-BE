from django.urls import path
from mcda import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("register", views.UserRegisterView.as_view()),
    path("problem", views.ProblemListApiView.as_view()),
    path("problem/<problem_id>", views.ProblemDetailApiView.as_view()),
    path("criterion", views.CriterionListApiView.as_view()),
    path("criterion/<criterion_id>", views.CriterionDetailApiView.as_view()),
    path("option", views.OptionListApiView.as_view()),
    path("option/<option_id>", views.OptionDetailApiView.as_view()),
    path("crit-option", views.CriterionOptionListApiView.as_view()),
    path("crit-option/<crit_option_id>", views.CriterionOptionDetailApiView.as_view()),
]
