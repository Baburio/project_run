from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status

from .serializers import RunSerializer, UserSerializer
from django.conf import settings
from .models import Run, User
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

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer


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
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

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
