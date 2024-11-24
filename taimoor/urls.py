from django.urls import path,include  # type: ignore
from django.contrib import admin # type: ignore

from blogger import views
from blogger.views import  ItemListCreate,LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('items/', views.item_list_create, name='item-list-create'),
    # path('items/<int:pk>/', views.item_detail, name='item-detail'),
    path('items/', ItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemListCreate.as_view(), name='item-list-create'),
    # path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('login/', LoginView.as_view(), name='login'),

]
