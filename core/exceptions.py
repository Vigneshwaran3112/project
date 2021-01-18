from rest_framework.exceptions import APIException, _get_error_details
from rest_framework import status


class CustomError(APIException):
    status_code = 400
    default_detail = 'permission denied.'
    default_code = 'invalid'