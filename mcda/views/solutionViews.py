from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import numpy as np

from mcda.models import CriterionWeight, CriterionOptionWeight, AppUser, HellwigIdeal, Rank, Option, SolvingStage, \
    Criterion, CriterionOption
from mcda.jwtUtil import JwtUtil
from lib.MCDA import MCDA
from lib.DistanceMetrics import Distance


class CriteriaWeightsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            return request.query_params.get('user_id')
        except:
            return None

    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                "Nie podano id problemu",
                status=status.HTTP_400_BAD_REQUEST,
            )
        weights = CriterionWeight.objects.filter(user_id=user_id, criterion__problem=problem_id)
        weights = [{"criterion": w.criterion.id, "weight": w.criterion_weight} for w in weights]
        return Response(weights, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(CriterionWeight.objects.filter(user_id=user_id)) != 0:
            return Response(
                "Wagi zostały już zapisane wcześniej",
                status=status.HTTP_400_BAD_REQUEST,
            )
        weightSum = 0
        for weight in request.data:
            weightSum += int(weight['weight'])
        weightsList = [CriterionWeight(None, user_id, int(weight['criterion']), int(weight['weight']),
                                       int(weight['weight']) / weightSum) for weight in request.data]
        CriterionWeight.objects.bulk_create(weightsList)
        problem_id = Criterion.objects.filter(id=weightsList[0].criterion.id).first().problem.id
        SolvingStage(None, user_id, problem_id, 1).save()
        return Response("Wagi kryteriów zostały pomyślnie zapisane", status=status.HTTP_201_CREATED)


class CriterionOptionWeightsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            return request.query_params.get('user_id')
        except:
            return None

    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                "Nie podano id problemu",
                status=status.HTTP_400_BAD_REQUEST,
            )
        weights = CriterionOptionWeight.objects.filter(user_id=user_id, criterion_option__criterion__problem=problem_id)
        weights = [{"criterionOption": w.criterion_option.id, "weight": w.numeric_value} for w in weights]
        return Response(weights, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(CriterionOptionWeight.objects.filter(user_id=user_id)) != 0:
            return Response(
                "Wagi zostały już zapisane wcześniej",
                status=status.HTTP_400_BAD_REQUEST,
            )
        weightsList = [CriterionOptionWeight(None, user_id, int(weight['criterionOption']), int(weight['weight'])) for
                       weight in request.data]
        CriterionOptionWeight.objects.bulk_create(weightsList)
        problem_id = CriterionOption.objects.filter(id=weightsList[0].criterion_option.id).first().criterion.problem.id
        SolvingStage.objects.filter(user_id=user_id, problem_id=problem_id).update(stage=2)
        return Response("Pomyślnie zapisano wagi opcji", status=status.HTTP_201_CREATED)


class IdealSolutionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            return request.query_params.get('user_id')
        except:
            return None

    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                "Nie podano id problemu",
                status=status.HTTP_400_BAD_REQUEST,
            )
        ideals = [ideal.criterion_option.id for ideal in
                  HellwigIdeal.objects.filter(user_id=user_id, criterion_option__option__problem_id=problem_id)]
        return Response(ideals, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(HellwigIdeal.objects.filter(user_id=user_id)) != 0:
            return Response(
                "Wzorzec rozwoju został już wyznaczony",
                status=status.HTTP_400_BAD_REQUEST,
            )
        solutionsList = [HellwigIdeal(None, user_id, int(solution['criterionOption'])) for solution in request.data]
        HellwigIdeal.objects.bulk_create(solutionsList)
        problem_id = CriterionOption.objects.filter(
            id=solutionsList[0].criterion_option.id).first().criterion.problem.id
        SolvingStage.objects.filter(user_id=user_id, problem_id=problem_id).update(stage=3)
        return Response("Pomyślnie zapisano wzorzec rozwoju", status=status.HTTP_201_CREATED)


class HellwigResultApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            return request.query_params.get('user_id')
        except:
            return None

    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(HellwigIdeal.objects.filter(user_id=user_id)) == 0 or len(
                CriterionWeight.objects.filter(user_id=user_id)) == 0 or len(
            CriterionOptionWeight.objects.filter(user_id=user_id)) == 0:
            return Response(
                "Nie ukończono analizy problemu. Nie można pobrać wyników",
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                "Nie podano id problemu.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        options = [option.id for option in Option.objects.filter(problem_id=problem_id).order_by('id')]
        if len(Rank.objects.filter(user_id=user_id, option__in=options)) > 0:
            ranks = [
                {
                    "option": rank.option.id,
                    "synth_var": rank.rank
                }
                for rank in Rank.objects.filter(user_id=user_id, option__in=options).order_by('-rank')
            ]
            return Response(ranks, status=status.HTTP_200_OK)
        alternatives = np.array([alt.numeric_value for alt in (CriterionOptionWeight.objects
                                                               .filter(user_id=user_id,
                                                                       criterion_option__option__in=options)
                                                               .order_by('criterion_option__option',
                                                                         'criterion_option__criterion'))])
        alternatives = np.reshape(alternatives, (len(options), len(alternatives) // (len(options))))
        ideal_options = [ideal.criterion_option.id for ideal in HellwigIdeal.objects
                         .filter(user_id=user_id, criterion_option__option__in=options)
                         .order_by('criterion_option__criterion')]
        ideal_solution = np.array([alt.numeric_value for alt in CriterionOptionWeight.objects
                                  .filter(user_id=user_id, criterion_option__in=ideal_options)
                                  .order_by('criterion_option__criterion')])
        criteria_weights = np.array([crit.criterion_weight_normalized for crit in CriterionWeight.objects
                                    .filter(user_id=user_id).order_by('id')])
        metric = 'Euclidean'
        synthVars = MCDA.Hellwig(alternatives, ideal_solution, Distance.Euclidean, criteria_weights)
        ranks = [Rank(None, user_id, option, synthVars[i], metric) for (i, option) in enumerate(options)]
        Rank.objects.bulk_create(ranks)
        ranks = [
            {
                "option" : rank.option.id,
                "synth_var": rank.rank
            }
            for rank in Rank.objects.filter(user_id=user_id, option__in=options).order_by('-rank')
        ]
        return Response(ranks, status=status.HTTP_200_OK)


class SolvingStageApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        try:
            userToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            return JwtUtil.get_user(userToken)
        except:
            return None

    def get(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                "Nie znaleziono użytkownika w bazie",
                status=status.HTTP_400_BAD_REQUEST,
            )
        stages = [{"problem": stage.problem.id, "stage": stage.stage} for stage in
                  SolvingStage.objects.filter(user_id=user_id)]
        return Response(stages, status=status.HTTP_200_OK)
