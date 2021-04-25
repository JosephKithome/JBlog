from django.core.checks import messages
from django.shortcuts import render,redirect
from .models import Post,Comments
from django.views import View
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


# class BlogListView(ListView):
#     # model =Post
#     template_name = "home.html"
# @login_required(login_url="authentication/login")
class BlogListView(View):
    def get(self,request):
        posts =Post.objects.all()
        comment=Comments.objects.filter(owner=request.user)
        context ={
            'posts':posts,
            'comments':comment
        }

        return render(request,"home.html",context)

class BlogPostDetailView(DetailView):
    model = Post
    template_name = "blogPost.html"  


# @login_required(login_url="authentication/login")
class CommenSectionView(ListView):
    def get(self,request):
        return render(request,"comments.html")
    def post(self,request):
        comment = request.POST['comment']
        date = request.POST['date']

        if not comment:
            messages.error(request,"Please add a comment")
            return render(request,"comments.html")
        if not date:
            messages.error(request,"Date field cannot be empty")
            return render(request,"comments.html")    
        Comments.objects.create(comment=comment, date=date,owner =request.user)
        messages.success(request,"Your comment was posted")
        return redirect('home')