from tkinter import CASCADE
from django.db import models

# Creating our models here.  
class test_list(models.Model):
    Test_ID = models.AutoField(primary_key=True,) # otomatik gelmeli 
    Test_Suite_Name = models.CharField(default= None, max_length=120)
    Test_Name = models.CharField(default= None, max_length= 120)
    Test_Path = models.CharField(default= None, max_length= 1200)   
    class Meta:
        unique_together = [('Test_Suite_Name', 'Test_Path')]
    # For admin panel naming convention
    def __str__(self):
        return self.Test_Name

# TEST LIST end date eklenecekti (İPTAL OLDU) , pklerden kurtul kendileri atanacak, serializerda test listi serialzie ederken
# test caseleri de döndürmeli array olarak vs,
#Testcase ID yerine testcasein descriptionu order of test ve ismi gözükmeli.(Known error için.)

class test_case(models.Model):
    Test_ID = models.ForeignKey(test_list, default= 0, max_length=20, null=True, blank= True, on_delete=models.CASCADE)
    Test_Case_ID = models.AutoField(unique= True, primary_key= True)
    Order_Of_Test = models.IntegerField(default= 0,)
    Test_Case_Description = models.CharField(default= None, max_length=1000,)
    
    class Meta:
        unique_together = [('Test_ID', 'Test_Case_ID')]
    #For admin panel naming convention
    def __str__(self):
        return str(self.Test_Case_ID)

class known_error(models.Model):
    Test_Case_Description = models.ForeignKey(test_case, default= None, unique=True, max_length = 1000, on_delete=models.SET_DEFAULT, related_name='Test_Case_Description_KE')
    Order_Of_Test = models.ForeignKey(test_case, unique=True,on_delete=models.CASCADE,null=True, blank= True, related_name= 'Order_Of_Test_KE')
    Test_Name = models.ForeignKey(test_list, unique=True, max_length=120, on_delete=models.CASCADE,null=True, blank= True, related_name='Test_Name_KE')
    Known_Error_ID = models.AutoField(primary_key=True)
    Test_Result = models.CharField(default=None, max_length= 120)
    Test_Result_Description = models.CharField(default=None, max_length= 1200)
    End_Date =  models.DateField(blank=True, default=None) 
    Start_Date = models.DateField(default=None)
    # For admin panel naming convention 
    def __str__(self):
        return str(self.Known_Error_ID)


'''
testteki end date gereksiz. known errora start date de gerekli.
test end date ile known errordaki end date aynı şey mi ?
hangi özellikleri blank true olarak set edebilirim?   ?
Belirtilen tarihteki bir test listesini çekmek için gerekli olan ekstra sütünlardan kasıt tam olarak nedir? 
Her şey ideal olduğunda table partitioning ile alakalı kısmın implemente edilmesine geçiş yapılacak.
Known errorda on delete cascade olmalı mıdır ? 
'''