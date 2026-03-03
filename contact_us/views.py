from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    form = ContactForm(request.POST or None)
    success = False

    if request.method == "POST" and form.is_valid():
        ContactMessage.objects.create(
            name = form.cleaned_data['name'],
            email = form.cleaned_data['email'],
            message = form.cleaned_data['message']
        )
        success = True
        form = ContactForm()
    return render(request, "contact_us/contact.html", {
        "form": form,
        "success": success
    })