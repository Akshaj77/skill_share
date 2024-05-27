from django.db import models
import uuid


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


# can a community have many skills ?
class Community(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    members = models.ManyToManyField("user.User", through="Membership")
    description = models.TextField(blank=True,null=True)
    banner = models.ImageField(upload_to="community/banner/")
    profile_image = models.ImageField(upload_to="community/profile_image/")

    def __str__(self) -> str:
        return f"{self.name} - {self.skill}"


class Membership(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE,related_name="memberships")
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)


class Badge(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField()


# date can be scheduled so not auto_now
class Session(models.Model):
    channel_id = models.UUIDField(default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=False,null=False)
    description = models.TextField(blank=False,null=False)
    duration = models.IntegerField()


class Feedback(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()


# not for specific skill
class TimeBank(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    hours_spent = models.IntegerField()
    # can add skill if specific


# why is community not many to many here
class Project(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    members = models.ManyToManyField("user.User")
    description = models.TextField()
