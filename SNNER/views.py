from django.shortcuts import render, render_to_response
from django.http import HttpResponse
# Create your views here.


def test_view(request):

    return render_to_response('test.html')