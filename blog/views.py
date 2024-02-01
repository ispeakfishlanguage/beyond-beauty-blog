from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post


# Create your views here.
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-date_posted')
    template_name = 'index.html'
    paginate_by = 10
