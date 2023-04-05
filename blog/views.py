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