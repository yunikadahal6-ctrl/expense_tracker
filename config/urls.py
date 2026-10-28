from django.contrib import admin
from django.urls import path
from django.urls import path, include  # <-- NAYA: include thapeko chha hai yaha
from django.views.generic import TemplateView

# 1. 'as' use garera dubai views lai aafno aafno naam dine
from tracker import views as tracker_views
from manager import views as manager_views
from todo import views as todo_views

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

    path('accounts/signup/', manager_views.signup_view, name='signup'),

    #todo app:
    path('todo/',todo_views.task_list, name='task_list'),
    path('todo/create/',todo_views.task_create, name = 'task_create'),
    path('todo/<int:pk>/edit/',todo_views.task_update, name = 'task_update'),
    path('todo/<int:pk>/toggle/',todo_views.toggle_task, name = 'toggle_task'),
    path('todo/<int:pk>/delete/',todo_views.task_delete, name = 'task_delete'),


]