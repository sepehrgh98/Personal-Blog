from django.http import HttpResponseRedirect
from django.views import generic
from .forms import TagForm, Post_Category_Form, Post_form, UserForm
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag, User, Post_category, Like, Dislike
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils import timezone
from rest_framework.views import APIView
from .serializers import LikeAndDislikeSerializer
from rest_framework.response import Response
from rest_framework import status
from dal import autocomplete


# final_project page
class IndexView(ListView):
    context_object_name = 'post_list'
    queryset = Post.objects.all()
    template_name = 'blog/index.html'

    # def get_queryset(self):
    #     pass


# register page
def register(request):
    if request.POST:
        user_form = UserForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.last_update = timezone.now()
            user.save()
            # user_form.save()
            return HttpResponseRedirect(reverse('blog:profile', args=(user.pk,)))
        else:
            user_form = UserForm(request.POST, request.FILES)
            return render(request, 'blog/register.html', context={'user_form': user_form})

    else:
        user_form = UserForm()
    return render(request, 'blog/register.html', context={'user_form': user_form})


# profile_view
class Profile(generic.DetailView):
    model = User
    template_name = 'blog/Profile.html'


# post_pre_view
class Post_Pre_View(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog/post_pre_view.html'


# new_post_page
@login_required
def new_Post(request):
    if request.POST:
        post_form = Post_form(request.POST, request.FILES)
        tag_form = TagForm(request.POST)
        # category_form = Post_Category_Form(request.POST)
        if post_form.is_valid() and tag_form.is_valid():
            tag = tag_form.save(commit=False)
            if tag.name not in Tag.objects.values_list('name', flat=True):
                tag.save()
                tag_form.save_m2m()

            # category = category_form.save(commit=False)
            # category.last_update = timezone.now()
            # category.save()
            # category_form.save()

            post = post_form.save(commit=False)
            post.last_update = timezone.now()
            # post.category = category
            post.tag = tag
            post.author = request.user
            post.save()
            # post_form.save()

            return HttpResponseRedirect(reverse('blog:preview', args=(post.id,)))

    else:
        post_form = Post_form()
        tag_form = TagForm()
        category_form = Post_Category_Form()
    return render(request, 'blog/new_post.html', {'post_form': post_form
        , 'tag_form': tag_form
        , 'category_form': category_form})


# category_page
class Categories(LoginRequiredMixin, generic.ListView):
    model = Post_category
    context_object_name = 'category_list'
    form = Post_Category_Form
    template_name = 'blog/categories.html'
    queryset = Post_category.objects.all()


# add like & dislike APIs
class likeAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            p = Post.objects.get(id=data['post_id'])
            for item in p.like_set.all():
                if item.user == request.user:
                    return Response(status=status.HTTP_201_CREATED)
            for item in p.dislike_set.all():
                if request.user == item.user:
                    item.delete()
            Like.objects.create(user=request.user, post=p, state_date=timezone.now())
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UnlikeAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            p = Post.objects.get(id=data['post_id'])
            for item in p.like_set.all():
                if item.user == request.user:
                    item.delete()
                    return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.filter(name__istartswith=self.request.POST['search'])
        print(qs)
        return qs


class dislikeAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            p = Post.objects.get(id=data['post_id'])
            for item in p.dislike_set.all():
                if item.user == request.user:
                    return Response(status=status.HTTP_201_CREATED)
            for item in p.like_set.all():
                if request.user == item.user:
                    item.delete()
            Dislike.objects.create(user=request.user, post=p, state_date=timezone.now())
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UndislikeAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            p = Post.objects.get(id=data['post_id'])
            for item in p.dislike_set.all():
                if item.user == request.user:
                    item.delete()
                    return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# count like & dislike APIs
class LikeAndDislikeCountAPI(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = LikeAndDislikeSerializer(posts, many=True)
        return Response(serializer.data)
