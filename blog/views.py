from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.views.generic import UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import logging


logger = logging.getLogger(__name__)


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-date_posted')
    template_name = 'index.html'
    paginate_by = 9


class PostDetail(View):

    def get(self, request, slug):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-date_posted')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm(),
            }
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-date_posted')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user
            comment_form.instance.user_id = request.user.id
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

        else:
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm(),
            }
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'featured_image']
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user  # Ensure only the post author can delete it

    def get_success_url(self):
        # Redirecting to the blog's home page after a post is deleted
        return reverse_lazy('home')


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'edit_comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'slug': comment.post.slug})


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'slug': comment.post.slug})


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        logger.debug(f"Action received: {self.request.POST.get('action')}")
        post = form.save(commit=False)
        # Assign the user as the author of the post
        post.user = self.request.user
        # Checking the value of the 'action' POST parameter
        action = self.request.POST.get('action', 'Draft')  # Default to 'Draft' if 'action' is not present

        if action == 'Publish':
            post.status = 1  # 1 indicates a published post
        else:  # Default to 'Draft'
            post.status = 0  # 0 indicates a draft post

        post.save()

        # Redirecting to the post's detail view using 'get_absolute_url' method of the Post model
        return HttpResponseRedirect(post.get_absolute_url())


class UserPostsList(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'user_posts.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user, status=1).order_by('-date_posted')
        logger.debug(f"Queryset for user {self.request.user}: {queryset}")
        return queryset


class UserDraftsList(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'user_posts.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user, status=0).order_by('-date_posted')
        logger.debug(f"Queryset for user {self.request.user}: {queryset}")
        return queryset