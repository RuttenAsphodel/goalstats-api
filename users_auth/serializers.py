from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser, Discipline #, Athlete

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

# class AthleteSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     disciplinas = DisciplineSerializer(many=True, read_only=True)

#     class Meta:
#         model = Athlete
#         fields = '__all__'
