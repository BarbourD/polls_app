

from django.http import  HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


class IndexView(generic.ListView):
    template_name = 'polls2/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls2/detail.html'

    def get_queryset(self):
        """
        Excludes and questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls2/results.html'

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls2/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls2/results.html', {'question': question})
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
       
        return render(request, 'polls2/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    
        return HttpResponseRedirect(reverse('polls2:results', args=(question.id,)))