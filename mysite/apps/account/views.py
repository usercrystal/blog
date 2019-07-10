from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm

from .forms import RegistrationForm, UserProfileForm

# Create your views here.

# class UserLogin(View):
#
#     def get(self, request):
#         login_form = LoginForm()
#         return render(request, "account/login.html", {"form": login_form})
#
#     def post(self, request):
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             login_data = login_form.cleaned_data
#             user_auth = authenticate(username=login_data["username"], password=login_data["password"])
#             if user_auth:
#                 login(request, user_auth)
#                 return HttpResponse("Welcome!")
#             else:
#                 return HttpResponse("Your username or password is not right.")
#         else:
#             return HttpResponse("Invalid login")


class Register(View):

    def get(self, request):
        user_info = RegistrationForm()
        user_profile = UserProfileForm()
        return render(request, 'account/register.html', {'form': user_info, 'profile': user_profile})

    def post(self, request):
        user_info = RegistrationForm(request.POST)
        user_profile = UserProfileForm(request.POST)
        if user_info.is_valid() and user_profile.is_valid():
            # temp = user_info
            # User.objects.create(username=temp['username'],
            #                     email=temp['email'],
            #                     password=temp['password'])
            new_user = user_info.save(commit=False)
            new_user.set_password(user_info.cleaned_data['password'])
            new_user.save()
            new_profile = user_profile.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponseRedirect(reverse('user_login'))
        else:
            return HttpResponse('You can not register!')
