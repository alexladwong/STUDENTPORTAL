from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("notes/", views.notes, name="notes"),
    path("delete-notes/<int:pk>", views.delete_notes, name="delete_notes"),
    path(
        "notes-details/<int:pk>", views.NotesDetailView.as_view(), name="notes_details"
    ),
    path("homework/", views.homework, name="homework"),
    path("update-homework/<int:pk>", views.update_homework, name="update_homework"),
    path("delete-homework/<int:pk>", views.delete_homework, name="delete_homework"),
    path("youtube-research", views.youtube_researcher, name="youtube_researcher"),
    path("todo", views.todo, name="todo"),
    path("update-todo/<int:pk>", views.update_todo, name="update_todo"),
    path("delete-todo/<int:pk>", views.delete_todo, name="delete_todo"),
    path("library/", views.Library, name="library"),
    path("dictionary/", views.get_dictionaries, name="dictionary"),
    path("s-wikipedia/", views.wikipedia_page, name="wikipedia"),
    path("conversion/", views.conversion, name="my_conversion"),
]
