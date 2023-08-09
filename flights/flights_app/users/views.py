import os.path
import uuid
from pprint import pprint

import boto3 as boto3
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from flights_app.users.serializers import UserSerializer, ExtendedTokenObtainPairSerializer, DetailedUserSerializer, \
    UserProfileSerializer, StaffUserSerializer

from google.oauth2 import id_token
from google.auth.transport import requests


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.profile.address
        }
        return JsonResponse(data)



# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def me(request):
#     print(request.user)
#     if request.user.is_authenticated:
#         # you will get here only if the user is already authenticated!
#         user_serializer = UserProfileSerializer(instance=request.user, many=False)
#         return Response(data=user_serializer.data)
#     else:
#         return Response(status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    # you will get here only if the user is already authenticated!
    #
    # if not request.user.is_staff:
    #     user_serializer = UserProfileSerializer(instance=request.user, many=False)
    #     return Response(data=user_serializer.data)
    # else:
    #     user_serializer = StaffUserSerializer(instance=request.user, many=False)
    #     return Response(data=user_serializer.data)

    serializer_class = StaffUserSerializer if request.user.is_staff else UserProfileSerializer
    user_serializer = serializer_class(instance=request.user, many=False)
    return Response(data=user_serializer.data)


class ExtendedTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = ExtendedTokenObtainPairSerializer


@api_view(['POST'])
def google_login(request):
    google_jwt = request.data['google_jwt']
    CLIENT_ID = '872794659630-ehu55i6a7fbglef45mjno5pgjv7qeab9.apps.googleusercontent.com'
    try:
        idinfo = id_token.verify_oauth2_token(google_jwt, requests.Request(), CLIENT_ID)
        email = idinfo['email']
        try:
            user = User.objects.get(email=email)
            print('user found')
            print(user)
            # creating jwt manually

        except User.DoesNotExist:
            print('does not exist')
            user = User.objects.create_user(username=email, email=email, password=str(uuid.uuid4()),
                                     first_name=idinfo['given_name'], last_name=idinfo['family_name'])

        refresh = RefreshToken.for_user(user)
        return Response(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

        print(idinfo)
    except ValueError as e:
        print(e)
    print(google_jwt)
    return Response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_img(request):
    bucket_name = 'edulabs-flights-profile'
    file_stream = request.FILES['file'].file
    _, ext = os.path.splitext(request.FILES['file'].name)

    object_name = f"profile_img_{request.user.id}{ext}"

    try:
        s3 = boto3.client('s3')
        # response = s3.upload_file(
        #         '../requirements.txt', bucket_name, object_name+'.txt')
        s3.upload_fileobj(file_stream, bucket_name, object_name)

        request.user.profile.img_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        request.user.profile.save()
    except Exception:
        return Response(status=500)

    return Response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_img_url(request):
    bucket_name = 'edulabs-flights-profile'
    filename = request.data['filename']
    _, ext = os.path.splitext(filename)

    object_name = f"profile_img_{request.user.id}_{uuid.uuid4()}{ext}"

    s3 = boto3.client('s3')
    response = s3.generate_presigned_post(bucket_name, object_name, ExpiresIn=3600)
    pprint(response)

    # request.user.profile.img_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    # request.user.profile.save()
    return Response(data=response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_img_done(request):
    bucket_name = 'edulabs-flights-profile'
    object_name = request.data['object_name']
    old_url = request.user.profile.img_url

    request.user.profile.img_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    request.user.profile.save()

    s3 = boto3.client('s3')

    old_object_name = old_url.split("/")[-1]
    s3.delete_object(Bucket='edulabs-flights-profile', Key=old_object_name)

    ser = UserProfileSerializer(request.user)
    return Response(data=ser.data)
