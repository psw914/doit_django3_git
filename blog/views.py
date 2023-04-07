# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import render


from blog import models
# Create your views here.
class PostList(ListView):
    model = models.Post
    # template_name = "blog/index.html"
    # template_name = "blog/post_list.html"
    ordering = "-pk"

    def get_context_data(self,**kwargs):
        context = super(PostList,self).get_context_data()
        context["categories"] = models.Category.objects.all()
        context["no_cgy"] = models.Post.objects.filter(category=None).count()

        return context 

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

    def get_context_data(self,**kwargs):
        context = super(PostDetail,self).get_context_data()
        context["categories"] = models.Category.objects.all()
        context["no_cgy"] = models.Post.objects.filter(category=None).count()

        return context 
# def single_post_page(request,pk):
#     post = models.Post.objects.get(pk=pk)

#     return render(
#         request,
#         "blog/single_post_page.html",
#         {
#           "post":post,
#         },
        
#         )

def category_page(request,slug):
    if slug == "no_category":
        category = "미분류"
        post_list = models.Post.objects.filter(category=None)
    else:
        category = models.Category.objects.get(slug=slug)
        post_list = models.Post.objects.filter(category=category)

    
    

    return render(
        request,
        "blog/post_list.html",
        {
            # "post_list":models.Post.objects.filter(category=category),
            "post_list":post_list,
            "categories":models.Category.objects.all(),
            "no_cgy":models.Post.objects.filter(category=None).count(),
            "category":category,
        },
    )