from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Student
class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student
    
# Create your views here.
def index(request):
    # Render the HTML template index.html with the data in context variable
    return render(request, 'portfolio_app/index.html')
    
