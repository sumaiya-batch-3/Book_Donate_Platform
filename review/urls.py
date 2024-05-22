from django.urls import path
from .views import PlatformCommentView

urlpatterns = [
    path('platform', PlatformCommentView.as_view(), name='platform_comments'),
    
]
