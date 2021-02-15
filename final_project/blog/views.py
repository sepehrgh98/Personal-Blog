from django.http import HttpResponseRedirect
from django.views import generic
from .forms import TagForm, Post_Category_Form, Post_form
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag, Post_category


# main page
class IndexView(generic.ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        pass


# post_pre_view
class Post_Pre_View(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog/post_pre_view.html'


# new_post_page
def new_Post(request):
    if request.POST:
        post_form = Post_form(request.POST, request.FILES)
        tag_form = TagForm(request.POST)
        category_form = Post_Category_Form(request.POST)
        if post_form.is_valid() and tag_form.is_valid() and category_form.is_valid():

            tag = tag_form.save(commit=False)
            if tag.name not in Tag.objects.values_list('name', flat=True):
                tag.save()
                tag_form.save_m2m()

            category = category_form.save(commit=False)
            category.last_update = timezone.now()
            category.save()
            category_form.save()

            post = post_form.save(commit=False)
            post.last_update = timezone.now()
            post.category = category
            post.tag = tag
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


# post_result
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog/post_pre_view.html'
