from django.db.models import Prefetch
from rest_framework.views import APIView
from yaml import serialize

from apps.inform.models import Inform, InformRead
from apps.inform.serializers import InformSerializer
from django.db.models import Q,Prefetch
from django.db.models import Count
from rest_framework.response import Response
from apps.absent.models import Absent
from apps.absent.serializers import AbsentSerializer
from apps.oaauth.models import OADepartment
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class LatestInformView(APIView):
    """
    返回最新的10条通知
    """
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        current_user= request.user
        informs = Inform.objects.prefetch_related(Prefetch('reads',queryset=InformRead.objects.filter(user_id=current_user.uid)),'departments').filter(Q(public = True)|Q(departments = current_user.department))[:10]
        serializer  = InformSerializer(informs,many=True)
        return Response(serializer.data)

class LatestAbsentView(APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        current_user = request.user
        queryset = Absent.objects
        if current_user.department.name !="董事会":
            queryset = queryset.filter(requester__department_id = current_user.department_id)
        queryset = queryset.all()[:10]
        serializer = AbsentSerializer(queryset, many=True)
        return Response(serializer.data)

class DepartmentStaffCountView(APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        rows = OADepartment.objects.annotate(staff_count = Count("staffs")).values("name","staff_count")
        return Response(rows)