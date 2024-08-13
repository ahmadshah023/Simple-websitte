from django.urls import path
from . import views
from .views import QRCodeAPIView, URLShortenAPIView, BarcodeAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('qr-code', QRCodeAPIView.as_view(), name='qr-code'),
    path('barcode', BarcodeAPIView.as_view(), name='barcode'),
    path('url-shorten', URLShortenAPIView.as_view(), name='url-shorten')
]
