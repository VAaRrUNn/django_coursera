from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views import View

# Create your views here.


class IndexView(View):
    def get(self, request):
        # resp = HttpResponse("hi you are in demo1")
        response = render(request, "demo1/main.html", {
            "cookies": request.COOKIES,
        })
        response.set_cookie("value", 1)
        response.content += b"kyu"
        print(f"the login url is {reverse('login')}")
        print(f"the login url is {reverse('logout')}")
        return response
