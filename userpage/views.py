from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Post, Profile, Like, Following, Comment
from django.contrib.auth.models import User
import json


# Create your views here.
def userHome(request):
    user= Following.objects.get(user= request.user)
    followed_user= user.followed.all()
    posts = Post.objects.filter(user__in = followed_user).order_by('-pk')
    liked_post=[]
    com=[]
    commented_post=[]
    for i in posts:
        is_liked=Like.objects.filter(post=i, like_user=request.user)
        if is_liked:
            liked_post.append(i)
        comment_obj = Comment.objects.filter(post=i)
        if comment_obj:

            for k in comment_obj:
                commented_post.append(i.id)
                #print(commented_post)
                com.append(k)

    data = {
        'posts': posts,
        'liked_post': liked_post,
        'com': com,
        'commented_to': commented_post
    }

    return render(request, 'userpage/postField.html', data)


def addPost(request):
    if request.method == "POST":
        image_ = request.FILES['image']
        captions_ = request.POST.get('caption', '')
        user_ = request.user
        print(user_, captions_, image_)

        post_obj = Post(user=user_, caption=captions_, image=image_)
        post_obj.save()
        messages.success(request, "Posted Successfully!")
        return redirect('/userpage')
    else:
        messages.error(request, "Retry to post! Something went wrong.")
        return redirect('/userpage')


def delPost(request, postId):
    post_ = Post.objects.filter(pk=postId)
    image_path = post_[0].image.url  # image loc
    post_.delete()
    # os.remove(image_path)
    messages.info(request, 'Post deleted')

    return redirect('/userpage')


def userProfile(request, username):
    user = User.objects.filter(username=username)
    if user:
        user=user[0]
        profile = Profile.objects.get(user=user)
        post=getPosts(user)
        bio = profile.bio
        conn = profile.connection
        user_img=profile.image
        is_following=Following.objects.filter(user=request.user, followed=user)
        following_obj=Following.objects.get(user=user)
        follower, following=following_obj.follower.count(), following_obj.followed.count()
        data = {'username': user,
                'bio': bio,
                'conn': conn,
                'follower': follower,
                'following': following,
                'posts': post,
                'userImg': user_img,
                'connection': is_following}
    else:
        messages.error(request,'No such user exists')
        return redirect('/userpage')

    return render(request, 'userpage/userProfile.html', data)

def getPosts(user):
    post_obj=Post.objects.filter(user=user)
    imgList=[
        post_obj[i:i+3] for i in range(0, len(post_obj), 3)
    ]
    return imgList

def likePost(request):
    post_id= request.GET.get("likeID","")
    post=Post.objects.get(pk=post_id)
    user=request.user

    like=Like.objects.filter(post=post, like_user=user)
    #print(like)
    liked=False
    if like:
        Like.dislike(post, user)
        #print("disliked", like[0].like_user)
    else:
        liked=True
        Like.like(post, user)
        #print("liked", like[0].like_user)

    resp={
        'liked': liked,
    }
    response= json.dumps(resp)

    return HttpResponse(response, content_type="application/json")

def comment(request):
    comment_=request.GET.get('comment','')
    id_=request.GET.get('poster','')
    id_=id_[3:]

    post_obj= Post.objects.filter(pk=id_)[0]
    comment_obj=Comment(user=request.user, post= post_obj, comment=comment_)
    print(comment_,post_obj, request.user)
    comment_obj.save()
    return redirect('/userpage')

def follow(request, username):
    main_user=request.user
    to_follow=User.objects.get(username=username)

    following=Following.objects.filter(user=main_user, followed=to_follow)
    is_following=True if following else False
    if is_following:
        Following.unfollow(main_user, to_follow)
        is_following=False
    else:
        Following.follow(main_user, to_follow)
        is_following=True
    resp={
         "following": is_following,
     }
    response=json.dumps(resp)
    return HttpResponse(response,content_type="application/json")

def search(request):
    global searched
    query=request.GET.get('search_bar', '')
    allUser = User.objects.values('username')
    #print(allUser)
    users = {item['username'] for item in allUser}
    #print(users)
    searched=[]
    profiles=[]
    for user1 in users:
        prodtemp = User.objects.filter(username=user1)
        for item in prodtemp:
            if searchMatch(query, item):
                searched.append(item)

    if searched:

            for item in searched:

                profal = Profile.objects.filter(user_id=item.id)

                profiles.append(profal[0])
            #print(searched[0].username)
            '''for j in profiles:
                j.user=str(j.user)
            for i in searched:
                i.username = str(i.username)
                print(j.user)'''

            return render(request, 'userpage/search.html', {'context': searched, 'profile': profiles})

    messages.error(request, 'no such user was found')
    return redirect('/userpage')


def searchMatch(query, item):

    if query in item.username:
        return True
    else:
        return False

