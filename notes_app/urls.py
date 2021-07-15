from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views as my_views

urlpatterns = [
    path('register/', my_views.RegisterView.as_view(), name='register'),
    path('login/', my_views.LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('note-create/', my_views.note_create, name='note-create'),

    path('notes/', my_views.NoteList.as_view(), name='notes'),
    path('note/<int:pk>/', my_views.NoteUpdate.as_view(), name='note'),
    path('note-delete/<int:pk>/', my_views.NoteDelete.as_view(), name='note-delete'),
]