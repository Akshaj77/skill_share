from django.urls import path
from community import views

urlpatterns = [
    path("skills/", views.SkillListCreateView.as_view(), name="skill-list-create"),
    path("", views.CommunityListCreateView.as_view(), name="community-list-create"),
    path("sessions/", views.SessionView.as_view(), name="session-list-create"),
    path("feedback/", views.FeedbackView.as_view(), name="feedback-list-create"),
    path("members/", views.CommunityMembersView.as_view(), name="community-members"),
]
