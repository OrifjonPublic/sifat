from django.urls import path
from .views import (
    CompanyView, CompanyEditView,
    RoleView, RoleEditView,
    ProductView, ProductEditView,
    UserView, UserEditView,
    DepartmentDetailView, DepartmentView,
    DefectView, DefectDetailView
)

urlpatterns = [
    path('company/', CompanyView.as_view(), name='company'),
    path('company/<int:id>/', CompanyEditView.as_view(), name='company_edit'),
    path('role/', RoleView.as_view(), name='role'),
    path('role/<int:id>/', RoleEditView.as_view(), name='role_edit'),
    path('product/', ProductView.as_view(), name='product'),
    path('product/<int:id>/', ProductEditView.as_view(), name='product_edit'),
    path('', UserView.as_view(), name='user'),
    path('<int:id>/', UserEditView.as_view(), name='user_edit'),
    path('department/', DepartmentView.as_view(), name='department'),
    path('department/<int:id>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('defect/', DefectView.as_view(), name='defect'),
    path('defect/<int:id>/', DefectDetailView.as_view(), name='defect_detail'),

]