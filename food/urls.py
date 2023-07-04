from django.urls import path,include
from . import views
urlpatterns = [
    path('list/',views.foods,name='Foods'),
    path('list/<int:id>/',views.food,name='Food'),
]