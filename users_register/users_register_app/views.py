from django.shortcuts import render
from users_register_app.forms import UserForm, UserProfileInfoForm
# Necessary classes for the authentication procedure:
from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse <-- deprecated
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'index.html',{})

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users_register_app:index'))

def register(request):
    print('Pase por register!')
    # Define a flag that represent the state of a user as registered or not.
    registered_flag = False
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        user_form = UserForm(request.POST)
        userprofileinfo_form = UserProfileInfoForm(request.POST)

        # Validation: is_valid() return 'True' or 'False'
        if user_form.is_valid() and userprofileinfo_form.is_valid():
            # userdata_object is an instance of class models.User
            userdata_object = user_form.save()
            # Hashing password data
            userdata_object.set_password(userdata_object.password)
            # Saving the changed
            userdata_object.save()
            # Create data object without commit to the data base.
            profiledata_object = userprofileinfo_form.save(commit=False)
             # One To One Relationship in view (in models.py must be specified too)
            profiledata_object.user = userdata_object
            # The client choosed a file or not:
            # profile_pic is a variable in models.py and also is represented
            # as a key in HTTPRequest.FILES
            if 'profile_pic' in request.FILES:
                profiledata_object.profile_pic = request.FILES['profile_pic']
            profiledata_object.save()
            # We pass through all the procedures of registration.
            registered_flag = True
        else:
            print(user_form.errors, userprofileinfo_form.errors)
    else:
        user_form = UserForm()
        userprofileinfo_form = UserProfileInfoForm()
    return render(request, 'registration.html',
                {'user_form':user_form,
                'userprofileinfo_form':userprofileinfo_form,
                'registered_flag':registered_flag})

# Remember that request.POST is a dictionary and also is a python object.
# We can access values by using the directly way ['key_name'] or by the get('key_name')
# method. With get('') method we avoid some error exceptions.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate a user: authenticate(request=None, **credentials)
        # returns a User object if the credentials are valid for a backend.
        # If the credentials aren’t valid for any backend or if a backend raises
        # PermissionDenied, it returns None.
        user_object = authenticate(username=username, password=password)

        if user_object is not None:
            # A backend authenticated the credentials.
            # is_active is a flag.
            if user_object.is_active:
                login(request, user_object)
                return HttpResponseRedirect(reverse('users_register_app:index'))
            else:
                return HttpResponse("Account Not Active")
        else:
            # No backend authenticated the credentials
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'login.html',{})
