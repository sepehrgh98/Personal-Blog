from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from .forms import TagForm, Post_Category_Form, Post_form, UserForm
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag, User, Post_category, Like
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from dal import autocomplete
from rest_framework.views import APIView
from .serializers import likeSerializer
from rest_framework.response import Response
from rest_framework import status


# main page
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


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.filter(name__istartswith=self.request.POST['search'])
        print(qs)
        return qs


# category_page
class Categories(LoginRequiredMixin, generic.ListView):
    model = Post_category
    context_object_name = 'category_list'
    form = Post_Category_Form
    template_name = 'blog/categories.html'
    queryset = Post_category.objects.all()


# like & dislike APIs
class likeAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            # print(f"<<<<<<<<<<<<<<<<{data}")
            p = Post.objects.get(id=data['post_id'])
            print(f"<<<<<<<<<<<<<<<<{p}")

            Like.objects.create(user=request.user, post=p, state_date=timezone.now())
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # def get(self, request):
    #     students = Like.objects.all()
    #     serialized = likeSerializer(students, many=True)
    #     return Response(serialized.data)
