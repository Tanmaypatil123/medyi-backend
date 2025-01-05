# Standard Library
import logging
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    def log_error(self, error):
        logger.error(error, exc_info=True)

    def log_exception(self, exception):
        logger.exception(exception)

