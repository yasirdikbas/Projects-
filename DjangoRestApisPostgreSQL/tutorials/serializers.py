from rest_framework import serializers 
from tutorials.models import test_case, test_list, known_error

class test_case_Serializer(serializers.ModelSerializer):
 
    class Meta:
        model = test_case 
        fields = '__all__'

class test_list_Serializer(serializers.ModelSerializer):

    class Meta:
        model = test_list
        fields = '__all__'

class known_error_Serializer(serializers.ModelSerializer):

    class Meta: 
        model = known_error
        fields = '__all__'
