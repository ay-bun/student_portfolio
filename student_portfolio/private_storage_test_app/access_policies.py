from rest_access_policy import FieldAccessMixin, AccessPolicy
from django.db.models import Q

class PrivateModelAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>", "<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff", "group:student"],
            "effect": "deny"

        },
    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        groups = request.user.groups.values_list('name', flat=True)
        method = request.method

        # Field Access
        # if 'staff' not in groups:
        #     fields.pop('approved', None)
        #     fields.pop('used_for_calculation', None)

        # Cleaning data
        if method == "POST":
            # We force the user to create an event first.

            fields = {
                # 'title': fields['title'],
                'created_by': fields['created_by']
            }

        elif method == "PUT":
            pass
            # fields.pop('created_by')
            #
            # if 'staff' not in groups:  # The user is a student or lower level users.
            #     fields.pop('used_for_calculation', None)
            #     fields.pop('approved', None)

        return fields
    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q()

        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q()

        elif request.method == "DELETE":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q()