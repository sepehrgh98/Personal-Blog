from django.http import HttpResponseRedirect
from django.views import generic
from .forms import content_form, TagForm, Post_Category_Form, Post_form
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


#main page
class IndexView(generic.ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        pass


#new_post_page
def new_Post(request):
    if request.POST:
        post_form = Post_form(request.POST)
        my_content_form = content_form(request.POST)
        tag_form = TagForm(request.POST)
        category_form = Post_Category_Form(request.POST)
        if post_form.is_valid() and my_content_form.is_valid() and tag_form.is_valid() and category_form.is_valid():
            content = my_content_form.save(commit=False)
            content.last_update = timezone.now()
            content.save()
            tag = tag_form.save(commit=False)
            tag.last_update = timezone.now()
            tag.save()
            category = category_form.save(commit=False)
            category.last_update = timezone.now()
            category.save()
            post = post_form.save(commit=False)
            post.last_update = timezone.now()
            post.tag = tag
            post.content = content
            post.category = category
            return HttpResponseRedirect(reverse('blog:post_detail', args=(post.id,)))
    else:
        post_form = Post_form()
        my_content_form = content_form()
        tag_form = TagForm()
        category_form = Post_Category_Form()
    return render(request, 'blog/new_post.html', {'post_form':post_form
        , 'my_content_form':my_content_form
        , 'tag_form':tag_form
        , 'category_form':category_form })


#post_result
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
