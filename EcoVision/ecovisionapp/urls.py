from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from .views import event_list, event_detail

urlpatterns = [
    path('about/', views.about, name="blog-about"),
    path('search/', views.search, name="search"),  # Add the search path
    path('', PostListView.as_view(), name="blog-home"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
    path('contact/', views.contact, name='blog-contact'),
    path('events/', event_list, name='events'),
    path('event/<int:pk>/', event_detail, name='event-detail'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/', views.event_list, name='event-list'),
]
