from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
   

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    md = markdown.Markdown(extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
                ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul></div>',md.toc,re.S)
    post.toc = md.toc
    # m.group(1) if m is not None else ''
    return render(request,'blog/detail.html',context={'post':post})

def archive(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
            created_time__month=month,
            ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request,pk):
    cat = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cat).order_by('-created_time')
    return render(reques,'blog/index.html',context={'post_list':post_list})

def tag(request,pk):
    t=get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
