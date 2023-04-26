# from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404
# from .models import Question, Choice
# from django.urls import reverse


# def index(request):
#     latest_question_list = Question.objects.order_by('pub_date')[:5]
#     return render(request, "polls/index.html", {
#         "latest_question_list": latest_question_list, })


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     # raise Http404("Question does not exist")
#     # print(f"the without one -> {question.choice_set.all}")
#     # print(f"the with() one -> {question.choice_set.all()}")
#     # for a in question.choice_set.all:
#     #     print(a.choice_text)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {
#         "question": question,
#     })


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form
#         return render(request, "polls/detail.html", {
#             "question": question,
#             "error_message": "You didn't select a choice",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         # print("-----------------hit")
#         # return HttpResponse("wow")
#         # return render(request, "polls/result.html")
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def owner(request):
#     return HttpResponse("Hello, world. 3c48606c is the polls index.")

# ---------------------------------USING GENERIC VIEWS------------------------------

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def owner(request):
        return HttpResponse("Hello, world. 3c48606c is the polls owner.")