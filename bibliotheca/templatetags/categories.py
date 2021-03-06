from django import template
from bibliotheca.models import Categories

register = template.Library()

@register.inclusion_tag('cat_menu.html')
def get_main_categories():
    main = Categories.objects.get(name='Książki')
    cats = Categories.objects.filter(top_category_id=main.id)
    return {'cats' : cats}

@register.inclusion_tag('search_categories_combobox.html', takes_context=True)
def get_cats(context):
    cats = Categories.objects.all()
    if 'formdata' in context:
        cid = context['formdata']['cid']
    else:
        cid = 0
    return {'categories' : cats, 'cid' : cid}