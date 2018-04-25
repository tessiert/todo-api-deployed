from django.urls import path
from . import api

urlpatterns = [
    path('todo/', api.TodoListView.as_view(), name='todo_list'),
    path('todo/<int:todo_id>/', api.TodoDetailView.as_view(), name='todo_detail')
]
