from django.db.models import Q
from rest_access_policy import AccessPolicy


class StaffApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
    ]

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q()


class StudentApiAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"

        },
        {
            "action": ["<method:put>"],
            "principal": ["group:staff"],
            "effect": "allow"

        },
    ]

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":

            query_scope_object = Q()

            curriculum_id = request.GET.get('curriculum_id', None)
            if curriculum_id is not None:
                query_scope_object &= Q(enroll=curriculum_id)

            if 'staff' in groups:
                query_scope_object &= Q()

            elif 'student' in groups:
                query_scope_object &= Q(user_id_fk=request.user.id)

            return query_scope_object

        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        groups = request.user.groups.values_list('name', flat=True)

        if request.method == 'PUT':
            if 'staff' in groups:
                fields = {
                    'id' : fields['id'],
                    'enroll' : fields['enroll']
                }

        return fields

class UserProfileApiAccessPolicy(AccessPolicy):

    statements = [
        {
            "action": ["<method:get>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
    ]


    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        groups = request.user.groups.values_list('name', flat=True)
        method = request.method

        # Cleaning data
        if method == "POST":
            pass

        elif method == "PUT":
            pass

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(user_id_fk=request.user.id)