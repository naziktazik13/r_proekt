from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, DetailView, UpdateView 
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, PostForm, ProfileForm, CommentForm
from django.contrib.auth import login 
from django.contrib import messages
from rp import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Profile, Comment, Vote, CommentVote
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views import View

class CustomLoginView(LoginView):
    template_name= "rp/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = "login"

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")

    else:
        form = CustomUserCreationForm()
        messages.error(request, "some error")
    return render(
        request,
        template_name="rp/register.html",
        context={"form": form}
    )

class PostListView(ListView):
    model = Post
    template_name = 'rp/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(status='published') | Post.objects.filter(author=self.request.user)
        else:
            return Post.objects.filter(status='published')

class PostCreateView(CreateView):
    model = models.Post
    form_class = PostForm
    template_name = 'rp/post_create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = models.Post
    success_url = reverse_lazy('post-list')
    template_name = 'rp/post_delete.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'rp/post_detail.html'
    context_object_name = 'post'

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'rp/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'rp/edit_profile.html'
    success_url = reverse_lazy('view_profile')

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'rp/post_edit.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("У вас нет прав на редактирование этого поста.")

class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'rp/add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['post_id']
        form.instance.author = self.request.user
        parent_id = self.request.GET.get('parent') or self.request.POST.get('parent')
        if parent_id:
            form.instance.parent = get_object_or_404(Comment, id=parent_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'rp/edit_comment.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'rp/delete_comment.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().post.pk})

class UserProfileView(DetailView):
    model = User
    template_name = 'rp/user_profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(author=user)
        return context
 
class AddLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        vote, created = Vote.objects.get_or_create(user=request.user, post=post, defaults={'vote': 'like'})
        if not created:
            if vote.vote == 'dislike':
                vote.vote = 'like'
                vote.save()
                post.likes += 1
                post.dislikes -= 1
            else:
                vote.delete()
                post.likes -= 1
        else:
            post.likes += 1
        post.save()
        return redirect('post_detail', pk=pk)

class AddDislikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        vote, created = Vote.objects.get_or_create(user=request.user, post=post, defaults={'vote': 'dislike'})
        if not created:
            if vote.vote == 'like':
                vote.vote = 'dislike'
                vote.save()
                post.likes -= 1
                post.dislikes += 1
            else:
                vote.delete()
                post.dislikes -= 1
        else:
            post.dislikes += 1
        post.save()
        return redirect('post_detail', pk=pk)

class AddCommentLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        vote, created = CommentVote.objects.get_or_create(user=request.user, comment=comment, defaults={'vote': 'like'})
        if not created:
            if vote.vote == 'dislike':
                vote.vote = 'like'
                vote.save()
                comment.likes += 1
                comment.dislikes -= 1
            else:
                vote.delete()
                comment.likes -= 1
        else:
            comment.likes += 1
        comment.save()
        return redirect('post_detail', pk=comment.post.pk)

class AddCommentDislikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        vote, created = CommentVote.objects.get_or_create(user=request.user, comment=comment, defaults={'vote': 'dislike'})
        if not created:
            if vote.vote == 'like':
                vote.vote = 'dislike'
                vote.save()
                comment.likes -= 1
                comment.dislikes += 1
            else:
                vote.delete()
                comment.dislikes -= 1
        else:
            comment.dislikes += 1
        comment.save()
        return redirect('post_detail', pk=comment.post.pk)