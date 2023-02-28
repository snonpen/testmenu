from django import template
from django.urls import reverse
from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu_items = MenuItem.objects.filter(parent=None, name=menu_name).prefetch_related('children')
    current_path = context['request'].path

    def _recursive_draw_menu(menu_items):
        menu_html = ''
        for item in menu_items:
            is_active = current_path == item.url or current_path.startswith(item.url)
            submenu_html = _recursive_draw_menu(item.children.all()) if item.children.count() else ''
            if is_active:
                item_class = 'active'
                submenu_class = 'show'
            else:
                item_class = ''
                submenu_class = ''
            menu_html += f'<li class="nav-item {item_class}">'
            menu_html += f'<a href="{item.url}" class="nav-link">{item.name}</a>'
            menu_html += submenu_html and f'<ul class="dropdown-menu {submenu_class}" aria-labelledby="navbarDropdown">{submenu_html}</ul>'
            menu_html += '</li>'
        return menu_html

    return _recursive_draw_menu(menu_items)
