from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.root),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('signup', views.signup),
    path('details', views.details),
    path('search', views.search),
    path('autocomplete', views.autocomplete, name="autocomplete"),
    path('details/<int:p_id>', views.details),
    path('order/<int:p_id>', views.order),
    path('order/post_order/<int:p_id>', views.post_order),
    path('account/<int:u_id>', views.account),
    path('update/<int:u_id>', views.update),
    path('order', views.order),
    path('about', views.about),
    path('contact', views.contact),
    path('admin/<int:u_id>', views.admin),
    path('like/<int:p_id>', views.like),
    path('review/<int:p_id>', views.review),
    path('review', views.review),
    path('deleteuser/<int:id>', views.deleteuser),
    path('editproduct/<int:id>', views.editproduct),
    path('updateproduct/<int:id>', views.updateproduct),
    path('deleteproduct/<int:id>', views.deleteproduct),
    path('addproduct', views.addproduct),
    path('addadmin', views.addadmin),
    path('thankyou', views.thankyou),
]