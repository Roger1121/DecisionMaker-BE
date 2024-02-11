from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from mcda.models import AppUser
from mcda.jwtUtil import JwtUtil

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        confirmPassword = request.data.get("passwordConfirmation")
        if password != confirmPassword:
            return Response("password and confirmation password don't match", status = status.HTTP_400_BAD_REQUEST)
        AppUser.objects.create_user(email, password)
        return Response("user created", status = status.HTTP_201_CREATED)

class UserScaleView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None
    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        return Response(AppUser.objects.filter(id = user_id)[0].training_group, status= status.HTTP_200_OK)