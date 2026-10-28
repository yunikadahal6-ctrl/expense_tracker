from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

# Create your views here.
@login_required
def task_list(request):
    items = Task.objects.filter(user=request.user).order_by('is_completed', '-created_at')

    priority = request.GET.get('priority')
    if priority:
        items = items.filter(priority = priority)
    query = request.GET.get('q')
    if query:
        items = items.filter(title__icontains = query)
    pending_count = items.filter(is_completed = False).count()
    return render (request, 'todo/task_list.html',{'items' : items , 'pending_count' : pending_count})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html',{'form': form})
@login_required
def task_update(request, pk):
    item = get_object_or_404(Task, pk = pk, user = request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=item)
    return render(request,'todo/task_form.html',{'form':form , 'item':item})

@login_required
def task_delete(request,pk):
    item = get_object_or_404(Task, pk = pk, user = request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('task_list')
    return render(request, 'todo/task_delete.html',{'item':item})

@login_required
#mark tasks Done / Undo with 1 click):
def toggle_task(request,pk):
    item = get_object_or_404(Task, pk = pk, user = request.user)
    item.is_completed = not item.is_completed
    item.save()
    return redirect('task_list')






