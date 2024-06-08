from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.admin import PostViewSet, CommentViewSet, VoteViewSet, GalleryViewSet


app_name = "blog-admin"

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'galleries', GalleryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
