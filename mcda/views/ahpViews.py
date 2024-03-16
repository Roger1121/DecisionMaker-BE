from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from mcda.models import CriteriaComparison, Criterion, SolvingStage, OptionComparison, CriterionOption, Rank, Option
from mcda.jwtUtil import JwtUtil
from lib.MCDA import MCDA
from lib.DistanceMetrics import Distance

class CriteriaComparisonApiView(APIView):
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
                {"res": "Nie znaleziono użytkownika w bazie"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                {"res": "Nie podano id problemu"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        weights = CriteriaComparison.objects.filter(user_id=user_id, criterion_a__problem=problem_id)
        weights = [{"criterionA": w.criterion_a.id, "criterionB": w.criterion_b.id, "value": w.value} for w in weights]
        return Response(weights, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                {"res": "Couldn't save option weights"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(CriteriaComparison.objects.filter(user_id=user_id)) != 0:
            return Response(
                {"res": "Wartości porównań kryteriów zostały już zapisane wcześniej"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        weightsList = [CriteriaComparison(None, user_id, int(weight['criterionA']), int(weight['criterionB']), int(weight['value'])) for
                       weight in request.data]
        CriteriaComparison.objects.bulk_create(weightsList)
        problem_id = Criterion.objects.filter(id=weightsList[0].criterion_a.id).first().problem.id
        SolvingStage(None, user_id, problem_id, 2).save()
        return Response("OK", status=status.HTTP_201_CREATED)

class OptionComparisonApiView(APIView):
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
                {"res": "Nie znaleziono użytkownika w bazie"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                {"res": "Nie podano id problemu"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        weights = OptionComparison.objects.filter(user_id=user_id, option_a__option__problem=problem_id)
        weights = [{"optionA": w.option_a.id, "optionB": w.option_b.id, "value": w.value} for w in weights]
        return Response(weights, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = self.get_user(request)
        if user_id is None:
            return Response(
                {"res": "Couldn't save option weights"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(OptionComparison.objects.filter(user_id=user_id)) != 0:
            return Response(
                {"res": "Wartości porównań opcji zostały już zapisane wcześniej"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        weightsList = [OptionComparison(None, user_id, int(weight['optionA']), int(weight['optionB']), int(weight['value'])) for
                       weight in request.data]
        OptionComparison.objects.bulk_create(weightsList)
        problem_id = CriterionOption.objects.filter(id=weightsList[0].option_a.id).first().option.problem.id
        SolvingStage.objects.filter(user_id=user_id, problem_id=problem_id).update(stage=3)
        return Response("OK", status=status.HTTP_201_CREATED)

class CriterionMatrixApiView(APIView):
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
                {"res": "Nie znaleziono użytkownika w bazie"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                {"res": "Nie podano id problemu"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        criteria = Criterion.objects.filter(problem = problem_id)
        matrix = [[0] * len(criteria)] * len(criteria)
        for i, criterionA in enumerate(criteria):
            for j, criterionB in enumerate(criteria):
                if matrix[i][j] != 0:
                    continue
                elif i == j:
                    matrix[i][j] = {"value": 1, "reversed": False}
                else:
                    comparison = CriteriaComparison.objects.filter(user_id=user_id, criterion_a = criterionA.id, criterion_b = criterionB.id)
                    if len(comparison) == 0:
                        comparison = CriteriaComparison.objects.filter(user_id=user_id, criterion_a=criterionA.id,
                                                                       criterion_b=criterionB.id)
                        matrix[i][j] = {"value": comparison[0].value, "reversed": True}
                        matrix[i][j] = {"value": comparison[0].value, "reversed": False}
                    else:
                        matrix[i][j] = {"value": comparison[0].value, "reversed": False}
                        matrix[i][j] = {"value": comparison[0].value, "reversed": True}
        return Response(matrix, status = status.HTTP_200_OK)

class OptionMatrixApiView(APIView):
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
                {"res": "Nie znaleziono użytkownika w bazie"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                {"res": "Nie podano id problemu"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        criteria = Criterion.objects.filter(problem = problem_id)
        optionMatrices = []
        for criterion in criteria:
            options = CriterionOption.objects.filter(criterion = criterion.id)
            matrix = [[0] * len(options)] * len(options)
            for i, optionA in enumerate(options):
                for j, optionB in enumerate(options):
                    if matrix[i][j] != 0:
                        continue
                    elif i == j:
                        matrix[i][j] = {"value": 1, "reversed": False}
                    else:
                        comparison = OptionComparison.objects.filter(user_id=user_id, option_a=optionA.id,
                                                                       option_b=optionB.id)
                        if len(comparison) == 0:
                            comparison = OptionComparison.objects.filter(user_id=user_id, option_a=optionA.id,
                                                                           option_b=optionB.id)
                            matrix[i][j] = {"value": comparison[0].value, "reversed": True}
                            matrix[i][j] = {"value": comparison[0].value, "reversed": False}
                        else:
                            matrix[i][j] = {"value": comparison[0].value, "reversed": False}
                            matrix[i][j] = {"value": comparison[0].value, "reversed": True}
            optionMatrices.append({"criterion":criterion.id, "matrix":matrix})
        return Response(optionMatrices, status = status.HTTP_200_OK)

class AhpResultApiView(APIView):
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
                {"res": "Couldn't get result."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(CriteriaComparison.objects.filter(user_id=user_id)) == 0 or len(
                OptionComparison.objects.filter(user_id=user_id)) == 0:
            return Response(
                {"res": "Nie ukończono analizy problemu. Nie można pobrać wyników"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        problem_id = request.query_params.get('problem_id')
        if problem_id is None:
            return Response(
                {"res": "Nie podano id problemu."},
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
        criteria = Criterion.objects.filter(problem=problem_id)
        criteriaMatrix = [[0] * len(criteria)] * len(criteria)
        for i, criterionA in enumerate(criteria):
            for j, criterionB in enumerate(criteria):
                if criteriaMatrix[i][j] != 0:
                    continue
                elif i == j:
                    criteriaMatrix[i][j] = 1
                else:
                    comparison = CriteriaComparison.objects.filter(user_id=user_id, criterion_a=criterionA.id,
                                                                   criterion_b=criterionB.id)
                    if len(comparison) == 0:
                        comparison = CriteriaComparison.objects.filter(user_id=user_id, criterion_a=criterionA.id,
                                                                       criterion_b=criterionB.id)
                        criteriaMatrix[i][j] = 1 / comparison[0].value
                        criteriaMatrix[i][j] = comparison[0].value
                    else:
                        criteriaMatrix[i][j] = comparison[0].value
                        criteriaMatrix[i][j] = 1 / comparison[0].value
        optionMatrices = []
        for criterion in criteria:
            options = CriterionOption.objects.filter(criterion=criterion.id)
            matrix = [[0] * len(options)] * len(options)
            for i, optionA in enumerate(options):
                for j, optionB in enumerate(options):
                    if matrix[i][j] != 0:
                        continue
                    elif i == j:
                        matrix[i][j] = 1
                    else:
                        comparison = OptionComparison.objects.filter(user_id=user_id, option_a=optionA.id,
                                                                     option_b=optionB.id)
                        if len(comparison) == 0:
                            comparison = OptionComparison.objects.filter(user_id=user_id, option_a=optionA.id,
                                                                         option_b=optionB.id)
                            matrix[i][j] = 1 / comparison[0].value
                            matrix[i][j] = comparison[0].value
                        else:
                            matrix[i][j] = comparison[0].value
                            matrix[i][j] = 1 / comparison[0].value
            optionMatrices.append({"criterion": criterion.id, "matrix": matrix})
        synthVars = MCDA.AHP(criteriaMatrix, optionMatrices, Distance.Mahalanobis)
        ranks = [Rank(None, user_id, option, synthVars[i]) for (i, option) in enumerate(options)]
        Rank.objects.bulk_create(ranks)
        ranks = [
            {
                "option" : rank.option.id,
                "synth_var": rank.rank
            }
            for rank in Rank.objects.filter(user_id=user_id, option__in=options).order_by('-rank')
        ]
        return Response(ranks, status=status.HTTP_200_OK)