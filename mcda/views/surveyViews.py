from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mcda.models import SolvingStage, Question, QuestionResponse
from mcda.jwtUtil import JwtUtil

class SurveyApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None

    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if SolvingStage.objects.filter(user_id = user_id, stage = 3).count() < 2:
            Response(
                "Ankieta może zostać wypełniona dopiero po ukończeniu dwóch zadań.",
                status=status.HTTP_200_OK)
        return Response([
            {
                "question":response.question.id,
                "content": response.content
            } for response in QuestionResponse.objects.all()], status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response("Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        responses = [QuestionResponse(None, user_id, int(resp["question"]), resp["content"]) for resp in request.data]
        QuestionResponse.objects.bulk_create(responses)
        return Response("Dodane odpowiedzi zostały zapisane", status=status.HTTP_201_CREATED)

class SurveyAvailableApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None

    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response("Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(SolvingStage.objects.filter(user_id = user_id, stage = 3).count() == 2, status=status.HTTP_200_OK)
