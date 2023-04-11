from django.urls import path
from . import views

urlpatterns = [
    path("",views.PostList.as_view()),
    # path("",views.index),
    path("<int:pk>/",views.PostDetail.as_view()),
    # path("<int:pk>/",views.single_post_page),
    path("category/<str:slug>/",views.category_page),
    path("tag/<str:slug>/",views.tag_page),
    path("create_post/",views.PostCreate.as_view()),

    path("search/<str:q>/", views.PostSearch.as_view()),
    path("update_post/<int:pk>/",views.PostUpdate.as_view()),  # 포스트 수정 페이지
    path("<int:pk>/new_comment/", views.new_comment),  # 댓글 작성 양식
    path("update_comment/<int:pk>/", views.CommentUpdate.as_view()),  # 댓글 수정
]