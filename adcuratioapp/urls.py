from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/blog/<uuid:blog_id>/', views.BlogView.as_view(), name='blog'),
    path('api/blog/', views.BlogView.as_view(), name='blog'),
]