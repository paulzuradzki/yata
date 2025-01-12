from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from . import forms
from .models import TodoItem


@require_http_methods(["GET"])
def index(request):
    form = forms.CreateTodoForm()
    todos = TodoItem.objects.all()
    context = {"todo_items": todos, "form": form}
    return render(request, "todos/index.html", context)


@require_http_methods(["POST"])
def action_add_new_todo(request):
    form = forms.CreateTodoForm(request.POST)
    instance = form.save()
    return render(request, "todos/partial_todo_item.html", {"item": instance})
