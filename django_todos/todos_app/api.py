import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Todo


class BaseCSRFExemptView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TodoListView(BaseCSRFExemptView):
    def get(self, request):
        status = request.GET.get('status', 'all')
        if (status == 'all'):
            todos = list(Todo.objects.all().values('id', 'title', 'completed'))
        elif (status == 'active'):
            todos = list(Todo.objects.filter(completed=False).values('id', 'title', 'completed'))
        elif (status == 'completed'):
            todos = list(Todo.objects.filter(completed=True).values('id', 'title', 'completed'))
        else:
            return JsonResponse({"success": False, 'msg': 'Invalid item status supplied'}, 
                status=400)
        response = {
            'filter': status, 
            'count': len(todos),
            'results': todos
        }
        return JsonResponse(response)

    def post(self, request):
        try:
            payload = json.loads(self.request.body)
        except (KeyError, ValueError):
            return JsonResponse({"success": False, "msg": "Provide a valid JSON payload"},
                status=400)
        try:
            todo = Todo.objects.create(
                title=payload['title'],
                completed=payload.get('completed', False)
                )
        except (KeyError, ValueError):
            return JsonResponse(
                {"success": False, "msg": "Provided payload is not valid"},
                status=400
                )
        data = {'title': todo.title, 'completed': todo.completed}
        return JsonResponse(data, status=201, safe=False)


class TodoDetailView(BaseCSRFExemptView):
    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        return JsonResponse({'id': todo.id, 'title': todo.title, 'completed': todo.completed})

    def delete(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.delete()
        return HttpResponse(status=204)

    def patch(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        try:
            payload = json.loads(self.request.body)
        except (KeyError, ValueError):
            return JsonResponse({"success": False, "msg": "Provide a valid JSON payload"}, 
                status=400)
        for field in Todo._meta.get_fields():
            # 1st clause: non-user specified fields, 2nd clause: not all fields need be present for 'PATCH'
            if (field.name in ['id', 'created', 'modified']) or (field.name not in payload.keys()):
                continue
            else:
                try:
                    setattr(todo, field.name, payload[field.name])
                except TypeError:
                    return JsonResponse({"success": False, "msg": "Provide a valid JSON payload"}, 
                        status=400)
        if ('action' in payload.keys() and 'toggle' in payload.values()):
            # Toggle status of todo list item
            todo.completed = not todo.completed
        todo.save()
        return HttpResponse(status=204)


    def put(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        try:
            payload = json.loads(self.request.body)
        except (KeyError, ValueError):
            return JsonResponse({"success": False, "msg": "Provide a valid JSON payload"}, 
                status=400)
        for field in Todo._meta.get_fields():
            if (field.name in ['id', 'created', 'modified']):    # Not user-specified fields
                continue
            if (field.name not in payload.keys()):
                return JsonResponse({'error': 'Missing argument: {}'.format(field.name)}, 
                    status=400)
            try:
                setattr(todo, field.name, payload[field.name])
            except TypeError:
                return JsonResponse({"success": False, "msg": "Provide a valid JSON payload"}, 
                    status=400)
        todo.save()
        return HttpResponse(status=204)


