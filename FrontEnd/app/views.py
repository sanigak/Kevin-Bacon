"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from .forms import ActorForm

from .Engine import Engine


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Bacon Page',
            'year':datetime.now().year,
            'form':ActorForm(),
        }
    )



def ans(request):
    """Renders the ans page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ActorForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            actor = form.cleaned_data['actor']
            answer = Engine(actor, "")

            return render(request, 'app/ans.html', {'ans': answer})
    return render(
        request,
        'app/ans.html',
        {
            
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'My contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'An application that finds solutions to the game Six Degrees of Kevin Bacon.',
            'year':datetime.now().year,
        }
    )
