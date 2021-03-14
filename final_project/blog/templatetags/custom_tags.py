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
