from django.http import HttpResponseRedirect
from django.views import generic
from .forms import TagForm, Category_Form, Post_form, UserForm
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag, User, Category, Like, Dislike, Comment, Post_Tag
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils import timezone
from rest_framework.views import APIView
from .serializers import LikeAndDislikeSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from dal import autocomplete
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import Group




# main page
class IndexView(ListView):
    context_object_name = 'post_list'
    queryset = Post.objects.all()
    template_name = 'blog/index.html'


# register page
def register(request):
    if request.POST:
        user_form = UserForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.last_update = timezone.now()
            group = Group.objects.get(name='ساده')
            user.save()
            user.groups.add(group)

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


# post
class myPost(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'

# tag
class myTag(generic.DetailView):
    model = Tag
    template_name = 'blog/tag.html'

# category_page
class myCategory(generic.DetailView):
    model = Category
    template_name = 'blog/categories.html'


#tagAPI
post_Tags=[]
class TagAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            print(f"<><><><>{data}")
            if data['tag_name'] not in Tag.objects.values_list('name', flat=True):
                t = Tag.objects.create(name=data['tag_name'])
            else:
                t = Tag.objects.filter(name=data['tag_name'])
                t = t[0]
                print(f"#####{t}")
            post_Tags.append(t)
            print(post_Tags)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class DeleteTagAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            print(f"<><><><>{data}")
            t = Post_Tag.objects.filter(tag=data['tag_id'],post=data['post_id'])
            t.delete()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# new_post_page
@login_required
def new_Post(request):
    if request.POST:
        post_form = Post_form(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.last_update = timezone.now()
            post.author = request.user
            post.save()
            for tag in post_Tags:
                Post_Tag.objects.create(tag=tag, post=post)

            post_Tags.clear()

            return HttpResponseRedirect(reverse('blog:index', args=(post.id,)))

    else:
        post_form = Post_form()
        tag_form = TagForm()
        category_form = Category_Form()
    return render(request, 'blog/new_post.html', {'post_form': post_form
        , 'tag_form': tag_form
        , 'category_form': category_form})





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


# CommentAPI
class CommentAPI(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            p = Post.objects.get(id=data['post_id'])
            Comment.objects.create(author=request.user, text=data['text'], post=p)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# CategoryAPI
ParentCategory_list = []


class CategoryAPI(APIView):
    def post(self, request):
        if request.data:
            ParentCategory_list.clear()
            data = request.POST
            c = Category.objects.get(name=data['category_name'])
            ParentCategory_list.append(c)
            while c.parent_category:
                PCat = c.parent_category
                ParentCategory_list.append(PCat)
                c = Category.objects.get(name=PCat)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryResultAPI(APIView):
    def get(self, request, format=None):
        serializer = CategorySerializer(ParentCategory_list, many=True)

        return Response(serializer.data)


# search view

def Searchbar(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        post_title = Post.objects.filter(title__contains = search)
        post_text = Post.objects.filter(text__contains=search)
        post_author = Post.objects.filter(author__username__contains=search)
        tag_name = Tag.objects.filter(name__contains=search)
        category_name = Category.objects.filter(name__contains=search)
        return render(request, 'blog/searchResult.html', {'search':search,
                                                          'post_title':post_title,
                                                          'post_text':post_text,
                                                          'post_author':post_author,
                                                          'tag_name':tag_name,
                                                          'category_name':category_name})
    else:
        return render(request, 'blog/searchResult.html', {})


#edit page
class Edit(ListView):
    model = Post
    context_object_name = 'post'
    # queryset = Post.objects.filter(is_accepted=False)
    template_name = 'blog/edit.html'


#edit_post
class PostEdit(UpdateView):
    model = Post
    fields = ['post_date', 'title', 'text', 'image', 'category', 'is_active', 'is_accepted']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('blog:index')


#post_activation
class ActivePost(APIView):
    def post(self, request):
        if request.data:
            data = request.POST
            p = Post.objects.filter(id=data["post_id"])
            if data["active_state"] == 'false':
                p.update(is_active=False)
            else:
                p.update(is_active=True)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)