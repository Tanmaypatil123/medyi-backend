# Standard Library
import json
import logging
from typing import Optional

# Third Party Stuff
import requests
from django.conf import settings

from api.utils.response import ServiceException, ExceptionType

logger = logging.getLogger(__name__)


class TwoFactorSMSService:
    def __init__(self, config):
        self.api_key = config["API_KEY"]
        self.txn_sms_url = (
                config["BASE_URL"] + "/" + self.api_key + config["TRANSACTION_SMS_SUFFIX"]
        )
        self.login_otp_sms_url = config["BASE_URL"] + config["LOGIN_OTP_SMS_SUFFIX"]
        self.verify_login_otp_sms_url = config["BASE_URL"] + config["VERIFY_LOGIN_OTP_SUFFIX"]
        self.templates = config["templates"]

    def send_otp(self, *, mobile_no: str, template: str = "login_otp"):
        template_data = self.templates.get(template, None)
        logger.info(f"[OTP] send otp before request to {mobile_no} template {template}")
        if not template_data:
            return None
        otp_url = self.login_otp_sms_url.format(
            self.api_key, mobile_no, template_data["template_name"]
        )
        response = requests.get(otp_url)
        return response

    def send_login_otp(self, *, mobile_no: str, template: str = "login_otp") -> Optional[dict]:
        logger.info(f"here is coming without any thing...")
        response = self.send_otp(mobile_no=mobile_no, template=template)
        if response:
            data = response.json()
            logger.info(
                "[login otp] to {} template{}, after request {}".format(mobile_no, template, data)
            )
            if data["Status"] == "Success":
                result = dict()
                result["verification_id"] = data["Details"]
                result["mobile_no"] = mobile_no
                logger.info(
                    f"[OTP] send otp success request to {mobile_no} template {template} details {data['Details']}"
                )
                return result
            else:
                logger.info(
                    f"[OTP] send otp failed request to {mobile_no} template {template} details {data}"
                )
                raise ServiceException("Invalid Mobile Number")

        else:
            logger.info(
                f"[OTP] send otp failed request to {mobile_no} template {template} response status {response.status_code}"
            )
            return None

    def verify_otp(self, *, otp: str, verification_id: str, mobile_no: str):
        logger.info(
            f"[OTP] verify login otp {otp} verificationId {verification_id} mobile {mobile_no}, before request"
        )
        verify_otp_url = self.verify_login_otp_sms_url.format(self.api_key, verification_id, otp)
        response = requests.get(verify_otp_url)
        return response

    def verify_login_otp(self, *, otp: str, verification_id: str, mobile_no: str) -> dict:
        response = self.verify_otp(otp=otp, verification_id=verification_id, mobile_no=mobile_no)
        logger.info(
            f"[OTP] verify login otp {otp} verificationId {verification_id} mobile {mobile_no}, request {response.status_code} {response.text}"
        )
        error_msg = ""
        if 200 <= response.status_code < 300:
            try:
                data = response.json()
                if data["Status"] == "Success":
                    result = dict()
                    result["verification_id"] = verification_id
                    result["Details"] = data["Details"]
                    logger.info(
                        f"[OTP] verify login success request otp {otp} verificationId {verification_id} mobile {mobile_no}"
                    )
                    return result
                else:
                    logger.info(
                        f"[OTP] login otp failed request otp {otp} verificationId {verification_id} mobile {mobile_no}"
                    )
                    error_msg = "Wrong Otp"
            except Exception as e:
                if '"Status":"Success"' in response.text:
                    logger.warning(e)
                    result = dict()
                    result["verification_id"] = verification_id
                    result["Details"] = "OTP Matched"
                    logger.info(
                        f"[OTP] verify login success request otp {otp} verificationId {verification_id} mobile {mobile_no}"
                    )
                    return result
                else:
                    logger.error(e, exc_info=True)
                    raise ServiceException("Invalid OTP")
        else:
            logger.info(
                f"[OTP] login otp failed request otp {otp} verificationId {verification_id} mobile {mobile_no}"
            )
            if response.status_code == 400:
                data = response.json()
                if data["Status"] == "Error":
                    raise ServiceException("Invalid Otp", type=ExceptionType.SILENT)
            elif response.status_code == 500:
                # this will let us know if the otp verification service is down or running
                raise ServiceException("Authentication Failed")

            raise ServiceException(f"Otp Verification Error: {response.reason}")

        if error_msg:
            raise ServiceException(error_msg, type=ExceptionType.SILENT)


two_factor_sms_service = TwoFactorSMSService(settings.TWO_FACTOR_SMS_SERVICE_CONFIG)
