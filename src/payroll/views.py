from django.shortcuts import render

def home_view(request):
    user = request.user
    context={
        'user':user
        }
    return render(request, "main/index.html", context)