
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newPost, name="newpost"),
    path("profile/<int:id>", views.Profile, name="profile"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name='following'),
    path("edit/<int:id>", views.edit, name='edit'),
    path("profile/edit/<int:id>", views.edit, name='profileedit'),
    path("addlike/<int:id>", views.addlike, name='addlike'),
    path("removelike/<int:id>", views.removelike, name='removelike'),
    path("profile/addlike/<int:id>", views.addlike, name='addlike'),
    path("profile/removelike/<int:id>", views.removelike, name='removelike'),
]
