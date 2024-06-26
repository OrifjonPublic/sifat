from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser


class WorkRecordView(ListCreateAPIView):
    queryset = WorkRecord.objects.all()
    serializer_class = WorkRecordSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class WorkRecordDetailView(RetrieveUpdateDestroyAPIView):
    queryset = WorkRecord.objects.all()
    serializer_class = WorkRecordSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class DefectRecordView(ListCreateAPIView):
    queryset = DefectRecord.objects.all()
    serializer_class = DefectRecordSerializer
    parser_classes = [MultiPartParser, FileUploadParser, JSONParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['rasmlar'] = self.request.data.getlist('images')
        return context


class DefectRecordDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DefectRecord.objects.all()
    serializer_class = DefectRecordSerializer
    lookup_field = 'id'
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class DefectView(ListCreateAPIView):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer


class DefectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    lookup_field = 'id'


class DepartmentView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id'


class CompanyView(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyEditView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'


class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductEditView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class RoleView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleEditView(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id'


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserEditView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    