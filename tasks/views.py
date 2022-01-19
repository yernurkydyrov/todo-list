from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .models import Todo
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = 'todo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = context['todo'].filter(user=self.request.user)
        context['count'] = context['todo'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todo'] = context['todo'].filter(
                title__icontains=search_input)
            context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = 'todo'
    template_name = 'tasks/detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'text', 'complete']
    success_url = reverse_lazy('todo')
    template_name = 'tasks/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'text', 'complete']
    success_url = reverse_lazy('todo')
    template_name = 'tasks/form.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = 'todo'
    success_url = reverse_lazy('todo')


class LoginView(LoginView):
    template_name = 'tasks/login.html'
    fields = '__all__'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('todo')


class RegisterPage(FormView):
    template_name = 'tasks/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todo')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todo')
        return super(RegisterPage, self).get(*args, *kwargs)
