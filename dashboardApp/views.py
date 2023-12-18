from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "dashboardApp/home.html")
