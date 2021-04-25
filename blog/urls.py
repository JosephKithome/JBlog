from django.urls import path
from .views import *
from django.views import View

urlpatterns = [
    path('',BlogListView.as_view(),name ='home'),
    path('post/<int:pk>/',BlogPostDetailView.as_view(),name = 'post'),
    path('comments/',CommenSectionView.as_view(),name='comments'),
  
]