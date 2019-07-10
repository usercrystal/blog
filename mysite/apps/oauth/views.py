from django.shortcuts import render
from django.contrib.auth import login

from .models import OauthUser

# Create your views here.

GIT_CLIENT_ID = '0c04b60d90a83fefb912'
GIT_CLIENT_SECRET = 'c72f92c5bc30e9e0d4c6232873bb0109ee476fcc'