from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event
from .forms import EventForm
from django.shortcuts import redirect
from django.contrib import messages

# About page view
def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})

# Contact page view
def contact(request):
    return render(request, 'blog/contact.html', {'title': "About Page"})  # Updated title for clarity

# Search results view
def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()
    return render(request, 'blog/search_results.html', {'posts': posts})

# Post list view
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]

# Post detail view
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

# Post create view
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Post update view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Post delete view
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def event_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        events = Event.objects.filter(title__icontains=search_query)
    else:
        events = Event.objects.all()

    return render(request, 'blog/events.html', {'events': events})


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'blog/event_detail.html', {'event': event})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'blog/events.html', {'events': events})


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('event-list')
    else:
        form = EventForm()
    return render(request, 'blog/add_event.html', {'form': form})
