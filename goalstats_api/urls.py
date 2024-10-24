from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users_auth.views import RegisterView, LoginView, LogoutView, UserListView, UserDetailView,SuperAdminDashboardView, CoachPlayersView, CoachPlayerDetailView, DisciplineViewSet #, AthleteViewSet

router = DefaultRouter()
router.register(r'disciplines', DisciplineViewSet, basename="disciplines")
# router.register(r'athletes', AthleteViewSet, basename="athletes")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),    
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/superadmin/dashboard/', SuperAdminDashboardView.as_view(), name='superadmin-dashboard'),
    path('api/coach/players/', CoachPlayersView.as_view(), name='coach-players'),
    path('api/coach/players/<int:pk>/', CoachPlayerDetailView.as_view(), name='coach-player-detail'),
    # path('api/disciplines/', include(router.urls)),
    # path('api/athletes/', include(router.urls)),
]