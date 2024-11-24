from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from ..models import OTP
from django.http import HttpResponse

#TODO: change it
@login_required
def dashboard(request):
    if not request.session.get('2fa_verified'):
        return redirect('authentication:2fa-verify')
    return HttpResponse("Welcome to your dashboard!")

def user_login(request):
    """Log in the user and send OTP if 2FA is enabled."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.two_factor_enabled:
                otp = OTP.generate_code(user)

                send_mail(
                    'Backend HighLoad - 2FA Code',
                    f'Your authentication code is {otp.code}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                return redirect('authentication:2fa-verify')
            else:
                return redirect('authentication:dashboard') # TODO: change it
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def two_factor_verify(request):
    """Verify the OTP code entered by the user."""
    if request.method == 'POST':
        code = request.POST.get('code')
        user = request.user

        try:
            otp = OTP.objects.filter(user=user).latest('created_at')

            # Check if OTP is expired
            if otp.is_expired():
                otp.delete()
                return render(request, 'two_factor_verify.html', {'error': 'The code has expired. Please log in again.'})

            # Check if OTP code matches
            if otp.code == code:
                request.session['2fa_verified'] = True
                otp.delete()
                return redirect('authentication:dashboard')
            else:
                return render(request, 'two_factor_verify.html', {'error': 'Invalid code'})
        except OTP.DoesNotExist:
            return render(request, 'two_factor_verify.html', {'error': 'No OTP found. Please log in again.'})

    return render(request, 'two_factor_verify.html')