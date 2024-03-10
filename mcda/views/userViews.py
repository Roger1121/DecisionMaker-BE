from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
import uuid

from mcda.models import AppUser
from mcda.jwtUtil import JwtUtil

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        confirmPassword = request.data.get("passwordConfirmation")
        scaleType = request.data.get("scaleType")
        if password != confirmPassword:
            return Response("password and confirmation password don't match", status = status.HTTP_400_BAD_REQUEST)
        AppUser.objects.create_user(email, password, scaleType)
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
        return Response(AppUser.objects.filter(id = user_id)[0].scale_type, status= status.HTTP_200_OK)

class UserGroupView(APIView):
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

class UserPrivilegesView(APIView):

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None
    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response("NOT_LOGGED_IN", status=status.HTTP_200_OK)
        user = AppUser.objects.filter(id = user_id)[0]
        if user.is_staff:
            return Response("ADMIN", status=status.HTTP_200_OK)
        return Response("USER", status= status.HTTP_200_OK)

class UserPasswordRecoveryRequestView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        user = AppUser.objects.filter(email = email).first()
        token = user.reset_token
        if token is None or token == "":
            token = uuid.uuid4()
            user.reset_token = token
            print(token)
            user.save()
        reset_link = "localhost:4200/password/reset/"+str(token)
        send_mail("Reset hasła",
                  "Drogi użytkowniku,\n otrzymalismy twoją prośbę o zresetowanie hasła. Aby to zrobić kliknij w poniższy link, a następnie wprowadź nowe hasło.\n" + reset_link + "\nPozdrawiamy\nZespół DecisionMaker.",
                  "decisionmakerpb@gmail.com",
                  [email],
                  fail_silently=False)
        return Response("Na podany adres email wysłana została wiadomość z linkiem do resetu hasła.", status = status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        #password reset logic
        return Response("Hasło zostało pomyślnie zresetowane.", status = status.HTTP_200_OK)