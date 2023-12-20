from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch


# Create your views here.
def home(request):
    return render(request, "dashboardApp/home.html")


# Create Notes views here.
def notes(request):
    if request.method == "POST":
        forms = NotesForm(request.POST)
        if forms.is_valid():
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


# Home Work Item
def homework(request):
    if request.method == "POST":
        forms = HomeworkForm(request.POST)
        if forms.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            homeworks = Homework(
                user=request.user,
                subject=request.POST["subject"],
                title=request.POST["title"],
                description=request.POST["description"],
                due_date=request.POST["due_date"],
                is_finished=finished,
            )
            homeworks.save()
            messages.success(
                request,
                f"Bravo, {request.user.username}: You Added Yours Homework successfully!!!",
            )
    else:
        forms = HomeworkForm()

    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {"homeworks": homework, "homeworks_done": homework_done, "form": forms}

    return render(request, "dashboardApp/homework.html", context)


# Update Homework
def update_homework(request, pk=None):
    homeworks = Homework.objects.get(id=pk)

    if homeworks.is_finished == True:
        homeworks.is_finished = False
    else:
        homeworks.is_finished = True
    homeworks.save()
    return redirect("homework")


# Delete Homework
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    messages.warning(
        request, f"Notes has been deleted successfully, {request.user.username} !"
    )
    return redirect("homework")


# Youtube Researcher
def youtube_researcher(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()["result"]:
            result_dict = {
                "input": text,
                "title": i["title"],
                "duration": i["duration"],
                "thumbnail": i["thumbnails"][0]["url"],
                "channel": i["channel"]["name"],
                "link": i["link"],
                "views": i["viewCount"]["short"],
                "published": i["publishedTime"],
            }
            desc = ""
            if i["descriptionSnippet"]:
                for j in i["descriptionSnippet"]:
                    desc += j["text"]
            result_dict["description"] = desc
            result_list.append(result_dict)

            context = {"form": form, "results": result_list}
        return render(request, "dashboardApp/youtube.html", context)
    else:
        form = DashboardForm()
    context = {"form": form}
    return render(request, "dashboardApp/youtube.html", context)


# Add todo Application
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user, title=request.POST["title"], is_finished=finished
            )
            todos.save()
            messages.success(
                request, f"{request.user.username}: You added New Todo successfully!!!"
            )
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    # todos = Todo.objects.all()
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    # todo = Todo.objects.all()
    context = {
        "form": form,
        "todos": todo,
        "todos_done": todos_done,
    }
    return render(request, "dashboardApp/todo.html", context)


# Update Todo
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")


# Delete Todo
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    messages.warning(
        request, f"Task has been deleted successfully, {request.user.username} !"
    )
    return redirect("todo")


def Library(request):
    return render(request, "dashboardApp/books.html")
