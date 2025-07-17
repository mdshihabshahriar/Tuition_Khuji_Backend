from django.urls import path,include
from .import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path('register/', views.UserRegistrationApiView.as_view(),name='register'),
    path('login/',views.UserLoginApiView.as_view(),name='login'),
    path('logout/',views.UserLogoutApiView.as_view(),name='logout'),
    path('active/<uid64>/<token>/',views.activate,name='activate'),
    path('change-password/', views.ChangePasswordView.as_view()),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/<int:pk>/', views.TutorProfileUpdateView.as_view(), name='tutor-profile'),

]
