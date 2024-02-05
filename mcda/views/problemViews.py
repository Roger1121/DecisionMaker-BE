from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mcda.models import Problem
from mcda.serializers import ProblemSerializer
from mcda.permissions import ReadOnly


class ProblemListApiView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUser|ReadOnly]
    def get(self, request, *args, **kwargs):
        problemList = Problem.objects
        serializer = ProblemSerializer(problemList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "id": request.data.get("id"),
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "is_available": request.data.get("is_available"),
            "group": request.data.get("group"),
        }
        serializer = ProblemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProblemDetailApiView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUser|ReadOnly]
    def get_object(self, problem_id):
        try:
            return Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return None

    def get(self, request, problem_id, *args, **kwargs):
        problem_instance = self.get_object(problem_id)
        if not problem_instance:
            return Response(
                {"res": "Problem with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProblemSerializer(problem_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, problem_id, *args, **kwargs):
        problem_instance = self.get_object(problem_id)
        if not problem_instance:
            return Response(
                {"res": "Problem with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "id": request.data.get("id"),
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "is_available": request.data.get("is_available"),
            "group": request.data.get("group"),
        }
        serializer = ProblemSerializer(instance=problem_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, problem_id, *args, **kwargs):
        problem_instance = self.get_object(problem_id)
        if not problem_instance:
            return Response(
                {"res": "Problem with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_instance.delete()
        return Response({"res": "Problem deleted!"}, status=status.HTTP_200_OK)