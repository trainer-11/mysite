from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile') # 수정 후 다시 마이페이지로 이동
    else:
        form = ProfileForm(instance=profile)

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 글 작성자를 현재 로그인한 유저로 지정
            post.save()
            return redirect('board:post_list')  # 글 목록 페이지로 이동
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'board/post_form.html', 'accounts/profile.html', context)    
