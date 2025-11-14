from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import ForumThread, ForumPost
from subjects.models import Topic


@login_required
def thread_detail(request, thread_id):
    """Detail diskusního vlákna s příspěvky."""
    thread = get_object_or_404(ForumThread, id=thread_id)
    
    # Zvýšit počet zobrazení
    thread.views += 1
    thread.save(update_fields=['views'])
    
    posts = thread.posts.all()
    
    context = {
        'thread': thread,
        'posts': posts,
    }
    return render(request, 'forum/thread_detail.html', context)


@login_required
def create_thread(request, topic_id):
    """Vytvoření nového diskusního vlákna."""
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            thread = ForumThread.objects.create(
                topic=topic,
                title=title,
                author=request.user
            )
            ForumPost.objects.create(
                thread=thread,
                author=request.user,
                content=content
            )
            messages.success(request, 'Diskusní vlákno bylo úspěšně vytvořeno.')
            return redirect('forum:thread_detail', thread_id=thread.id)
        else:
            messages.error(request, 'Vyplňte prosím všechny povinné pole.')
    
    context = {
        'topic': topic,
    }
    return render(request, 'forum/create_thread.html', context)


@login_required
@require_POST
def create_post(request, thread_id):
    """Vytvoření nového příspěvku ve vlákně."""
    thread = get_object_or_404(ForumThread, id=thread_id)
    
    if thread.is_locked and not request.user.is_teacher:
        messages.error(request, 'Toto vlákno je zamčené.')
        return redirect('forum:thread_detail', thread_id=thread.id)
    
    content = request.POST.get('content')
    if content:
        ForumPost.objects.create(
            thread=thread,
            author=request.user,
            content=content
        )
        messages.success(request, 'Příspěvek byl úspěšně přidán.')
    else:
        messages.error(request, 'Příspěvek nemůže být prázdný.')
    
    return redirect('forum:thread_detail', thread_id=thread.id)


@login_required
def edit_post(request, post_id):
    """Úprava příspěvku."""
    post = get_object_or_404(ForumPost, id=post_id)
    
    # Zkontrolovat oprávnění
    if post.author != request.user and not request.user.is_teacher:
        messages.error(request, 'Nemáte oprávnění upravit tento příspěvek.')
        return redirect('forum:thread_detail', thread_id=post.thread.id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post.content = content
            post.is_edited = True
            post.save()
            messages.success(request, 'Příspěvek byl úspěšně upraven.')
            return redirect('forum:thread_detail', thread_id=post.thread.id)
    
    context = {
        'post': post,
    }
    return render(request, 'forum/edit_post.html', context)


@login_required
@require_POST
def delete_post(request, post_id):
    """Smazání příspěvku."""
    post = get_object_or_404(ForumPost, id=post_id)
    thread_id = post.thread.id
    
    # Zkontrolovat oprávnění
    if post.author != request.user and not request.user.is_teacher:
        messages.error(request, 'Nemáte oprávnění smazat tento příspěvek.')
    else:
        post.delete()
        messages.success(request, 'Příspěvek byl úspěšně smazán.')
    
    return redirect('forum:thread_detail', thread_id=thread_id)

