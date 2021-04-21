from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ContactForm
from .models import ContactUs


class ContactUsView( View, LoginRequiredMixin ):
    form_class = ContactForm
    template_name = 'contact/contactUs_page.html'

    def get(self, request):
        contact_form = self.form_class()
        context = {'contact_form': contact_form, 'title': 'تماس با ما'}
        return render( request, self.template_name, context )

    def post(self, request):
        contact_form = self.form_class( request.POST or None )
        if contact_form.is_valid():
            username = contact_form.cleaned_data.get( 'user_name' )
            email = contact_form.cleaned_data.get( 'email' )
            title = contact_form.cleaned_data.get( 'title' )
            text = contact_form.cleaned_data.get( 'text' )
            contact = ContactUs()
            contact.user = request.user
            contact.email = email
            contact.title = title
            contact.text = text
            contact.save()
            return redirect( 'home' )
        context = {'contact_form': contact_form, 'title': 'تماس با ما'}
        return render( request, self.template_name, context )
