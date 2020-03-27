from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, View
from django.conf import settings

from account.models import User, Contact, ActivationCode
from account.tasks import send_email_async
from account.forms import SignUpForm


def smoke(request):
    return HttpResponse('smoke')


# def my_profile(request):
#     return render(request, 'my_profile.html')


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email', )
    success_url = reverse_lazy('index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)


class ContactUS(CreateView):
    model = Contact
    fields = ('email', 'title', 'body')
    template_name = 'contact_us.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        subject = form.instance.title
        message = form.instance.body
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]  # send e-mail to our own address
        send_email_async.delay(subject, message, from_email, recipient_list)
        return super().form_valid(form)


class SignUpView(CreateView):
    template_name = 'SignUP.html'
    queryset = Contact.objects.all()
    success_url = reverse_lazy('index')
    form_class = SignUpForm


class Activate(View):
    def get(self, request, activation_code):
        ac = get_object_or_404(ActivationCode.objects.select_related('user'),
                               code=activation_code, is_activated=False)

        if ac.is_expired:
            raise Http404

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')
