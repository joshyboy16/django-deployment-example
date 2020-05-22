from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    is_registered = False

    if request.method == 'POST':

        # grab the information off both forms...
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if both forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            # grab everything form the base user form
            user = user_form.save()
            # hash the password
            user.set_password(user.password)
            # save all information
            user.save()

            # grab the profile form dont save yet, as we will double check if there is a picture or not
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            is_registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'is_registered': is_registered,
                   })


def user_login(request):

    if request.method == 'POST':
        # this looks in the request.POST pathway... which will be coming from
        # the login.html file there is a variable name="username" .get('username')
        # looks for it's value
        username = request.POST.get('username')
        password = request.POST.get('password')

        # django completes the authentication for you here based on user name and password..
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")

        else:
            print("someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied")

    else:
        return render(request, 'basic_app/login.html', {})
