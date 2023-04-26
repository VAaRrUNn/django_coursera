from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from cats.models import Cat, Breed


# Create your views here.
class CatList(LoginRequiredMixin, View):
    def get(self, request):
        catlist = Cat.objects.all()
        no_of_breeds = len(Breed.objects.all())
        return render(request, "cats/catlist.html", {
            "catlist": catlist,
            "no_of_breeds": no_of_breeds,
        })


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy("cats:cat_list")

    # better specify this like this otherwise django will search inside templates dir not templates/cats
    template_name = "cats/cat_form.html"


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = "__all__"
    success_url = reverse_lazy("cats:cat_list")


class CatDelete(LoginRequiredMixin, DeleteView):
    # you have to make a cat_confirm_delete.html file for handling this, otherwise error 
    # error will tell you that it didn't find the file if you forgot to make one 
    model = Cat
    fields = "__all__"
    template_name = "cats/cat_confirm_delete.html"
    success_url = reverse_lazy("cats:cat_list")
    # this is the name using which we can access the object passed 
    context_object_name = "cat"


# ----------------------------
# FOR BREED

class BreedList(LoginRequiredMixin, View):
    template = "cats/breedlist.html"

    def get(self, request):
        breed_list = Breed.objects.all()
        return render(request, self.template, {
            "breed_list": breed_list,
        })


class BreedCreateForm(ModelForm):

    class Meta:
        model = Breed
        fields = "__all__"

# Just to practive not using CreateView here


class BreedCreate(LoginRequiredMixin, View):
    template = "cats/breed_form.html"
    success_url = reverse_lazy("cats:breed_list")

    def get(self, request):
        form = BreedCreateForm()
        return render(request, self.template, {
            "form": form,
        })

    def post(self, request):
        form = BreedCreateForm(request.POST)
        if not form.is_valid():
            return render(request, self.template, {
                "form": form,
            })

        form.save()
        return redirect(self.success_url)


class BreedUpdate(LoginRequiredMixin, View):
    model = Breed
    template = "cats/breedupdate.html"
    success_url = reverse_lazy("cats:breed_list")

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = BreedCreateForm(instance=obj)
        return render(request, self.template, {
            "form": form,
        })
    
    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = BreedCreateForm(request.POST, instance=obj)
        if not form.is_valid():
            return render(request, self.template, {
                "form": form,
            })
        
        form.save()
        return redirect(self.success_url)


class BreedDelete(LoginRequiredMixin, View):
    model = Breed
    template = "cats/breeddelete.html"
    success_url = reverse_lazy("cats:breed_list")

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.template, {
            "obj": obj,
        })
    

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return redirect(self.success_url)

    

