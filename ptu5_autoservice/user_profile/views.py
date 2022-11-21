from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.validators import validate_email


# Create your views here.
User = get_user_model()

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        error = False

        if not username or User.objects.filter(username=username).first():
            messages.error(request, 'WARNING: username is missing or username is exists')
            error = True

        if not email or User.objects.filter(email=email).first():
            messages.error(request, 'WARNING: email is missing or email is exists')
            error = True
        else:
            try:
                validate_email(email)
            except:
                messages.error(request, 'WARNING: invalid email')

        if not password or not password2 or password != password2:
            messages.error(request, "WARNING: password is missing or not same")
            error = True

        if not error:
            # sukuriam useri
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'CONGRATULATIONS:  user:{username} registration successfull. You can log in now')
            return redirect('login')


    return render(request, 'user_profile/register.html')
    

