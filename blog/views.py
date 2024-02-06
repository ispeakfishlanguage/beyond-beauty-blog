from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-date_posted')
    template_name = 'index.html'
    paginate_by = 10


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
