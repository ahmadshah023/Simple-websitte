from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import qrcode
from io import BytesIO
from django.http import HttpResponse
import barcode
from barcode.writer import ImageWriter
import pyshorteners



# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken already!')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken already!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords did not match!')
            return redirect('signup')
        return redirect('index')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, '   error !  Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')

def about(request):
    return render(request, 'about.html')

class QRCodeAPIView(APIView):
    def get(self, request, format=None):
        data = request.query_params.get('data', 'No data provided')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')

# Barcode Generation
class BarcodeAPIView(APIView):
    def get(self, request, format=None):
        data = request.query_params.get('data', '123456789012')
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(data, writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')

# URL Shortening
class URLShortenAPIView(APIView):
    def post(self, request, format=None):
        original_url = request.data.get('url')
        if not original_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        shortener = pyshorteners.Shortener()
        shortened_url = shortener.tinyurl.short(original_url)

        # Save to database if needed
        # shortened_instance = ShortenedURL.objects.create(original_url=original_url, shortened_url=shortened_url)

        return Response({"original_url": original_url, "shortened_url": shortened_url}, status=status.HTTP_200_OK)
