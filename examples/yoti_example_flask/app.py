# noinspection PyPackageRequirements
import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, render_template, request

from yoti_python_sdk import Client

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from settings import (
    YOTI_APPLICATION_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_KEY_FILE_PATH,
)

app = Flask(__name__)


def save_image(selfie_data):
    upload_path = os.path.join(app.root_path, 'static', 'YotiSelfie.jpg')
    fd = open(upload_path, 'wb')
    fd.write(selfie_data)
    fd.close()


@app.route('/')
def index():
    return render_template('index.html', app_id=YOTI_APPLICATION_ID)


@app.route('/yoti/auth')
def auth():
    client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
    activity_details = client.get_activity_details(request.args['token'])
    context = vars(activity_details.profile)
    context['base64_selfie_uri'] = getattr(activity_details, 'base64_selfie_uri')
    context['user_id'] = getattr(activity_details, 'user_id')

    selfie = context.get('profile', {}).get('selfie')
    if selfie is not None:
        save_image(selfie.value)
    return render_template('profile.html',
                           **context)


if __name__ == '__main__':
    app.run(host="0.0.0.0", ssl_context='adhoc')
