from django.conf import settings # import the settings file
from google.appengine.ext import blobstore

def host_name(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'HOST': settings.HOST}

def url_upload_image(request):
	upload_url = blobstore.create_upload_url('/upload-image/')
	return {'url_upload_image': upload_url}