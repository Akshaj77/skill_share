from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from skill_share.authentication import FirebaseAuthentication
from community_post.services.community_post_service import CommunityPostService
from community_post.repositories.community_post_repository import (
    CommunityPostRepository,
)

from user.models import User

communityPostService = CommunityPostService(repository=CommunityPostRepository())


class CommunityPostView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        data = request.data
        data["user"] = request.user.pk
        return Response(
            communityPostService.create_new_community_post(data=data),
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        return Response(
            communityPostService.get_all_community_posts(request=request),
            status=status.HTTP_200_OK,
        )


class CommunityPostDetailView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, pk):
        return Response(communityPostService.get_community_post(pk=pk, request=request))


class CommunityPostCommentView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, pk):
        return Response(
            communityPostService.get_community_post_comments(
                post_pk=pk, request=request
            )
        )
    
class CommunityPostByCommunityView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        community_pk = request.query_params.get('community_pk')
        if not community_pk:
            return Response({"error": "Missing community_pk query parameter"}, status=400)
        return Response(
            communityPostService.get_community_posts_by_community(
                community_pk=community_pk, request=request
            )
        )
    
class SavePostView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        data = request.data
        user = request.user
        post = data.get('post')
        save = data.get('save')
        return Response(
            communityPostService.save_post(post=post, user=user, save=save),
            status=status.HTTP_200_OK,
        )
    
class VotePostView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        data = request.data
        user = request.user
        post = data.get('post')
        value = data.get('value')
        return Response(
            communityPostService.vote_post(post=post, user=user, value=value),
            status=status.HTTP_200_OK,
        )
    
class SavedPostsView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        user = request.user
        return Response(
            communityPostService.get_saved_posts(request=request, user=user),
            status=status.HTTP_200_OK,
        )
    
