from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mcda.models import Question

class QuestionApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        return Response([
            {
                "id": question.id,
                "content": question.content
            } for question in Question.objects.all()], status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        Question.objects.create(content = request.data['content'])
        return Response("Pomyślnie dodano pytanie do bazy", status=status.HTTP_201_CREATED)

class QuestionDetailsApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return None

    def delete(self, request, question_id, *args, **kwargs):
        question_instance = self.get_object(question_id)
        if not question_instance:
            return Response(
                "Pytanie o podanym id nie istnieje",
                status=status.HTTP_400_BAD_REQUEST,
            )
        question_instance.delete()
        return Response("Pytanie zostało usunięte", status=status.HTTP_200_OK)