from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from .forms import EventForm
from .models import Post, Event, Booking
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'blog/event-detail.html', {'event': event})


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user.username
            event.save()
            messages.success(request, 'Event added successfully!')
            return redirect('event')
    else:
        form = EventForm()
    return render(request, 'blog/add_event.html', {'form': form})


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not Booking.objects.filter(user=request.user, event=event).exists():
        Booking.objects.create(user=request.user, event=event)
        messages.success(request, 'Event booked successfully!')
    else:
        messages.warning(request, 'You have already booked this event.')

    return redirect('event')


def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by("-date_posted")
    else:
        posts = Post.objects.all()
    return render(request, 'blog/search-results.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


def home(request):
    user_count = User.objects.count()
    return render(request, 'blog/mainhome.html', {'user_count': user_count})


def get_user_count(request):
    user_count = User.objects.count()
    return JsonResponse({'user_count': user_count})


def team(request):
    return render(request, 'blog/team.html', {'title': "Team Page"})


def contact(request):
    return render(request, 'blog/contact.html', {'title': "Contact Page"})


def event(request):
    events = Event.objects.all()
    booked_events = Booking.objects.filter(user=request.user).values_list('event_id', flat=True)
    is_booked = {event.id: (event.id in booked_events) for event in events}
    return render(request, 'blog/event.html', {'events': events, 'is_booked': is_booked})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
