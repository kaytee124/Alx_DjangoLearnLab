from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserProfileForm, PostForm, CommentForm
from .models import Post, Comment, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from urllib.parse import unquote
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


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10  # Optional: pagination for large result sets

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            # Use Q objects for complex query lookups
            # Search in title, content, and tags (case-insensitive)
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()  # distinct() prevents duplicate results when a post has multiple matching tags
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['search_query'] = query
        context['is_search'] = bool(query)
        return context


class PostByTagListView(ListView):
    """View to display posts filtered by a specific tag"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10

    def get_tag_from_slug(self, tag_slug):
        """Find tag by matching slugified name"""
        from django.utils.text import slugify
        # Get all tags and find the one matching the slug
        tags = Tag.objects.all()
        for tag in tags:
            if slugify(tag.name) == tag_slug:
                return tag
        return None

    def get_queryset(self):
        # Get tag slug from URL parameter
        tag_slug = self.kwargs.get('tag_slug', '')
        # Find tag by matching slugified name
        tag = self.get_tag_from_slug(tag_slug)
        if not tag:
            from django.http import Http404
            raise Http404("Tag not found")
        # Filter posts by tag
        return Post.objects.filter(tags=tag).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get tag slug from URL
        tag_slug = self.kwargs.get('tag_slug', '')
        # Find tag by slug
        tag = self.get_tag_from_slug(tag_slug)
        if tag:
            context['tag'] = tag
            context['tag_name'] = tag.name
            context['tag_slug'] = tag_slug
        else:
            context['tag'] = None
            context['tag_name'] = tag_slug.replace('-', ' ')
            context['tag_slug'] = tag_slug
        context['is_tag_filter'] = True
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        # Support both 'pk' and 'post_id' for flexibility
        post_pk = self.kwargs.get('pk') or self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Support both 'pk' and 'post_id' for flexibility
        post_pk = self.kwargs.get('pk') or self.kwargs.get('post_id')
        return reverse('post_detail', kwargs={'pk': post_pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/post_comment_update.html'
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/post_comment_delete.html'
    context_object_name = 'comment'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
