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
        except ValueError:
            return JsonResponse({"success": False, "msg": "Provide a valid JSON payload"},
                status=400)
        try:
            todo = Todo.objects.create(
                title=payload['title'],
                completed=payload.get('completed', False)
                )
        except (ValueError, KeyError):
            return JsonResponse(
                {"success": False, "msg": "Provided payload is not valid"},
                status=400
                )
        data = {'title': todo.title, 'completed': todo.completed}
        return JsonResponse(data, status=201, safe=False)


class TodoDetailView(BaseCSRFExemptView):
    def get(self, request, todo_id):
        raise NotImplementedError('Detail POST')

    def delete(self, request, todo_id):
        raise NotImplementedError('Detail DELETE')

    def patch(self, request, todo_id):
        raise NotImplementedError('Detail PATCH')

    def put(self, request, todo_id):
        raise NotImplementedError('Detail PUT')
