from rest_framework import serializers
from community_post.models import CommunityPost, Vote, Comment, CommentVote, SavedPost
from user.serializers import UserSerializer
from community.serializers import CommunityListSerializer


class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = "__all__"


class CommunityPostListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all community posts
    """

    user = UserSerializer(read_only=True)
    community = CommunityListSerializer(read_only=True)

    score = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()
    # detail_url = serializers.HyperlinkedIdentityField(
    #     view_name="community-post-detail",
    #     lookup_field="pk",
    #     lookup_url_kwarg="pk",
    # )

    class Meta:
        model = CommunityPost
        fields = "__all__"

    def get_score(self, obj):
        return obj.score()

    def get_vote(self, obj):
        user = self.context["request"].user
        vote = Vote.objects.filter(post=obj, user=user).first()
        if vote:
            return vote.value
        return None


class CommunityPostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all community posts
    """

    user = UserSerializer(read_only=True)
    community = CommunityListSerializer(read_only=True)

    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()

    class Meta:
        model = CommunityPost
        fields = "__all__"

    def get_upvotes(self, obj):
        return obj.upvotes()

    def get_downvotes(self, obj):
        return obj.downvotes()

    def get_score(self, obj):
        return obj.score()

    def get_is_saved(self, obj):
        user = self.context["request"].user
        return SavedPost.objects.filter(post=obj, user=user).exists()

    def get_vote(self, obj):
        user = self.context["request"].user
        vote = Vote.objects.filter(post=obj, user=user).first()
        if vote:
            return vote.value
        return None


class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_upvotes(self, obj):
        return obj.upvotes()

    def get_downvotes(self, obj):
        return obj.downvotes()

    def get_score(self, obj):
        return obj.score()

    def get_vote(self, obj):
        user = self.context["request"].user
        vote = CommentVote.objects.filter(comment=obj, user=user).first()
        if vote:
            return vote.value
        return None
