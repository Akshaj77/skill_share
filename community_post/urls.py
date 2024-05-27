from django.urls import path
from community_post import views

urlpatterns = [
    path("", views.CommunityPostView.as_view(), name="community-post-view"),
    path(
        "<int:pk>/",
        views.CommunityPostDetailView.as_view(),
        name="community-detail-view",
    ),
    path(
        "<int:pk>/comments/",
        views.CommunityPostCommentView.as_view(),
        name="community-comment-view",
    ),
    path(
        "community/",
        views.CommunityPostByCommunityView.as_view(),
        name="community-post-by-community-view",
    ),
    path(
        "save/",
        views.SavePostView.as_view(),
        name="save-post-view",
    ),
    path(
        "vote/",
        views.VotePostView.as_view(),
        name="vote-post-view",
    ),
    path(
        "saved/",
        views.SavedPostsView.as_view(),
        name="saved-posts-view",
    ),
]
