from django import template
from django.template.loader import get_template

register = template.Library()


@register.inclusion_tag("blog/nested_cat.html")
def nested_cat(cat):
    cats = cat.post_category_set.all()
    print(f'dvsf{cats}')
    return {'cats': cats}


# nested_cat_template = get_template('blog/nested_cat.html')
# print(f'ssssssssssss{nested_cat_template}')
# register.inclusion_tag(nested_cat_template)(nested_cat)

register.filter('nested_cat', nested_cat)


def like_counter(val):
    return val.like_set.all().count()


def dislike_counter(val):
    return val.dislike_set.all().count()


register.filter('like_counter', like_counter)
register.filter('dislike_counter', dislike_counter)


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