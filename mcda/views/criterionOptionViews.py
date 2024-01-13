from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mcda.models import CriterionOption
from mcda.serializers import CriterionOptionSerializer


class CriterionOptionListApiView(APIView):
    def get(self, request, *args, **kwargs):
        option_id = request.query_params.get('option_id')
        if option_id:
            criterionOptionList = CriterionOption.objects.filter(option__id=option_id)
        else:
            criterionOptionList = CriterionOption.objects
        serializer = CriterionOptionSerializer(criterionOptionList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if is_many:
            serializer = CriterionOptionSerializer(data=request.data, many=True)
        else:
            serializer = CriterionOptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CriterionOptionDetailApiView(APIView):
    def get_object(self, criterion_option_id):
        try:
            return CriterionOption.objects.get(id=criterion_option_id)
        except CriterionOption.DoesNotExist:
            return None

    def get(self, request, criterion_option_id, *args, **kwargs):
        criterion_option_instance = self.get_object(criterion_option_id)
        if not criterion_option_instance:
            return Response(
                {"res": "CriterionOption with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CriterionOptionSerializer(criterion_option_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, criterion_option_id, *args, **kwargs):
        criterion_option_instance = self.get_object(criterion_option_id)
        if not criterion_option_instance:
            return Response(
                {"res": "CriterionOption with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        criterion_option_instance.delete()
        return Response({"res": "CriterionOption deleted!"}, status=status.HTTP_200_OK)