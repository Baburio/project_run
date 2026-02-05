from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import RunSerializer 
from django.conf import settings
from .models import Run


# Create your views here.

@api_view(['GET'])
def company_details(request):
    details = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts':settings.CONTACTS,
    }
    return Response(details)

class Run_View(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
