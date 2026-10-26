from django.contrib import admin
from django.urls import path
from django.urls import path, include  # <-- NAYA: include thapeko chha hai yaha
from django.views.generic import TemplateView

# 1. 'as' use garera dubai views lai aafno aafno naam dine
from tracker import views as tracker_views
from manager import views as manager_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # NAYA: Django ko ready-made Login/Logout URLs yaha connect vayo
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Tracker (Expense) ko paths - aagadi 'expense/' prefix thapeko
    path('expense/', tracker_views.expense_list, name='expense_list'),
    path('expense/create/', tracker_views.expense_create, name='expense_create'),
    path('expense/<int:pk>/edit/', tracker_views.expense_update, name='expense_update'),
    path('expense/<int:pk>/delete/', tracker_views.expense_delete, name='expense_delete'),

    # Manager (Bookmark) ko paths - aagadi 'bookmark/' prefix thapeko
    path('bookmark/', manager_views.bookmark_list, name='bookmark_list'),
    path('bookmark/create/', manager_views.bookmark_create, name='bookmark_create'),  
    path('bookmark/<int:pk>/edit/', manager_views.bookmark_update, name='bookmark_update'),
    path('bookmark/<int:pk>/delete/', manager_views.bookmark_delete, name='bookmark_delete'),
]