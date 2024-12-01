from rest_framework import viewsets
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, DisciplineSerializer, UpdateCustomUserSerializer, UserListSerializer, PerformanceMetricSerializer # AthleteSerializer
from .models import CustomUser, Discipline, PerformanceMetric #, Athlete
from .permissions import IsSuperAdmin, IsAdmin, IsCoach

# Vistas de Administrador
class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []
    # Dar informacion del rol del usuario que esta iniciando sesion
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}) 
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = []

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = []

class UpdateUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = []
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateCustomUserSerializer
        return UserListSerializer    
# Vistas de Superadministrador
class SuperAdminDashboardView(APIView):
    permission_classes = []

    def get(self, request):
        total_users = CustomUser.objects.count()
        users_by_role = {
            'super_admin': CustomUser.objects.filter(role='SUPER_ADMIN').count(),
            'admin': CustomUser.objects.filter(role='ADMIN').count(),
            'coach': CustomUser.objects.filter(role='COACH').count(),
            'player': CustomUser.objects.filter(role='PLAYER').count(),
        }
        return Response({
            'total_users': total_users,
            'users_by_role': users_by_role
        })

# Vistas de Entrenador
class CoachPlayersView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        return CustomUser.objects.filter(role='PLAYER')

    def perform_create(self, serializer):
        serializer.save(role='PLAYER')

class CoachPlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='PLAYER')
    serializer_class = UserSerializer
    permission_classes = []
    


# Vistas de Disciplinas
class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = []

# Vistas de Rendimientos de Jugadores
class PerformanceMetricViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer
    permission_classes = []
    
    def perform_create(self, serializer):
        metric = serializer.save()
        metric.calculate_performance_score()
        metric.determine_optimal_position()
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         return PerformanceMetric.objects.all()
    #     return PerformanceMetric.objects.filter(athlete=user)
    
# Vistas de Atletas
# class AthleteViewSet(viewsets.ModelViewSet):
#     queryset = Athlete.objects.all()
#     serializer_class = AthleteSerializer
#     permission_classes = []

#     def perform_create(self, serializer):
#         user = CustomUser.objects.create_user(
#             username=self.request.data.get('username'),
#             password=self.request.data.get('password'),
#             email=self.request.data.get('email'),
#             role='PLAYER'
#         )
#         serializer.save(user=user)
