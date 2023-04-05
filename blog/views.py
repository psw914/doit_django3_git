from django.shortcuts import render
from blog import models
# Create your views here.
def index(request):
    posts = models.Post.objects.all().order_by("-pk")
    return render(
        request,
        "blog/index.html",
        {
          "posts":posts,
        },
        )

def single_post_page(request,pk):
    post = models.Post.objects.get(pk=pk)

    return render(
        request,
        "blog/single_post_page.html",
        {
          "post":post,
        },
        
        )