# from django.shortcuts import render
from django.views.generic import ListView, DetailView



from blog import models
# Create your views here.
class PostList(ListView):
    model = models.Post
    template_name = "blog/index.html"
    ordering = "-pk"



# def index(request):
#     posts = models.Post.objects.all().order_by("-pk")
#     return render(
#         request,
#         "blog/index.html",
#         {
#           "posts":posts,
#         },
#         )

class PostDetail(DetailView):
    model = models.Post


# def single_post_page(request,pk):
#     post = models.Post.objects.get(pk=pk)

#     return render(
#         request,
#         "blog/single_post_page.html",
#         {
#           "post":post,
#         },
        
#         )