from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ProfileForm

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
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('accounts:profile') # 수정 후 다시 마이페이지로 이동
    else:
        form = ProfileForm(instance=profile)
    
    context = {'form': form}
    # 👇 [필수] GET 요청이든, 유효성 검사 실패든 함수 끝에서는 반드시 렌더링 결과를 반환해야 합니다!
    return render(request, 'accounts/profile.html', context)