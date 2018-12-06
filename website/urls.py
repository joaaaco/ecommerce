from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import LoginView, LogoutView
from django.conf.urls import handler404

urlpatterns = [
    path('', LoginView.as_view(), name="panel-login"),
    path('home/', views.home, name='home'),
    path('product/<int:pk>/', views.product, name='product'),
    path('chart/user/<int:pk>/', views.chart, name='chart'),
    path('chart-admin/', views.chart_admin, name='chart_admin'),
    path('logout/', LogoutView.as_view(), name="panel-logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
