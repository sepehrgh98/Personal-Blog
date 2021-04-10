from django import template
from django.template.loader import get_template
from blog.models import Category

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def subfinder(val):
    o = Category.objects.filter(parent_category=val)

    return o


def parentCat(val):
    ParentCategory_list= []
    c = Category.objects.get(name=val.name)
    ParentCategory_list.append(c)
    while c.parent_category:
        PCat = c.parent_category
        ParentCategory_list.append(PCat)
        c = Category.objects.get(name=PCat)
    print(f'+++++{ParentCategory_list}')
    print(type(ParentCategory_list[0]))
    return ParentCategory_list


def like_counter(val):
    return val.like_set.all().count()


def dislike_counter(val):
    return val.dislike_set.all().count()


register.filter('like_counter', like_counter)
register.filter('dislike_counter', dislike_counter)
register.filter('parentCat', parentCat)
register.filter('subfinder', subfinder)


def liked_or_disliked(post, user):
    mylikeusers = []
    mydislikeusers = []
    for item in post.like_set.all():
        mylikeusers.append(item.user)
    for item in post.dislike_set.all():
        mydislikeusers.append(item.user)
    if user in mylikeusers:
        return True
    elif user in mydislikeusers:
        return False
    else:
        return None


register.filter('liked_or_disliked', liked_or_disliked)

mypost_list = []


def delPost(post_list, val):
    mypost_list.append(val)
    p = list(post_list)
    p = p - mypost_list
    return p




register.filter('delPost', delPost)
