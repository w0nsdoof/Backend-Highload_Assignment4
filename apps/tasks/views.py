from django.shortcuts import render
from django.http import JsonResponse
from .forms import EmailForm 
from .tasks import send_email_task

def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            send_email_task.delay(email.recipient, email.subject, email.body)
            return JsonResponse({'status': 'Email is being sent in the background!'})
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})
