from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mcda.models import AppUser

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        confirmPassword = request.data.get("passwordConfirm")
        if password != confirmPassword:
            return Response("password and confirmation password don't match", status = status.HTTP_400_BAD_REQUEST)
        AppUser.objects.create_user(email, password)
        return Response("user created", status = status.HTTP_201_CREATED)