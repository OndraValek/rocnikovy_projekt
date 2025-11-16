from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ForumThread, ForumPost
from subjects.models import Topic


class ThreadDetailView(LoginRequiredMixin, DetailView):
    """Detail diskusního vlákna s příspěvky."""
    model = ForumThread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'
    pk_url_kwarg = 'thread_id'
    
    def get_object(self, queryset=None):
        """Získá vlákno a zvýší počet zobrazení."""
        thread = super().get_object(queryset)
        thread.views += 1
        thread.save(update_fields=['views'])
        return thread
    
    def get_context_data(self, **kwargs):
        """Přidá příspěvky do kontextu."""
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        return context


class ThreadCreateView(LoginRequiredMixin, CreateView):
    """Vytvoření nového diskusního vlákna."""
    model = ForumThread
    template_name = 'forum/create_thread.html'
    fields = ['title']
    
    def dispatch(self, request, *args, **kwargs):
        """Získá topic před zobrazením."""
        self.topic = get_object_or_404(Topic, id=kwargs['topic_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Nastaví topic a autora při vytváření vlákna."""
        form.instance.topic = self.topic
        form.instance.author = self.request.user
        
        # Vytvořit první příspěvek
        content = self.request.POST.get('content')
        if not content:
            messages.error(self.request, 'Vyplňte prosím obsah prvního příspěvku.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        
        # Vytvořit první příspěvek
        ForumPost.objects.create(
            thread=self.object,
            author=self.request.user,
            content=content
        )
        
        messages.success(self.request, 'Diskusní vlákno bylo úspěšně vytvořeno.')
        return response
    
    def get_context_data(self, **kwargs):
        """Přidá topic do kontextu."""
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context
    
    def get_success_url(self):
        """Přesměruje na detail vlákna."""
        return reverse_lazy('forum:thread_detail', kwargs={'thread_id': self.object.id})


class PostCreateView(LoginRequiredMixin, CreateView):
    """Vytvoření nového příspěvku ve vlákně."""
    model = ForumPost
    template_name = 'forum/create_post.html'
    fields = ['content']
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontroluje, zda není vlákno zamčené."""
        self.thread = get_object_or_404(ForumThread, id=kwargs['thread_id'])
        
        if self.thread.is_locked and not request.user.is_teacher:
            messages.error(request, 'Toto vlákno je zamčené.')
            return redirect('forum:thread_detail', thread_id=self.thread.id)
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Nastaví thread a autora při vytváření příspěvku."""
        form.instance.thread = self.thread
        form.instance.author = self.request.user
        messages.success(self.request, 'Příspěvek byl úspěšně přidán.')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Přesměruje na detail vlákna."""
        return reverse_lazy('forum:thread_detail', kwargs={'thread_id': self.thread.id})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Úprava příspěvku."""
    model = ForumPost
    template_name = 'forum/edit_post.html'
    fields = ['content']
    pk_url_kwarg = 'post_id'
    
    def test_func(self):
        """Zkontroluje oprávnění k úpravě."""
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_teacher
    
    def form_valid(self, form):
        """Označí příspěvek jako upravený."""
        form.instance.is_edited = True
        messages.success(self.request, 'Příspěvek byl úspěšně upraven.')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Přesměruje na detail vlákna."""
        return reverse_lazy('forum:thread_detail', kwargs={'thread_id': self.object.thread.id})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Smazání příspěvku."""
    model = ForumPost
    template_name = 'forum/post_confirm_delete.html'
    pk_url_kwarg = 'post_id'
    
    def test_func(self):
        """Zkontroluje oprávnění ke smazání."""
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_teacher
    
    def get_success_url(self):
        """Přesměruje na detail vlákna."""
        thread_id = self.object.thread.id
        messages.success(self.request, 'Příspěvek byl úspěšně smazán.')
        return reverse_lazy('forum:thread_detail', kwargs={'thread_id': thread_id})

