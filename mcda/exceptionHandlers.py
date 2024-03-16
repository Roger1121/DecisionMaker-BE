from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def handler500(request, *args, **argv):
    return Response(
        "Podczas przetwarzania akcji wystąpił nieoczekiwany błąd",
        status=status.HTTP_400_BAD_REQUEST,
    )


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if exc is not None:
        response = Response(
            "Podczas przetwarzania akcji wystąpił nieoczekiwany błąd",
            status=status.HTTP_400_BAD_REQUEST,
        )
    return response
