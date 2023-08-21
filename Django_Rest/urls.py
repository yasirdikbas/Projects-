from django.urls import path, include
from rest_framework import routers

from .views import *


# Register your ViewSets here 

router = routers.DefaultRouter()
router.register(r'test-viewset', TestList)
router.register(r'case-viewset', TestCase) 
router.register(r'known-error', KnownError )

urlpatterns = [
    path('', include(router.urls)),
]