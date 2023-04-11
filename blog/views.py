# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
# 포스트 수정 페이지
from django.core.exceptions import PermissionDenied
# 작성자의 태그 기능
from django.utils.text import slugify





from blog import models
from blog import forms
# Create your views here.
class PostList(ListView):
    model = models.Post
    # template_name = "blog/index.html"
    # template_name = "blog/post_list.html"
    ordering = "-pk"
    paginate_by = 3

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

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = models.Post
    # fields = forms.PostForm
    form_class = forms.PostForm
    # fields = ["title","hook_text","content","head_image","file_upload","category","tags"]
    # fields = []

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self,form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            # super(PostCreate,self).form_valid(form)
            
            # 작성자의 태그 기능
            response = super(PostCreate,self).form_valid(form)
            tags_str = self.request.POST.get("tags_str")
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(",", "#")
                tags_list = tags_str.split("#")

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = models.Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        
        else:
            return redirect("/blog/")



class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs["q"]
        post_list = models.Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q) | Q(content__contains=q)
        ).distinct()
        return post_list
    
    def get_context_data(self,**kwargs):
        context = super(PostSearch,self).get_context_data()
        q = self.kwargs["q"]
        context["search_info"] = f"Search:{q} ({self.get_queryset().count()})"

        return context
    
# 포스트 수정 페이지
class PostUpdate(LoginRequiredMixin,UpdateView):
    model = models.Post
    form_class = forms.PostForm
    # fields = ['title','hook_text','content','head_image','file_upload','category','tags']
    template_name = "blog/post_update_form.html"

    def get_context_data(self,**kwargs):
        context = super(PostUpdate,self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context["tags_str_default"] = "#".join(tags_str_list)

        return context


    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request,*args,**kwargs)
        else:
            raise PermissionDenied
        
    
    def form_valid(self,form):
        response = super(PostUpdate,self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get("tags_str")
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(",", "#")
            tags_list = tags_str.split("#")

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = models.Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response