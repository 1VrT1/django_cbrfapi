from django.urls import path
from .views import ChooseParams, Info

urlpatterns = [
    path('', ChooseParams.as_view()),
    path('Information/', Info.as_view(), name='information')
]
