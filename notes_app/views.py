from datetime import datetime
from django.contrib.auth.models import User
from django.forms.models import fields_for_model
from django.forms.widgets import Select
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import RegisterForm
from . import models as mod
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
MAX_NOTE_COUNT = 99

# Create your views here.
class RegisterView(FormView):
    template_name = 'notes_app/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        new_setting = mod.Settings(user=user)
        new_setting.save()
        if user:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, request, *args, **kwargs ):
        if request.user.is_authenticated:
            return redirect('notes')

        return super().get(request, *args, **kwargs )


class LoginPageView(LoginView):
    template_name = 'notes_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('notes')

    def post(self, request, *args, **kwargs):
        if self.form_invalid(self.get_form()):
            self.extra_context = {'error': 'Incorrect username or password. Please try again.',}
            
        return super().post(request, *args, **kwargs)


def note_create(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if mod.Note.objects.filter(user=request.user).count() >= MAX_NOTE_COUNT:
        print('TOO MANY NOTES')
        return redirect('notes')

    time_now = datetime.now()
    new_note = mod.Note(user=request.user, title='Untitled Note', create_time=time_now, last_save_time=time_now)
    new_note.save()
    return redirect('note', pk=new_note.pk)


class NoteUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'notes_app/note.html'
    model = mod.Note
    fields = ['title', 'content']
    success_url = reverse_lazy('notes')

    def get(self, request, pk):
        if self.get_object().user != request.user:
            return redirect('notes', permanent=True)
        return super().get(request, pk)
    

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.instance.title == '':
            form.instance.title = 'Untitled Note'

        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.last_save_time = datetime.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_valid(form)


class NoteDelete(LoginRequiredMixin, DeleteView):
    template_name = 'notes_app/note-delete.html'
    model = mod.Note
    context_object_name = 'note'
    success_url = reverse_lazy('notes')

    def get(self, request, pk):
        if self.get_object().user != request.user:
            return redirect('notes')

        return super().get(request, pk)


class NoteList(LoginRequiredMixin, ListView):
    template_name = 'notes_app/notes.html'
    model = mod.Note
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        return context


def index(request):
    return redirect('login', permanent=True)


def light_theme(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    user_settings = mod.Settings.objects.get(pk=request.user)
    user_settings.enabled_dark = False
    user_settings.save()
    return redirect('notes')


def dark_theme(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    user_settings = mod.Settings.objects.get(pk=request.user)
    user_settings.enabled_dark = True
    user_settings.save()
    return redirect('notes')


def error_404(request, *args):
    return render(request, 'notes_app/404.html')


def error_500(request, *args):
    return render(request, 'notes_app/404.html')
    

def error_403(request, *args):
    return render(request, 'notes_app/404.html')


def error_400(request, *args):
    return render(request, 'notes_app/404.html')
