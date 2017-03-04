from django.contrib.auth import get_user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def auth_test(request):
    return Response({'status': 'authenticated'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_current_user_data(request):
    user = get_user(request)
    return Response({'username': user.get_username()})
