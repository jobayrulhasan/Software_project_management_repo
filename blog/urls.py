from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
     # customer registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='userregistration'),
    # login
    path('accounts/login/', views.user_login, name='loginpage'),
    # logout
    path('account/logout/', views.user_logout, name='userLogout'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
