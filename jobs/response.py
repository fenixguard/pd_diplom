from django.utils.translation import gettext_lazy as _
from rest_framework import status as http_status
from rest_framework.response import Response

from jobs.utils import is_dict


def ResponseOK(**kwargs):
    response = {'Status': True}
    if kwargs:
        response.update(kwargs)
    return Response(response, status=http_status.HTTP_200_OK)


def ResponseCreated(**kwargs):
    response = {'Status': True}
    if kwargs:
        response.update(kwargs)
    return Response(response, status=http_status.HTTP_201_CREATED)


def UniversalResponse(error=None, format=None, status=418, **kwargs):
    response = {'Status': False}
    if error:
        if format:
            if is_dict(format):
                response['Errors'] = _(error if is_dict(error) else str(error)).format(**format)
            else:
                response['Errors'] = _(error if is_dict(error) else str(error)).format(str(format))
        else:
            response['Errors'] = _(error if is_dict(error) else str(error))
    if kwargs:
        response.update(kwargs)
    return Response(response, status=status)


def ResponseBadRequest(error=None, format=None, status=None, **kwargs):
    return UniversalResponse(error, format, http_status.HTTP_400_BAD_REQUEST, **kwargs)


def ResponseForbidden(error=None, format=None, status=None, **kwargs):
    return UniversalResponse(error, format, http_status.HTTP_403_FORBIDDEN, **kwargs)


def ResponseConflict(error=None, format=None, status=None, **kwargs):
    return UniversalResponse(error, format, http_status.HTTP_409_CONFLICT, **kwargs)


def ResponseNotFound(error=None, format=None, status=None, **kwargs):
    return UniversalResponse(error, format, http_status.HTTP_404_NOT_FOUND, **kwargs)
