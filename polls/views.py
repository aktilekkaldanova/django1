from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from .models import Choice, Question, Account

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

@csrf_exempt
def test(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        login = data.get("login")
        password = data.get("password")

        Account.objects.create(
            login = login,
            password = encode(password, 3)
        )

        return JsonResponse({"message":"Account created"})
    else:
        return HttpResponse("The method is not supported. Please send a POST  request.")

def encode(text,n):
    result = " "

    for char in text:
        if char.isalpha():
            shift = (ord(char)- ord('a') + n) % 26
            result += chr(ord('a') + shift)
        else:
            result += char
    return result

@csrf_exempt
def account(request, pk=None):
    if request.method == "GET":
        if pk is None:
            accounts = Account.objects.all()
            data = [
                {"id":a.id, "login":a.login, "password":a.password}
                for a in accounts
            ]
            return JsonResponse(data,safe=False)
        else:
            try:
                a = Account.objects.get(pk=pk)
                data = {
                    "id":a.id,
                    "login":a.login,
                    "password":a.password,
                }
                return JsonResponse(data)
            except Account.DoesNotExist:
                return JsonResponse({"error":"Not Found"}, status = 404)
    elif request.method == "PATCH":
        try:
            a = Account.objects.get(pk=pk)
            body = json.loads(request.body)

            if "login" in body:
                a.login = body["login"]
            if "password" in body:
                a.password = body["password"]
            
            a.save()

            return JsonResponse({
                "id": a.id,
                "login": a.login,
                "password": a.password,
            })

        except Account.DoesNotExist:
            return JsonResponse({"error":"Not Found"}, status = 404)

    elif request.method == "DELETE":
        try:
            a = Account.objects.get(pk=pk)
            a.delete()
            return JsonResponse({"message":"Deleted"})
        except Account.DoesNotExist:
            return JsonResponse({"error":"Not Found"}, status = 404)                                          