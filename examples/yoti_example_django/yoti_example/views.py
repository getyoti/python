from binascii import a2b_base64
from os.path import join, dirname

from django.views.generic import TemplateView
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from yoti_python_sdk import Client
from .app_settings import (
    YOTI_APPLICATION_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_KEY_FILE_PATH
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'app_id': YOTI_APPLICATION_ID})


class AuthView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
        activity_details = client.get_activity_details(request.GET['token'])
        context = activity_details.user_profile
        self.save_image(context.get('selfie'))
        return self.render_to_response(context)

    @staticmethod
    def save_image(base64_uri):
        base64_data_stripped = base64_uri[base64_uri.find(",") + 1:]
        binary_data = a2b_base64(base64_data_stripped)
        fd = open('yoti_example/static/YotiSelfie.jpg', 'wb')
        fd.write(binary_data)
        fd.close()
