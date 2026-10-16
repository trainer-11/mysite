from django.db import models
from django.contrib.auth.models import User

# 1. 게시판 카테고리 모델 추가
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="게시판 이름")
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True, verbose_name="URL 슬러그")

    def __str__(self):
        return self.name

# 2. 기존 Post 모델에 카테고리 연결
class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="소속 게시판", null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return self.title