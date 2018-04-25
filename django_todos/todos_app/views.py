from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo


def index(request):
    todos = Todo.objects.all()
    status = request.GET.get('status', 'all')
    if status == 'active':
        todos = todos.filter(completed=False)
    elif status == 'completed':
        todos = todos.filter(completed=True)

    pending_count = Todo.objects.filter(completed=False).count()
    return render(request, 'index.html', {
        'todos': todos,
        'filter': status,
        'pending_count': pending_count
    })


def create(request):
    Todo.objects.create(title=request.POST['title'])
    return redirect('/')

def toggle(request):
    todo = get_object_or_404(Todo, id=request.POST['todo_id'])
    todo.completed = not todo.completed
    todo.save()
    return redirect('/')


def destroy(request):
    todo = get_object_or_404(Todo, id=request.POST['todo_id'])
    todo.delete()
    return redirect('/')
