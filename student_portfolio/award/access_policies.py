from datetime import datetime

from django.db.models import Q
from rest_access_policy import AccessPolicy

class AwardApiAccessPolicy(AccessPolicy):

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

        elif method == "POST":
            fields.pop('id', None)

            if 'staff' in groups:
                pass
            elif 'student' in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        elif method == "PUT":
            fields.pop('created_by', None)

            if 'staff' in groups:
                pass
            elif 'student' in groups:
                fields.pop('used_for_calculation', None)
                fields.pop('approved', None)
                fields.pop('approved_by', None)

        return fields

    @classmethod
    def scope_query_object(cls, request):
        groups = request.user.groups.values_list('name', flat=True)

        if request.method == "GET":

            lower_bound_received_date = request.GET.get('lower_bound_received_date', None)
            upper_bound_received_date = request.GET.get('upper_bound_received_date', None)
            # print(lower_bound_received_date)
            # print(upper_bound_received_date)
            query_object = Q()
            if lower_bound_received_date is not None:
                query_object &= Q(received_date__gte=datetime.strptime(lower_bound_received_date, '%Y-%m-%d'))

            if upper_bound_received_date is not None:
                query_object &= Q(received_date__lte=datetime.strptime(upper_bound_received_date, '%Y-%m-%d'))

            if 'staff' in groups:
                return query_object

            elif 'student' in groups:
                return query_object & (Q(receivers=request.user.id) | Q(created_by=request.user.id))

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