
from django.urls import path
from django.conf.urls import url
from .views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    url(r'^signup/$', views.signup, name='signup'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate, name='activate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit-profile/', UserEditView.as_view(), name='edit-profile'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password-success', views.password_success, name="password-success"),
    path('<int:pk>/profile', ShowProfilePageView.as_view(), name="show-profile"),
    path('<int:pk>/edit-profile-page',
         EditProfilePageView.as_view(), name="edit-profile-page"),
    path('create-profile-page', CreateProfilePageView.as_view(),
         name="create-profile-page"),

]
