from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import note
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('notes')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes')
        return super(RegisterPage, self).get(*args, **kwargs)


class noteList(LoginRequiredMixin, ListView):
    model = note
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['count'] = context['notes'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['notes'] = context['notes'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class noteDetail(LoginRequiredMixin, DetailView):
    model = note
    context_object_name = 'note'
    template_name = 'base/note.html'


class noteCreate(LoginRequiredMixin, CreateView):
    model = note
    fields = ['title', 'description']
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(noteCreate, self).form_valid(form)


class noteUpdate(LoginRequiredMixin, UpdateView):
    model = note
    fields = ['title', 'description']
    success_url = reverse_lazy('notes')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = note
    context_object_name = 'note'
    success_url = reverse_lazy('notes')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class noteReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_note_order(positionList)

        return redirect(reverse_lazy('notes'))
