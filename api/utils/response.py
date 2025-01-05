# Standard Library
import logging
from enum import Enum
from typing import Optional

# Third Party Stuff
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import functools
import inspect
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

class ExceptionType(Enum):
    SILENT = "SILENT"
    WARNING = "WARNING"
    FORM_VALIDATION_ERROR = "FORM_VALIDATION_ERROR"



class ServiceException(Exception):
    @property
    def type(self):
        return self._type

    @property
    def error_code(self):
        return self._error_code

    @property
    def message(self):
        return self._message

    @property
    def error_message(self):
        return self._error_message

    def __init__(self, *args, **kwargs):
        logger.info(f"[ServiceException][__init__] :: args - {args} :: kwargs - {kwargs}")
        self._type = kwargs.get("type", ExceptionType.WARNING)
        self._error_code = kwargs.get("error_code", 400)
        self._error_message = kwargs.get("error_message", None)
        self._message = kwargs.get("message", None)
        Exception.__init__(self, *args)


def handle_post_exception(func: callable) -> callable:
    if not inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ServiceException as se:
                if se.type == ExceptionType.SILENT:
                    logger.info(se, exc_info=True)
                else:
                    logger.warning(se, exc_info=True)
                return status_400(str(se), error_code=se.error_code)
            except Exception as e:
                logger.error(e, exc_info=True)
                return status_500()

        return wrapper

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ServiceException as se:
            if se.type == ExceptionType.SILENT:
                logger.info(se, exc_info=True)
            else:
                logger.warning(se, exc_info=True)
            return status_400(str(se), error_code=se.error_code)
        except Exception as e:
            logger.error(e, exc_info=True)
            return status_500()

    return wrapper
