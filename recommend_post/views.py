from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from community_post.models import CommunityPost, Vote, Comment, SavedPost
from community_post.serializers import CommunityPostListSerializer
from surprise import Dataset, Reader, SVD
import pandas as pd
from user.models import User
from django.http import HttpRequest
import traceback


def generate_interaction_matrix():
    votes = Vote.objects.all().values("user_id", "post_id", "value")
    comments = Comment.objects.all().values("user_id", "post_id")
    saved_posts = SavedPost.objects.all().values("user_id", "post_id")

    data = []

    for vote in votes:
        data.append([vote["user_id"], vote["post_id"], vote["value"]])

    for comment in comments:
        data.append([comment["user_id"], comment["post_id"], 2])

    for save in saved_posts:
        data.append([save["user_id"], save["post_id"], 3])

    df = pd.DataFrame(data, columns=["user_id", "post_id", "interaction"])
    # print(df)

    interaction_matrix = df.pivot_table(
        index="user_id",
        columns="post_id",
        values="interaction",
        fill_value=0,
        aggfunc="sum",
    )
    print(interaction_matrix)

    return interaction_matrix


def prepare_data(interaction_matrix):
    reader = Reader(rating_scale=(-1, 3))
    data = Dataset.load_from_df(interaction_matrix.stack().reset_index(), reader)
    trainset = data.build_full_trainset()
    return trainset


def train_model(trainset):
    model = SVD()
    model.fit(trainset)
    return model


def recommend_posts(model, user_id, interaction_matrix, top_n=2):
    # user_id = '74g82gOrwYRAMd5tu56LQg8pQEs2'  # replace with the actual user_id
    user_ratings = interaction_matrix.loc[user_id]
    user_interactions = {post_id: rating for post_id, rating in user_ratings.items() if rating != 0}
    # user_ratings = interaction_matrix.loc[str(user_id)].values
    # print(user_ratings)
    # user_interactions = {
    #     post_id : rating for post_id, rating in enumerate(user_ratings) if rating != 0
    # }

    print("columns")
    print(interaction_matrix.columns)
    print(user_interactions)
    all_post_ids = set(interaction_matrix.columns)
    seen_post_ids = set(user_interactions.keys())
    unseen_post_ids = list(all_post_ids - seen_post_ids)

    predictions = [model.predict(uid=user_id, iid=post_id) for post_id in unseen_post_ids]
    recommendations = sorted(predictions, key=lambda x: x.est, reverse=True)[:top_n]

    return [rec.iid for rec in recommendations]


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_recommended_posts(request):
    user = User.objects.all().first()
    # print(user)
    # print(user.uid)
    # print(user.email)
    interaction_matrix = generate_interaction_matrix()
    trainset = prepare_data(interaction_matrix)
    model = train_model(trainset)
    try:
        recommended_post_ids = recommend_posts(model, user.uid, interaction_matrix)
        recommended_posts = CommunityPost.objects.filter(id__in=recommended_post_ids)

        fake_request = HttpRequest()
        fake_request.user = "QH98P2w9lxXVl5ZG7rvviAZ23X32"

        serializer = CommunityPostListSerializer(
            recommended_posts,
            many=True,
            context={"request": fake_request},
        )
        return Response(serializer.data)
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {str(e)}")
        # traceback.print_exc()
        return Response([])
