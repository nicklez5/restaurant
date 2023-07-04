from django.urls import path,include
from . import views
urlpatterns = [
    path('<int:id>/items/',views.cartitems,name='CartItems'),
    path('<int:id>/item/',views.cartitem,name='CartItem'),
    path('list/',views.carts,name='Carts'),
    path('list/<int:id>/',views.cart,name='Cart')
]