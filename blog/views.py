from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.generic import ListView,DetailView
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from .forms import MusicForm
import pygments
from django.shortcuts import render, get_object_or_404
from . import go_music
import json

# 没修改类视图之前
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self,request,*args,**kwargs):
        response = super(PostDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView,self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',

                                      ]
                                      )
        return post
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',

                                  ]
                                  )
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


# def archives(request, year, month):
#
#     post_list = Post.objects.filter(
#         created_time__year=year,
#         created_time__month=month,
#     )
#
#     return render(request, 'blog/index.html', context={'post_list': post_list})
class ArchivesView(IndexView):
    def get_queryset(self):
        year=self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(created_time__year =year,created_time__month = month)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})
class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 重写父类获取列表的函数，使其具有过滤功能
    def get_queryset(self):
        cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category = cate)

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        # pk是tag和cat都有的主键？
        tag = get_object_or_404(Tag, pk = self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags = tag)

def crawl(request):
    form = MusicForm()
    return render(request, 'blog/go.html', {'form':form})

def crawl_music(request):
    #创建一个表单
    form = MusicForm() ##forms.MusicForm 类
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            mid = form.cleaned_data['mid']
            page = form.cleaned_data['page']
            key = form.cleaned_data['key']
        # 传入歌曲id 和 页数
        cmtlist, topUser, hit, rowTag, topWord = go_music.craw(int(mid), int(page), str(key))
        data = [10, 20, 30, 40, 50]
        print(rowTag)
        return render(request, 'blog/show.html', {'form': form, 'cmtlist':cmtlist,
              'data':json.dumps(data), 'topUser':topUser, 'hit':json.dumps(hit),
            'rowTag':json.dumps(rowTag), 'topWord':json.dumps(topWord)})
    return render(request, 'blog/go.html', {'form':form})