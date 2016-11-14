from django.utils.html import format_html

from .login_button import get_login_button_html
from .settings import YOTI_VERIFICATION_KEY, YOTI_APPLICATION_ID


def yoti_context(request):
    context = login_button_context(request)
    context.update(site_verification_context(request))
    context.update(application_context(request))
    return context


def login_button_context(request):
    return {
        'yoti_login_button': get_login_button_html,
        'yoti_login_button_sm': get_login_button_html('small'),
        'yoti_login_button_md': get_login_button_html('medium'),
        'yoti_login_button_lg': get_login_button_html('large')
    }


def site_verification_context(request):
    raw_text = '<meta name="yoti-site-verification" content="{0}">'.format(
        YOTI_VERIFICATION_KEY
    )
    return {'yoti_site_verification': format_html(raw_text)}


def application_context(request):
    return {'yoti_application_id': YOTI_APPLICATION_ID}
