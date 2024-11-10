"""
URL configuration for Unity_Workers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('client_form/',views.client_form,name='client_form'),
    path('home_page/',views.home_page,name='home_page'),
    path('worker_login_page/',views.worker_login_page,name='worker_login_page'),
    path('worker_registration_form/',views.worker_registration_form,name='worker_registration_form'),
    path('logout/', views.logout_view, name='logout'),
    path('username/<str:username>/',views.username,name='username'),
    path('contract_form/',views.contract_form,name='contract_form'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('cashfree/payment/success/', views.payment_success, name='payment_success'),
    path('cashfree/payment/failure/', views.payment_failure, name='payment_failure'),
    path('worker_number/',views.worker_number,name='worker_number'),
    path('payment_page',views.payment_page,name='payment_page'),
    path('rapid_service/',views.rapid_service,name='rapid_service')

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)