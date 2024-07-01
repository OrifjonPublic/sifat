from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'first_name', 'password', 'last_name', 'gender', 'department', 'profile_picture')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("This username is already in use."))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username', None),
            role=validated_data.get('role', None),
            department=validated_data.get('department', None),
            first_name = validated_data.get('first_name'),
            
            gender = validated_data.get('gender'),
            last_name = validated_data.get('last_name')
        )   
        if validated_data.get('profile_picture'):
            user.profile_picture = validated_data.get('profile_picture')
        # profile_picture =      
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.username = validated_data.get('username', instance.username)
        instance.department = validated_data.get('department', instance.department)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance


class MyOwnSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token =  super().get_token(user)
        token['username'] = user.username
        if user.role:
            token['role'] = user.role.name
        token['profile_picture'] = user.profile_picture.url
        if token.department:
            token['department'] = user.department.name
        token['id'] = user.id
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        data['id'] = self.user.id
        data['username'] = self.user.username
        # if self.user.role:
        if self.user.role:
            data['role'] = self.user.role.name
        if self.user.department:
            data['department'] = self.user.department.name
        data['profile_picture'] = self.user.profile_picture.url       
        return data
    

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
    

class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'


class WorkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkRecord
        fields = ['employee', 'product', 'quantity', 'work_time']
    def __init__(self, *args, **kwargs):
        super(WorkRecordSerializer, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = User.objects.filter(role__name='xodim')
        
    def create(self, validated_data):
        work_record = WorkRecord.objects.create(
            employee=validated_data.get('employee'),
            product=validated_data.get('product'),
            quantity=validated_data.get('quantity'),
            work_time = validated_data.get('work_time')
        )
        work_record.created_by = self.context.get('request').user
        work_record.save()
        return work_record
    
    def update(self, instance, validated_data):
        instance.employee = validated_data.get('employee', instance.employee)
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.work_time = validated_data.get('work_time', instance.work_time)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()
        return instance
    

class DefectRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectRecord
        fields = ['employee', 'defect', 'quantity']
    def __init__(self, *args, **kwargs):
        super(DefectRecordSerializer, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = User.objects.filter(role__name='xodim')
    
    def create(self, validated_data):
        defect_record = DefectRecord.objects.create(
            employee=validated_data.get('employee'),
            defect=validated_data.get('defect'),
            quantity=validated_data.get('quantity', 0)
        )
        defect_record.created_by = self.context.get('request').user
        defect_record.save()
        return defect_record
    
    def update(self, instance, validated_data):
        instance.employee = validated_data.get('employee', instance.employee)
        instance.defect = validated_data.get('defect', instance.defect)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()
        return instance
    