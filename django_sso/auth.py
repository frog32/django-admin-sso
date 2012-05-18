import fnmatch

from django.contrib.auth.models import User

from openid.extensions import ax, pape, sreg

from django_sso import settings
from django_sso.models import Assignment, OpenIDUser

class DjangoSSOAuthBackend(object):
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
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
                
        # pape_response = pape.Response.fromSuccessResponse(response)
        try:
            openid_user = OpenIDUser.objects.get(claimed_id=user_data['claimed_id'])
        except OpenIDUser.DoesNotExist:
            pass
        else:
            return openid_user.user
        
        email = user_data.get('email')
        if not email:
            return None
        try:
            username, domain = email.split('@')
        except ValueError:
            return None
        possible_assignments = Assignment.objects.filter(domain=domain)
        used_assignment = None
        for assignment in possible_assignments:
            if assignment.username_mode == settings.ASSIGNMENT_ANY:
                used_assignment = assignment
                break
            elif assignment.username_mode == settings.ASSIGNMENT_MATCH:
                if fnmatch.fnmatch(username, assignment.username):
                    used_assignment = assignment
                    break
            elif assignment.username_mode == settings.ASSIGNMENT_EXCEPT:
                if not fnmatch.fnmatch(username, assignment.username):
                    used_assignment = assignment
                    break
        if used_assignment is None:
            return None
        first_and_lastname = u"%s %s" % (user_data.pop('firstname', ""), user_data.pop('lastname', ""))
        user_data['fullname'] = user_data['fullname'] or first_and_lastname
        user_data.update(user=used_assignment.user)
        openid_user = OpenIDUser.objects.create(**user_data)
        return openid_user.user
