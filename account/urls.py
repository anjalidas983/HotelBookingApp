from . import views
from django.urls import path
app_name = "account"

urlpatterns = [
    path('user-registration/', views.registration_view, name='user-register'),
    path('login/', views.login_view, name='user_login'),
    # path('login/<slug:redir_url>/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
