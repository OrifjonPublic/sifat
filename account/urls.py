from django.urls import path
from .views import (
    CompanyView, CompanyEditView,
    RoleView, RoleEditView,
    ProductView, ProductEditView,
    UserView, UserEditView
)

urlpatterns = [
    path('company/', CompanyView.as_view(), name='company'),
    path('company/<int:pk>/', CompanyEditView.as_view(), name='company_edit'),
    path('role/', RoleView.as_view(), name='role'),
    path('role/<int:pk>/', RoleEditView.as_view(), name='role_edit'),
    path('product/', ProductView.as_view(), name='product'),
    path('product/<int:pk>/', ProductEditView.as_view(), name='product_edit'),
    path('', UserView.as_view(), name='user'),
    path('<int:pk>/', UserEditView.as_view(), name='user_edit'),

]