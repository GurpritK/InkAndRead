from django.shortcuts import render

# Create your views here.


def index(request):
    """
    Display the home page.
    
    **Template:**
    :template:`home/index.html`
    """
    return render(request, 'home/index.html')
