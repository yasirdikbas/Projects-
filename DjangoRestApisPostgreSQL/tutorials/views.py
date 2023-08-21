from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from tutorials.models import *
from tutorials.serializers import *
from rest_framework.decorators import api_view
# Create your views here.

# Request types handled by the function
@api_view(['GET', 'POST', 'DELETE'])
def Test_list(request):
    # GET list of tests , POST a new test , DELETE all tests 
    # GET METHOD 
    if request.method == 'GET':
        tests  = test_list.objects.all()
        
        name = request.GET.get('test_name', None)
        if name is not None:
            tests  = tests.filter(name__icontains= name)
        
        testList_serializer = test_list_Serializer(tutorials, many=True)
        return JsonResponse(testList_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    # POST METHOD 
    elif request.method == 'POST':
        test_data = JSONParser().parse(request)
        test_serializer = test_list_Serializer(data=test_data)
        if test_serializer.is_valid():
            test_serializer.save()
            return JsonResponse(test_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE METHOD 
    elif request.method == 'DELETE':
        count = test_list.objects.all().delete()
        return JsonResponse({'message': '{} Tests were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


# Filtering and doing operation according to id 
@api_view(['GET', 'PUT', 'DELETE'])
def test_details(request, pk):
    try: 
        tutorial = test_case.objects.get(pk=pk) 
    except test_case.DoesNotExist: 
        return JsonResponse({'message': 'The testcase does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = TutorialSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


















# Request types handled by the function        
@api_view(['GET'])
def tutorial_list_published(request):
    # GET all published tutorials























