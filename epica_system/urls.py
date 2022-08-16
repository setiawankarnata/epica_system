from django.contrib.auth.urls import *
from django.contrib.auth.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),
    path('accounts/password_change/done/',
         PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('accounts/password_reset/done/',
         PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', users_views.home, name='home'),
    path('users/', include('users.urls')),
    path('pica/', include('pica.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
