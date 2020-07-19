from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Test, Question, Option
import datetime
import random


def index(request):
    return render(request, 'test_constructor/index.html')


def add_test(request):
    if request.method == "POST":
        test = Test()
        test.title = request.POST.get("title")
        test.author = request.user
        test.pub_date = datetime.datetime.now()
        while True:
            code = random.randint(10000000, 99999999)
            if Test.objects.filter(code=code).count() == 0:
                test.code = code
                break
        test.save()
        return HttpResponseRedirect("/test_constructor/test/?code={0}".format(test.code))


def new_test(request):
    code = request.GET.get("code")
    questions = Question.objects.filter(test_code=code)
    return render(request, "test_constructor/testConstructor.html",
                  {"questions": questions, "code": code})


def add_question(request):
    if request.method == "POST":
        question = Question()
        code = request.GET.get("code")
        question.test_code = code
        question.id = request.GET.get("id")
        question.text = request.POST.get("text")
        question.amount_of_points = request.POST.get("amount_of_points")
        question.image = request.POST.get("image")
        question.save()
        for i in range(20):
            try:
                option = Option()
                option.text = request.POST.get("option" + str(i + 1))
                option.question = question
                option.is_correct = request.POST.get("correct" + str(i + 1)) == "on"
                option.save()
            except:
                break
        return HttpResponseRedirect("/test_constructor/test/?code={0}".format(code))


def edit(request):
    try:
        id = request.GET.get("id")
        question = Question.objects.get(id=id)
        options = question.option_set.all()

        if request.method == "POST":
            code = request.GET.get("code")
            question.text = request.POST.get("text")
            question.amount_of_points = request.POST.get("amount_of_points")
            question.image = request.POST.get("image")
            question.save()
            i = 0
            for option in options:
                try:
                    option.text = request.POST.get("option" + str(i + 1))
                    option.is_correct = request.POST.get("correct" + str(i + 1)) == "on"
                    option.save()
                    i += 1
                except:
                    break
            for j in range(i, 20 - options.count()):
                try:
                    option = Option()
                    option.text = request.POST.get("option" + str(j + 1))
                    option.question = question
                    option.is_correct = request.POST.get("correct" + str(j + 1)) == "on"
                    option.save()
                except:
                    break
            return HttpResponseRedirect("/test_constructor/test/?code={0}".format(code))
        else:
            return render(request, "test_constructor/edit.html", {"question": question, "options": options})
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")


def delete(request):
    try:
        id = request.GET.get("id")
        code = request.GET.get("code")
        question = Question.objects.get(id=id)
        question.delete()
        return HttpResponseRedirect("/test_constructor/test/?code={0}".format(code))
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")
