from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from .models import Post

# Create your views here.

def post_list(request):
    post_list = Post.publish.all()
    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page_number n'est pas un nombre entier, récupérer la première page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request,'blog/post/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    # post=Post.objects.get(id=id)
    post=get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        published__year=year,
        published__month=month,
        published__day=day,
    )
    return render(request,'blog/post/detail.html',{'post':post})
