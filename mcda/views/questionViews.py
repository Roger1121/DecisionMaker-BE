from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mcda.models import Question, Answer
from mcda.permissions import ReadOnly

class QuestionApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    def get(self, request, *args, **kwargs):
        return Response([
            {
                "id": question.id,
                "type": question.type,
                "content": question.content
            } for question in Question.objects.all()], status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        question = Question.objects.create(content = request.data['content'], type = request.data['type'])
        return Response(question.id, status=status.HTTP_201_CREATED)

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

class AnswerApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    def get(self, request, *args, **kwargs):
        return Response([
            {
                "id": answer.id,
                "question": answer.question.id,
                "name": answer.name
            } for answer in Answer.objects.all()], status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            answers = [Answer(None, answer.get('question'), answer.get('name')) for answer in request.data]
            Answer.objects.bulk_create(answers)
        else:
            Answer.objects.create(name = request.data['name'])
        return Response("Pomyślnie dodano odpowiedzi", status=status.HTTP_201_CREATED)