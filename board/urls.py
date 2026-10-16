from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    # 목록 관련 모든 별칭 허용
    path('', views.post_list, name='list'),
    path('post_list/', views.post_list, name='post_list'),
    
    # 글쓰기 관련 모든 별칭 허용
    path('create/', views.post_create, name='create'),
    path('create/', views.post_create, name='post_create'),
    
    # 상세 보기 관련 모든 별칭 허용 (여기서 에러가 났던 'post_detail' 포함)
    path('<int:pk>/', views.board_detail, name='detail'),
    path('<int:pk>/', views.board_detail, name='board_detail'),
    path('<int:pk>/', views.board_detail, name='post_detail'),
    
    # 수정 관련 모든 별칭 허용
    path('<int:pk>/update/', views.post_update, name='update'),
    path('<int:pk>/update/', views.post_update, name='post_update'),
    
    # 삭제 관련 모든 별칭 허용
    path('<int:pk>/delete/', views.post_delete, name='delete'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
]