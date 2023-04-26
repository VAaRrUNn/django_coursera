from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from autos.models import Auto, Make
from autos.forms import MakeForm
# Create your views here.

# If you inherit View first then LoginRequiredMixin, then authentication won't happen


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        mc = Make.objects.all().count()
        a1 = Auto.objects.all()

        ctx = {"make_count": mc, "auto_list": a1}
        return render(request, "autos/auto_list.html", ctx)


# class MakeView(LoginRequiredMixin, View):
class MakeView(LoginRequiredMixin, View):
    def get(self, request):
        m1 = Make.objects.all()
        ctx = {"make_list": m1}
        return render(request, "autos/make_list.html", ctx)

# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded

# making a new row in database or adding it

# to creat a form of the model -> autos.
class MakeCreate(LoginRequiredMixin, View):
    template = "autos/make_form.html"
    success_url = reverse_lazy("autos:all")

    def get(self, request):
        form = MakeForm()
        ctx = {"form": form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = MakeForm(request.POST)
        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template, ctx)

        make = form.save()
        return redirect(self.success_url)

# update the row


class MakeUpdate(LoginRequiredMixin, View):
    model = Make
    success_url = reverse_lazy('autos:all')
    template = 'autos/make_form.html'

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = MakeForm(instance=make)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = MakeForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)

# delete the row


class MakeDelete(LoginRequiredMixin, View):
    model = Make
    success_url = reverse_lazy('autos:all')
    template = 'autos/make_confirm_delete.html'

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = MakeForm(instance=make)
        ctx = {'make': make}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        make.delete()
        return redirect(self.success_url)

# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes



# This makes things more easy wow 
# just map it using AutoCreate.as_view() then everything will be handled
# accordingly and to redirect to the specified success_url ... ooo
class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.
# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview
