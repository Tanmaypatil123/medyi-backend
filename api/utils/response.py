# Standard Library
import logging
from typing import Optional

# Third Party Stuff
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def status_200(message="", data=None):
    # Explicit None check is required, because data can contain empty list - []
    if data is not None:
        return Response({"message": message, "data": data},  status=status.HTTP_200_OK)
    return Response({"message": message}, status=status.HTTP_200_OK)


def status_400(message, error_code: int = 400):
    return Response({"error": {"error_code": error_code, "err_message": message}}, status=status.HTTP_400_BAD_REQUEST)


def status_500(err: Optional[Exception] = None):
    if err:
        logger.error(err)
    # TODO: error code will be a string
    return Response(
        {"error": {"error_code": 500, "err_message": "Something went wrong"}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )




def json_status_200(message="", data=None):
    # Explicit None check is required, because data can contain empty list - []
    if data is not None:
        return JsonResponse({"message": message, "data": data}, status=status.HTTP_200_OK)
    return JsonResponse({"message": message}, status=status.HTTP_200_OK)

def json_status_400(message, error_code: int = 400):
    return JsonResponse({"error": {"error_code": error_code, "err_message": message}},
                    status=status.HTTP_400_BAD_REQUEST)

def json_status_500(err: Optional[Exception] = None):
    if err:
        logger.error(err)
    # TODO: error code will be a string
    return JsonResponse(
        {"error": {"error_code": 500, "err_message": "Something went wrong"}},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


