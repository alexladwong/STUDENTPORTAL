from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.views import generic


# Create your views here.
def home(request):
    return render(request, "dashboardApp/home.html")


# Create Notes views here.
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user,
                title=request.POST["title"],
                description=request.POST["description"],
            )
            notes.save()
        messages.success(
            request, f"Notes saved successfully, {request.user.username} !"
        )

    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {"notes": notes, "forms": form}

    return render(request, "dashboardApp/notes.html", context)


# Delete notes
def delete_notes(request, pk=None):
    Notes.objects.get(id=pk).delete()
    messages.success(
        request, f"Notes has been deleted successfully, {request.user.username} !"
    )
    return redirect("notes")


# Note Details
class NotesDetailView(generic.DetailView):
    model = Notes
