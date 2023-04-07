# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


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



# 방법1
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


# 방법2
# def category_page2(request, slug):
#     category = models.Category.objects.get(slug=slug)
#     context = {
#         "post_list":models.Post.objects.filter(category=category),
#         "categories":models.Category.objects.all(),
#         "no_cgy":models.Post.objects.filter(category=None).count(),
#         "category":category,
#     }
#     return render(
#         request,
#         "blog/post_list.html",
#         context
#     )

def tag_page(request,slug):
    tag = models.Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list":post_list,
            "tag":tag,
            "categories":models.Category.objects.all(),
            "no_cgy":models.Post.objects.filter(category=None).count(),
        },
    )

class PostCreate(LoginRequiredMixin,CreateView):
    model = models.Post
    fields = ["title","hook_text","content","head_image","file_upload","category"]

    def form_valid(self,form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect("/blog")
