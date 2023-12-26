from django.shortcuts import redirect, render
import requests
import wikipedia
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def home(request):
    return render(request, "dashboardApp/home.html")


# Create Notes views here.
@login_required()
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
@login_required()
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
@login_required()
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


@login_required()
def todo(request):
    todos = Todo.objects.filter(is_finished=False, user=request.user)
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
    # todo = Todo.objects.filter(user=request.user)
    todo = Todo.objects.all()
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
@login_required()
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    messages.warning(
        request, f"Task has been deleted successfully, {request.user.username} !"
    )
    return redirect("todo")


# Google Books


def Library(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get("text", "")
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()

        # Use a list comprehension for better readability
        result_list = [
            {
                "title": item["volumeInfo"]["title"],
                "subtitle": item["volumeInfo"].get("subtitle", ""),
                "description": item["volumeInfo"].get("description", ""),
                "count": item["volumeInfo"].get("pageCount", 0),
                "category": item["volumeInfo"].get("categories", []),
                "rating": item["volumeInfo"].get(
                    "averageRating", 0
                ),  # Change to the correct attribute if needed
                "thumbnail": item["volumeInfo"]
                .get("imageLinks", {})
                .get("thumbnail", ""),
                "preview": item["volumeInfo"].get("previewLink", ""),
            }
            for item in answer.get("items", [])[:10]
        ]

        context = {"form": form, "results": result_list}
        return render(request, "dashboardApp/books.html", context)
    else:
        form = DashboardForm()
        context = {"form": form}
        return render(request, "dashboardApp/books.html", context)


# Dictionaries Views
def get_dictionaries(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get("text")
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()

        try:
            # Extract data from the API response
            phonetics = answer[0]["phonetics"][0]["text"]
            audio = answer[0]["phonetics"][0]["audio"]
        except (KeyError, IndexError):
            # Handle the case where the expected fields are not present in the API response
            phonetics = "Phonetics data not available"
            audio = "Audio data not available"

        try:
            definition = answer[0]["meanings"][0]["definitions"][0]["definition"]
            example = answer[0]["meanings"][0]["definitions"][0]["example"]
            synonyms = answer[0]["meanings"][0]["definitions"][0]["synonyms"]
        except (KeyError, IndexError):
            # Handle the case where the expected fields are not present in the API response
            definition = "Definition not available"
            example = "Example not available"
            synonyms = []

        context = {
            "form": form,
            "input": text,  # Changed from "input" to the actual input text
            "phonetics": phonetics,
            "audio": audio,
            "definition": definition,
            "example": example,
            "synonyms": synonyms,
        }
        return render(request, "dashboardApp/dictionary.html", context)

    else:
        form = DashboardForm()
        context = {
            "form": form,
        }
        return render(request, "dashboardApp/dictionary.html", context)


# wikipedia
def wikipedia_page(request):
    if request.method == "POST":
        text = request.POST["text"]
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            "form": form,
            "title": search.title,
            "link": search.url,
            "details": search.summary,
        }
        return render(request, "dashboardApp/wiki.html", context)
    else:
        form = DashboardForm()
        context = {"form": form}
    return render(request, "dashboardApp/wiki.html", context)


# Conversion functions
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST["measurement"] == "mass":
            measurement_form = ConversionMassForm()
            context = {
                "form": form,
                "m_form": measurement_form,
                "input": True,
            }
            if "input" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ""
                if input and int(input) >= 0:
                    if first == "pound" and second == "kilogram":
                        answer = f"{input} pound = {int(input)*0.453592} kilogram"
                    if first == "kilogram" and second == "pound":
                        answer = f"{input} kilogram = {int(input)*2.2062} pound"
                context = {
                    "form": form,
                    "m_form": measurement_form,
                    "input": True,
                    "answer": answer,
                }

        else:
            if request.POST["measurement"] == "length":
                measurement_form = ConversionLengthForm()
            context = {
                "form": form,
                "m_form": measurement_form,
                "input": True,
            }
            if "input" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ""
                if input and int(input) >= 0:
                    if first == "yard" and second == "foot":
                        answer = f"{input} yard = {int(input)*3} foot"
                    if first == "foot" and second == "yard":
                        answer = f"{input} foot = {int(input)/3} yard"
                context = {
                    "form": form,
                    "m_form": measurement_form,
                    "input": True,
                    "answer": answer,
                }

    else:
        form = ConversionForm()
        context = {
            "form": form,
            "input": False,
        }
    return render(request, "dashboardApp/conversion.html", context)


# Register Form``
def Register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account Registration completed successfully: {username}"
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "dashboardApp/register.html", context)


# # Profile form
def Profile(request):
    homework = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        "homeworks": homework,
        "todos": todos,
        "home_done": homework_done,
        "todos_done": todos_done,
    }
    return render(request, "dashboardApp/profile.html", context)


# LOGOUT
def LOGOUT(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account Registration completed successfully: {username}"
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "dashboardApp/logout.html", context)
