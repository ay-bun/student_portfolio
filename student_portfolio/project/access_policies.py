from datetime import datetime

from django.db.models import Q
from rest_access_policy import AccessPolicy

class ProjectApiAccessPolicy(AccessPolicy):

    statements = [
        {
            "action": ["<method:get>", "<method:post>", "<method:put>", "<method:delete>"],
            "principal": ["group:staff", "group:student"],
            "effect": "allow"
        },
    ]
    
    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        groups = request.user.groups.values_list('name', flat=True)
        method = request.method


        if method == "GET":
            pass

        # Cleaning data
        elif method == "POST":
            fields.pop('id', None)

            if 'staff' not in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        elif method == "PUT":
            fields.pop('created_by', None)

            if 'staff' not in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":
            lower_bound_start_date = request.GET.get('lower_bound_start_date', None)
            upper_bound_start_date = request.GET.get('upper_bound_start_date', None)

            query_object = Q()
            if lower_bound_start_date is not None:
                query_object &= Q(start_date__gte=datetime.strptime(lower_bound_start_date, '%Y-%m-%d'))

            if upper_bound_start_date is not None:
                query_object &= Q(start_date__lte=datetime.strptime(upper_bound_start_date, '%Y-%m-%d'))

            if 'staff' in groups:
                return query_object

            elif 'student' in groups:
                return query_object & (Q(approved=True) | Q(created_by=request.user.id))

        elif request.method == "PUT":
            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(approved=False) & Q(created_by=request.user.id)

        elif request.method == "DELETE":

            if 'staff' in groups:
                return Q()

            elif 'student' in groups:
                return Q(approved=False) & Q(created_by=request.user.id)