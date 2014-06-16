try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from openid.extensions import ax, sreg

from admin_sso import settings
from admin_sso.models import Assignment, OpenIDUser


def authenticate(self, **kwargs):
    response = kwargs.pop('openid_response', None)
    if not response:
        return None
    user_data = {}
    user_data['claimed_id'] = response.getDisplayIdentifier()
    sreg_response = sreg.SRegResponse.fromSuccessResponse(response)
    if sreg_response:
        for field_name in ('email', 'fullname',):
            user_data[field_name] = sreg_response.get(field_name, None)

    ax_response = ax.FetchResponse.fromSuccessResponse(response)
    if ax_response:
        for ax_name, field_name in settings.AX_MAPPING:
            value = ax_response.getSingle(ax_name)
            user_data[field_name] = value or user_data.get(field_name)
    try:
        openid_user = OpenIDUser.objects.get(
            claimed_id=user_data['claimed_id'])
    except OpenIDUser.DoesNotExist:
        pass
    else:
        openid_user.user.active_openid_user = openid_user
        return openid_user.user

    email = user_data.get('email')
    assignment = Assignment.objects.for_email(email)
    if assignment is None:
        return None

    first_and_lastname = u"%s %s" % (
        user_data.pop('firstname', ""), user_data.pop('lastname', ""))
    user_data['fullname'] = user_data['fullname'] or first_and_lastname
    user_data.update(user=assignment.user)
    openid_user = OpenIDUser.objects.create(**user_data)
    openid_user.user.active_openid_user = openid_user
    return openid_user.user
