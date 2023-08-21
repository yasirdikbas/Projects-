from django.db import models

# Creating our models here.
class test_list(models.Model):
    test_suite_name = models.CharField(default= None, max_length=120)
    test_name = models.CharField(default= None, max_length= 120)
    test_path = models.CharField(default= None, max_lenght =120 )

class test_case(models.Model):
    test_id = models.IntegerField(default= 0, unique= True, max_length=20)
    rank_of_test = models.IntegerField(default= 0, max_length=20)
    test_case_description = models.CharField(default= None, max_length=1000)

class known_error(models.Model):
    test_case_id = models.IntegerField(default= 0, unique=True, max_length = 20)
    known_error_id = models.IntegerField(default=0, max_length= 20)
    test_result = models.CharField(default=None, max_length= 120)
    test_result_description = models.CharField(default=None, max_length= 1200)
    end_date =  models.DateTimeField(blank=True) 

 # hangi özellikleri blank true olarak set edebilirim, hangileri blank false olmak zorunda ?    
