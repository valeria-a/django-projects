import io

from django.http import FileResponse
from google.cloud import storage
from google.oauth2 import service_account
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from flights_app.boarding_passes.serializers import BoardingPassSerializer
from flights_app.models import BoardingPass


class BoardigPassesViewSet(ModelViewSet):
    serializer_class = BoardingPassSerializer
    queryset = BoardingPass.objects.all()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_boarding_pass(request):

    boarding_pass_id = request.query_params['pass_id']
    print('pass id:', boarding_pass_id)

    b_pass = BoardingPass.objects.get(id=boarding_pass_id, user=request.user)
    gs_url = b_pass.url

    # gs://bucket/path/path/object
    split_url = gs_url.replace("gs://", "").split('/')
    bucket_name, *object_name = split_url
    object_name = '/'.join(object_name)


    credentials = service_account.Credentials.from_service_account_file(
        '/Users/valeria/Documents/keys/jb-eve-service-account-key.json')
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    file_obj = io.BytesIO()
    blob.download_to_file(file_obj)

    file_obj.seek(0)

    return FileResponse(file_obj)

    # blob = bucket.blob('cat-2934720_1280.jpg')
    # file_obj = io.BytesIO()
    # blob.download_to_file(file_obj)
    # file_obj.seek(0)
    # return FileResponse(file_obj, as_attachment=True, filename='cat-2934720_1280.jpg')