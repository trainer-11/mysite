from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    category_slug = request.GET.get('category')
    posts = Post.objects.all().order_by('-created_at')
    current_category = None
    
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=current_category)
        
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'board/post_list.html', context)

def board_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,  # 👇 [필수] context에 반드시 담아주어야 합니다!
    }
    return render(request, 'board/board_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            category_id = request.POST.get('category')
            if category_id:
                post.category = get_object_or_404(Category, pk=category_id)
                
            post.save()
            return redirect('board:detail', pk=post.pk)
    else:
        form = PostForm()
        
    categories = Category.objects.all()
    # 👇 핵심: 'form'을 context에 반드시 포함해야 합니다!
    context = {
        'form': form,
        'categories': categories,
        'page_title': '글쓰기'
    }
    return render(request, 'board/post_form.html', context)

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('board:detail', pk=pk)
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            category_id = request.POST.get('category')
            if category_id:
                post.category = get_object_or_404(Category, pk=category_id)
                
            post.save()
            return redirect('board:detail', pk=pk)
    else:
        form = PostForm(instance=post)
        
    categories = Category.objects.all()
    # 👇 수정 뷰에서도 올바른 form 객체를 전달합니다.
    context = {
        'form': form,
        'categories': categories,
        'page_title': '글 수정'
    }
    return render(request, 'board/post_form.html', context)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('board:post_list')

@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        else:
            # 👇 유효성 검사 실패 시 터미널에 에러 원인 출력
            print("댓글 폼 에러:", form.errors)    
            return redirect('board:detail', pk=post.pk)
    
    # 만약 잘못된 접근이라면 상세 페이지로 돌려보냄
    return redirect('board:detail', pk=post.pk)