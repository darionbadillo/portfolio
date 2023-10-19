from typing import Any
from django.shortcuts import *
from django.http import HttpResponse
from django.views import generic
from .models import Student, Portfolio, Project
from .forms import ProjectForm, PortfolioForm
    
# Create your views here.
def index(request):
    student_active_portfolios = Student.objects.select_related('portfolio').all().filter(portfolio__is_active=True)
    print("active portfolio query set", student_active_portfolios)
    return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})

def createProject(request, portfolio_id):
    form = ProjectForm()
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        project_data = request.POST.copy()
        project_data['portfolio_id'] = portfolio_id
        
        form = ProjectForm(project_data)
        if form.is_valid():
            # Save the form without committing to the database
            project = form.save(commit=False)
            # Set the portfolio relationship
            project.portfolio = portfolio
            project.save()

            # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form': form}
    return render(request, 'portfolio_app/project_form.html', context)

# Deletes Projects
def deleteProject(request, project_id, portfolio_id):
    # Gets the project to delete
    project = get_object_or_404(Project, pk=project_id)
    
    # Deletes the project if the request method is POST
    if request.method == 'POST':
        project.delete()
        return redirect('portfolio-detail', portfolio_id)

    # Renders the delete project page
    context = {'project': project}
    return render(request, 'portfolio_app/delete_project.html', context)

def updateProject(request, portfolio_id, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('portfolio-detail', portfolio_id)
        
    context = {'form': form, 'portfolio_id': portfolio_id, 'project': project} 
    return render(request, 'portfolio_app/update_project.html', context)


def updatePortfolio(request, student_id):
    
    portfolio = Portfolio.objects.get(id=student_id)    
    
    form = PortfolioForm(instance=portfolio)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('student-detail', student_id)
        
    context = {'form': form, 'portfolio': portfolio, 'student': student_id} 
    return render(request, 'portfolio_app/update_project.html', context)


class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student

class PortfolioDetailView(generic.DetailView):
    model = Portfolio 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_list'] = Project.objects.all()
        return context

class ProjectListView(generic.ListView):
    model = Project
class ProjectDetailView(generic.DetailView):
    model = Project