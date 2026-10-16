from django.db import models
from django.contrib.auth.models import User  # 👈 1. User 모델 임포트 추가

# Create your models here.

class Post(models.Model):  # 👈 4. 모델 이름은 대문자로 시작 (권장)
    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    # 👈 2. 날짜/시간 필드 설정 수정 (자동 생성 및 갱신)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # 👈 3. def와 __str__ 사이 띄어쓰기 추가
        return self.title