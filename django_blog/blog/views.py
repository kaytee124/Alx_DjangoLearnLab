from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserProfileForm, PostForm
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'blog/edit_profile.html', {'form': form})


class ListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class DetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

class CreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/update.html'
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author