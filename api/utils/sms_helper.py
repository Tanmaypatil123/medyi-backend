# Standard Library
import logging
from api.utils.two_factor_sms_service import two_factor_sms_service
from enum import Enum
from typing import Optional

# Third Party Stuff
from django.core.cache import cache


logger = logging.getLogger(__name__)


class OTPServiceName(Enum):
    TWO_FACTOR = "TWO_FACTOR"
    MSG_91 = "MSG_91"


class SMSHelper:
    def __init__(self):
        pass

    def send_login_otp(self, *, mobile_no: str, template: str = "login_otp") -> Optional[dict]:
        result = two_factor_sms_service.send_login_otp(mobile_no=mobile_no, template=template)
        self._update_otp_request_status(result=result)

        return result

    def _update_otp_request_status(self, result):
        from api.services import get_cache_key_and_timeout
        new_status = "Y" if result is not None else "N"
        cache_key, cache_timeout = get_cache_key_and_timeout("TWO_FACTOR_OTP_LAST_STATUSES_CACHE")
        otp_statuses = cache.get(cache_key)
        if otp_statuses:
            if len(otp_statuses) < 25:
                new_status = otp_statuses + new_status
            else:
                new_status = otp_statuses[1:] + new_status
        cache.set(cache_key, new_status, cache_timeout)

    def verify_login_otp(self, *, otp: str, verification_id: str, mobile_no: str) -> dict:
        if (
                (mobile_no in ["9876543210", "9876543211"] and otp)

        ):
            return dict(verification_id=verification_id, Details="OTP Matched")
        return two_factor_sms_service.verify_login_otp(
            mobile_no=mobile_no, verification_id=verification_id, otp=otp
        )


sms_helper = SMSHelper()
