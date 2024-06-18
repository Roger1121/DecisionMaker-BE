from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mcda.models import CriteriaComparison, Criterion, OptionComparison, CriterionOption, Rank, Option, AppUser
from lib.MCDA import MCDA


class CriteriaConsistencyApiView(APIView):
    def get(self, request, *args, **kwargs):
        systems = []
        for user in AppUser.objects.all():
            if len(OptionComparison.objects.filter(user_id=user.id)) == 0:
                continue
            problem_id = user.training_group + 1
            criteria = Criterion.objects.filter(problem=problem_id)
            criteriaMatrix = [[0 for _ in range(len(criteria))] for _ in range(len(criteria))]
            for i, criterionA in enumerate(criteria):
                for j, criterionB in enumerate(criteria):
                    if criteriaMatrix[i][j] != 0:
                        continue
                    elif i == j:
                        criteriaMatrix[i][j] = 1
                    else:
                        comparison = CriteriaComparison.objects.filter(user_id=user.id, criterion_a=criterionA.id,
                                                                       criterion_b=criterionB.id)
                        if len(comparison) == 0:
                            comparison = CriteriaComparison.objects.filter(user_id=user.id, criterion_a=criterionB.id,
                                                                           criterion_b=criterionA.id)
                            criteriaMatrix[i][j] = 1 / comparison[0].value
                            criteriaMatrix[j][i] = comparison[0].value
                        else:
                            criteriaMatrix[i][j] = comparison[0].value
                            criteriaMatrix[j][i] = 1 / comparison[0].value
            cr = MCDA.AHPMatrixConsistencyFactor(criteriaMatrix)
            systems.append(
                {
                    'user_id': user.id,
                    'consistency_ratio': cr
                })
        return Response(systems, status=status.HTTP_200_OK)

class OptionsConsistencyApiView(APIView):
    def get(self, request, *args, **kwargs):
        systems = []
        for user in AppUser.objects.all():
            if len(OptionComparison.objects.filter(user_id=user.id)) == 0:
                continue
            problem_id = user.training_group + 1
            criteria = Criterion.objects.filter(problem=problem_id)
            optionMatrices = []
            for criterion in criteria:
                crit_options = CriterionOption.objects.filter(criterion=criterion.id).order_by('criterion')
                matrix = [[0 for _ in range(len(crit_options))] for _ in range(len(crit_options))]
                for i, optionA in enumerate(crit_options):
                    for j, optionB in enumerate(crit_options):
                        if matrix[i][j] != 0:
                            continue
                        elif i == j:
                            matrix[i][j] = 1
                        else:
                            comparison = OptionComparison.objects.filter(user_id=user.id, option_a=optionA.id,
                                                                         option_b=optionB.id)
                            if len(comparison) == 0:
                                comparison = OptionComparison.objects.filter(user_id=user.id, option_a=optionB.id,
                                                                             option_b=optionA.id)
                                matrix[i][j] = 1 / comparison[0].value
                                matrix[j][i] = comparison[0].value
                            else:
                                matrix[i][j] = comparison[0].value
                                matrix[j][i] = 1 / comparison[0].value
                cr = MCDA.AHPMatrixConsistencyFactor(matrix)
                systems.append(
                    {
                        'user_id': user.id,
                        'criterion_id': criterion.id,
                        'consistency_ratio': cr
                    })
        return Response(systems, status=status.HTTP_200_OK)