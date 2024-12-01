from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser, Discipline, PerformanceMetric #, Athlete

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'role', 'is_active')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','role', 'is_active', 'nombre', 'apellido', 'fecha_nacimiento', 'peso', 'estatura', 'nombre_disciplina']
    
class UpdateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role', 'is_active', 'nombre', 'apellido', 'fecha_nacimiento', 'peso', 'estatura', 'nombre_disciplina']

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'

class PerformanceMetricSerializer(serializers.ModelSerializer):
    athlete_name = serializers.CharField(source='CustomUser.username', read_only=True)
    sport_name = serializers.CharField(source='Discipline.nombre_disciplina', read_only=True)

    class Meta:
        model = PerformanceMetric
        fields = '__all__'
        read_only_fields = ['suggested_position', 'performance_score']