
from django.urls import path
from .views import HomeView, DetailsView, AddPostView, EditPostView, DeletePostView, AddCategoryView, CategoryView, CategoryListView, LikeView, load_more, delete_comment, suggested_post_view, change_suggestion_view

urlpatterns = [


    path('', HomeView.as_view(), name="home"),
    path('article/<slug>', DetailsView.as_view(), name='article-detail'),
    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('article/edit/<slug>', EditPostView.as_view(), name='edit-post'),
    path('article/<slug>/delete', DeletePostView.as_view(), name='delete-post'),
    path('add-category', AddCategoryView.as_view(), name='add-category'),
    path('category/<str:cats>', CategoryView, name='category'),
    path('category-list/', CategoryListView, name='category-list'),
    path('like', LikeView, name="like-post"),
    path('load-more', load_more, name="load-more"),
    path('delete-comment/<int:id>', delete_comment, name="delete-comment"),
    path('suggested-posts', suggested_post_view, name="suggested-posts"),
    path('change-suggestion', change_suggestion_view, name="change-suggestion"),

]
