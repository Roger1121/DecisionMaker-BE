from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mcda.models import CriterionWeight, CriterionOptionWeight, AppUser, HellwigIdeal
from mcda.jwtUtil import JwtUtil

class CriteriaWeightsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None

    def get(self, request, *args, **kwargs):
        pass;

    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                {"res": "Nie znaleziono użytkownika w bazie"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(CriterionWeight.objects.filter(user_id = user_id)) != 0:
            return Response(
                {"res": "Wagi zostały już zapisane wcześniej"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        weightSum = 0
        for weight in request.data:
            weightSum += int(weight['weight'])
        weightsList = [CriterionWeight(None, user_id, int(weight['criterion']), int(weight['weight']), int(weight['weight']) / weightSum) for weight in request.data]
        CriterionWeight.objects.bulk_create(weightsList)
        group = AppUser.objects.filter(id = user_id)[0].training_group
        return Response(group, status=status.HTTP_201_CREATED)

class CriterionOptionWeightsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None

    def get(self, request, *args, **kwargs):
        pass;
    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                {"res": "Couldn't save option weights"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(CriterionOptionWeight.objects.filter(user_id = user_id)) != 0:
            return Response(
                {"res": "Wagi zostały już zapisane wcześniej"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        weightsList = [CriterionOptionWeight(None, user_id, int(weight['criterionOption']), int(weight['weight'])) for weight in request.data]
        CriterionOptionWeight.objects.bulk_create(weightsList)
        return Response("OK", status=status.HTTP_201_CREATED)

class IdealSolutionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None

    def get(self, request, *args, **kwargs):
        pass;
    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                {"res": "Couldn't save option weights"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(HellwigIdeal.objects.filter(user_id = user_id)) != 0:
            return Response(
                {"res": "Wzorzec rozwoju został już wyznaczony"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(str(request.data))
        solutionsList = [HellwigIdeal(None, user_id, int(solution['criterionOption'])) for solution in request.data]
        HellwigIdeal.objects.bulk_create(solutionsList)
        return Response("OK", status=status.HTTP_201_CREATED)