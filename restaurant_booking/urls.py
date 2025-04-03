from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from booking import views as booking_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', booking_views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


