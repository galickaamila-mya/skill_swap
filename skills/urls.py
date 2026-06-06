from django.urls import path
from . import views

app_name = "skills"
urlpatterns = [
    path("", views.skill_list, name="skill_list"),
    path("create/", views.skill_create, name="skill_create"),
    path("<int:skill_id>/", views.skill_detail, name="skill_detail"),
    path("<int:skill_id>/edit/", views.skill_update, name="skill_update"),
    path("<int:skill_id>/delete/", views.skill_delete, name="skill_delete"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("<int:skill_id>/wishlist/add/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/clear/", views.clear_wishlist, name="clear_wishlist"),
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),
]
