from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
    event_detail

urlpatterns = [
    # path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('search/', views.search, name="search"),
    path('team/', views.team, name="team"),
    path('', views.home, name="home"),
    path('blogs/', PostListView.as_view(), name="blog-home"),
    path('contact/', views.contact, name='contact'),
    path('get_user_count/', views.get_user_count, name='get_user_count'),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
    path('events/', views.event, name="event"),
    path('event/<int:pk>/', event_detail, name='event-detail'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/book/<int:event_id>/',views.book_event, name='book_event'),

]
