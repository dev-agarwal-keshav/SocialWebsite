from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="user_image/Post", blank=True)

    def __str__(self):
        return str(self.user) + " " + str(self.date)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_image/Profile", default="user_image/Profile/default.png")
    bio = models.CharField(max_length=100, blank=True)
    connection = models.CharField(max_length=200, blank=True)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


class Like(models.Model):
    like_user = models.ManyToManyField(User, related_name="likingUser")
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    # liking post
    @classmethod
    def like(cls, post, liking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.like_user.add(liking_user)

    # disliking post
    @classmethod
    def dislike(cls, post, disliking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.like_user.remove(disliking_user)

    def __str__(self):
        return str(self.post)


class Following(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    followed=models.ManyToManyField(User, related_name="followed")
    follower=models.ManyToManyField(User, related_name="follower")

    @classmethod
    def follow(cls, user, another_account):
        obj, create=cls.objects.get_or_create(user=user)
        obj.followed.add(another_account)
        #print("followed")

    @classmethod
    def unfollow(cls, user, another_account):
        obj, create=cls.objects.get_or_create(user=user)
        obj.followed.remove(another_account)
        #print("unfollowed")

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.CharField(max_length=500)
    post_on= models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.post)


