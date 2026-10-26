from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # <-- NAYA: Security ko lagi
from .forms import BookmarkForm
from .models import Bookmark

# @login_required le login navako user lai yo page herna didaina
@login_required 
def bookmark_list(request):
    # NAYA: all() ko satto filter(user=request.user) haleko (Aafno matra dekhna)
    items = Bookmark.objects.filter(user=request.user).order_by('-created_at')

    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)

    query = request.GET.get('q')
    if query:
        items = items.filter(title__icontains=query)

    return render(request, 'manager/bookmark_list.html', {'items': items})


@login_required
def bookmark_create(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            # NAYA: Data save garnu vanda paila roknu (commit=False)
            bookmark = form.save(commit=False)
            # Login vako user lai yo bookmark ko malik banaune
            bookmark.user = request.user
            # Ani balla final save garne
            bookmark.save()
            return redirect('bookmark_list')
    else:
        form = BookmarkForm()
    return render(request, 'manager/bookmark_form.html', {'form': form})


@login_required
def bookmark_update(request, pk):
    # NAYA: user=request.user thapeko (Aru ko ID type garera edit garna namilos)
    item = get_object_or_404(Bookmark, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('bookmark_list')
    else:
        form = BookmarkForm(instance=item)
    return render(request, 'manager/bookmark_form.html', {'form': form})


@login_required
def bookmark_delete(request, pk):
    # NAYA: user=request.user thapeko (Aru ko bookmark delete garna namilos)
    item = get_object_or_404(Bookmark, pk=pk, user=request.user)
    
    if request.method == 'POST':
        item.delete()
        return redirect('bookmark_list')
    return render(request, 'manager/bookmark_confirm_delete.html', {'item': item})