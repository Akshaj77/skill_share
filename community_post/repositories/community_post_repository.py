from user.models import User
from community_post.models import CommunityPost, SavedPost, Vote
from community_post.serializers import (
    CommunityPostSerializer,
    CommunityPostListSerializer,
    CommunityPostDetailSerializer,
    CommentListSerializer,
)


class CommunityPostRepository:
    def create_new_community_post(self, data):
        serializer = CommunityPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_all_community_posts(self, request):
        posts = CommunityPost.objects.all()
        serializer = CommunityPostListSerializer(
            posts, many=True, context={"request": request}
        )
        return serializer.data

    def get_community_post(self, pk, request):
        post = CommunityPost.objects.get(pk=pk)
        serializer = CommunityPostDetailSerializer(post, context={"request": request})
        return serializer.data

    def get_community_post_comments(self, post_pk, request):
        post = CommunityPost.objects.get(pk=post_pk)
        comments = post.comments.all()
        serializer = CommentListSerializer(
            comments, many=True, context={"request": request}
        )
        return serializer.data

    def get_community_posts_by_community(self, community_pk, request):
        posts = CommunityPost.objects.filter(community=community_pk)
        serializer = CommunityPostListSerializer(
            posts, many=True, context={"request": request}
        )
        return serializer.data

    def save_post(self, post, user, save=True):
        post = CommunityPost.objects.get(pk=post)
        if save:
            SavedPost.objects.create(user=user, post=post)
        else:
            SavedPost.objects.filter(user=user, post=post).delete()

    def vote_post(self, post, user, value):
        vote = Vote.objects.filter(user=user, post=post).first()
        post = CommunityPost.objects.get(pk=post)
        if vote:
            vote.value = value
            if value == 0:
                vote.delete()
                return
            vote.save()
        else:
            Vote.objects.create(user=user, post=post, value=value)

    def get_saved_posts(self, request, user):
        saved_posts = SavedPost.objects.filter(user=user)
        posts = [saved_post.post for saved_post in saved_posts]
        serializer = CommunityPostListSerializer(
            posts, many=True, context={"request": request}
        )
        return serializer.data
