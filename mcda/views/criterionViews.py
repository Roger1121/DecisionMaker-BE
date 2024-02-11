from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mcda.models import Criterion
from mcda.serializers import CriterionSerializer
from mcda.permissions import ReadOnly


class CriterionListApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]

    def get(self, request, *args, **kwargs):
        problem_id = request.query_params.get('problem_id')
        if problem_id:
            criteriaList = Criterion.objects.filter(problem__id=problem_id)
        else:
            criteriaList = Criterion.objects
        serializer = CriterionSerializer(criteriaList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if is_many:
            serializer = CriterionSerializer(data=request.data, many=True)
        else:
            serializer = CriterionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CriterionDetailApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]

    def get_object(self, criterion_id):
        try:
            return Criterion.objects.get(id=criterion_id)
        except Criterion.DoesNotExist:
            return None

    def get(self, request, criterion_id, *args, **kwargs):
        criterion_instance = self.get_object(criterion_id)
        if not criterion_instance:
            return Response(
                {"res": "Criterion with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CriterionSerializer(criterion_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, criterion_id, *args, **kwargs):
        criterion_instance = self.get_object(criterion_id)
        if not criterion_instance:
            return Response(
                {"res": "Criterion with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "id": request.data.get("id"),
            "name": request.data.get("name"),
            "problem_id": request.data.get("problem_id"),
            "type": request.data.get("type")
        }
        serializer = CriterionSerializer(instance=criterion_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, criterion_id, *args, **kwargs):
        criterion_instance = self.get_object(criterion_id)
        if not criterion_instance:
            return Response(
                {"res": "Criterion with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        criterion_instance.delete()
        return Response({"res": "Criterion deleted!"}, status=status.HTTP_200_OK)

