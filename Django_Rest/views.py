from urllib import request
from django.shortcuts import render
from rest_framework import status
from tutorials.models import *
from tutorials.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response 
from rest_framework import filters

# ViewSet to handle requests related to tests
class TestList(ModelViewSet): 
    serializer_class = test_list_Serializer
    queryset = test_list.objects.all() 
    http_method_names = ['get', 'post','put','patch','delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('Test_ID', 'Test_Suite_Name', 'Test_Name', 'Test_Path',)

    



# ViewSet to handle requests related to testcases 
class TestCase(ModelViewSet):
    serializer_class = test_case_Serializer
    queryset = test_case.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('Test_ID', 'Test_Case_ID')

# Not to be used at least for some time 
class KnownError(ModelViewSet):
    serializer_class = known_error_Serializer
    queryset = known_error.objects.all()
