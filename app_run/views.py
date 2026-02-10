from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from .serializers import RunSerializer, UserSerializer, AthleteInfoSerialzer
from django.conf import settings
from .models import Run, User, AthleteInfo
from django.shortcuts import get_object_or_404


# Create your views here.

@api_view(['GET'])
def company_details(request):
    details = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts':settings.CONTACTS,
    }
    return Response(details)

class PagePagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 50



class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status','athlete']
    ordering_fields = ['created_at'] 


class RunStartView(APIView):

    def post(self, request, run_id):
        run = get_object_or_404(Run, id = run_id)

        if run.status != Run.Status.INIT:
            return Response (status = status.HTTP_400_BAD_REQUEST)
        
        run.status = Run.Status.IN_PROGRESS
        run.save()

        return Response (status=status.HTTP_200_OK)


class RunStopView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id = run_id)

        if run.status != Run.Status.IN_PROGRESS:
            return Response (status = status.HTTP_400_BAD_REQUEST)
        
        run.status = Run.Status.FINISHED
        run.save()
        return Response (status=status.HTTP_200_OK)
    

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PagePagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_foelds = ['date_joined']

    def get_queryset(self):
        qs = self.queryset
        qs = qs.exclude(is_superuser = True)
        type = self.request.query_params.get('type', None)

        if type == 'coach':
            qs = qs.filter(is_staff = True)
            return qs            
        elif type == 'athlete':
            qs = qs.filter(is_staff = False)
            return qs
        else:
            return qs

class AthleteInfoViewSet(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id = user_id)
        info, created = AthleteInfo.objects.get_or_create(user = user)
        serializer = AthleteInfoSerialzer(
            info,
            context = {'request':request}
        )
        return Response(serializer.data)
    
    def put(self, request, user_id):
        user =get_object_or_404(User, id = user_id)

        if request.data.get('weight') > 900 or request.data.get('weight') < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        info, created = AthleteInfo.objects.update_or_create(
            user = user, 
            defaults={
            "goals" : request.data.get('goals'),
            "weight" : request.data.get('weight'),
            }
            )

        return Response(status=status.HTTP_200_OK)