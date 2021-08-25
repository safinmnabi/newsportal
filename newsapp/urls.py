from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('recover/', views.reset_password, name='recover'),
    path('', views.home, name='home'),
    path('pag/<int:id>', views.pagination, name='pag'),
    path('setting/', views.setting, name='setting'),
    path('mail/', views.recover_email, name='email'),
    path('check/<email>/<token>', views.changepassword, name='check'),
    path('api/', views.api, name='api'),

]