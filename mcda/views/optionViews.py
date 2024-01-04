from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mcda.models import Option
from mcda.serializers import OptionSerializer


class OptionListApiView(APIView):
    def get(self, request, *args, **kwargs):
        optionList = Option.objects
        serializer = OptionSerializer(optionList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "id": request.data.get("id"),
            "name": request.data.get("name")
        }
        serializer = OptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OptionDetailApiView(APIView):
    def get_object(self, option_id):
        try:
            return Option.objects.get(id=option_id)
        except Option.DoesNotExist:
            return None

    def get(self, request, option_id, *args, **kwargs):
        option_instance = self.get_object(option_id)
        if not option_instance:
            return Response(
                {"res": "Option with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OptionSerializer(option_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, option_id, *args, **kwargs):
        option_instance = self.get_object(option_id)
        if not option_instance:
            return Response(
                {"res": "Option with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "id": request.data.get("id"),
            "name": request.data.get("name")
        }
        serializer = OptionSerializer(instance=option_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, option_id, *args, **kwargs):
        option_instance = self.get_object(option_id)
        if not option_instance:
            return Response(
                {"res": "Option with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        option_instance.delete()
        return Response({"res": "Option deleted!"}, status=status.HTTP_200_OK)