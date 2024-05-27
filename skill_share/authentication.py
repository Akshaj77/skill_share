from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from firebase_admin import auth

from user.services.user_service import UserService
from user.repositories.user_repository import UserRepository


class FirebaseAuthentication(BaseAuthentication):
    def __init__(self) -> None:
        self.user_service = UserService(repository=UserRepository())
        super().__init__()

    keyword = "Token"

    def authenticate_header(self, request):
        return self.keyword

    def authenticate(self, request):
        id_token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        # print("id_token: ")
        print(id_token)

        if not id_token:
            return None

        try:
            decoded_token = auth.verify_id_token(id_token=id_token)
            # print(decoded_token)
            uid = decoded_token["uid"]

            user = self.user_service.get_user_from_firebase_uid(uid=uid)
            return (user, decoded_token)
            # if user is not None:
            #     return user
            # else:  # redundant??
            #     raise AuthenticationFailed('User not found')
        except auth.InvalidIdTokenError:
            raise AuthenticationFailed("Invalid ID token")
