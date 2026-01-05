"""
Django views for AI Visibility Tracker
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import threading

from .models import (
    VisibilityProject, Brand, Competitor, Prompt, AIModel, 
    ModelSelection, VisibilityScore, DetailedReport
)
from .workflows import run_module1
from .module2_engine import run_module2
from .module3_engine import run_module3


def index(request):
    """Landing page"""
    return render(request, 'tracker/index.html')


def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'tracker/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'tracker/login.html', {'form': form})


@login_required
def dashboard(request):
    """Main dashboard showing all projects"""
    projects = VisibilityProject.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tracker/dashboard.html', {'projects': projects})


@login_required
def create_project(request):
    """Step 1: Create new project and enter company details"""
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_description = request.POST.get('company_description')
        area_of_work = request.POST.get('area_of_work')
        
        if not all([company_name, company_description, area_of_work]):
            messages.error(request, 'All fields are required')
            return render(request, 'tracker/create_project.html')
        
        # Create project
        project = VisibilityProject.objects.create(
            user=request.user,
            name=f"{company_name} Visibility Check",
            company_name=company_name,
            company_description=company_description,
            area_of_work=area_of_work,
            status='setup'
        )
        
        # Create main brand
        Brand.objects.create(
            project=project,
            name=company_name,
            description=company_description
        )
        
        # Run Module 1 in background
        def run_analysis():
            run_module1(project.id)
        
        thread = threading.Thread(target=run_analysis)
        thread.daemon = True
        thread.start()
        
        messages.success(request, 'Project created! Analyzing your company...')
        return redirect('validate_project', project_id=project.id)
    
    return render(request, 'tracker/create_project.html')


@login_required
def validate_project(request, project_id):
    """Step 2: Validate AI-generated competitors and prompts"""
    project = get_object_or_404(VisibilityProject, id=project_id, user=request.user)
    
    if request.method == 'POST':
        # Handle form submission
        
        # Update refined summary
        refined_summary = request.POST.get('refined_summary')
        if refined_summary:
            project.refined_summary = refined_summary
            project.save()
        
        # Update competitor validation
        for competitor in project.competitors.all():
            checkbox_name = f'competitor_{competitor.id}'
            if checkbox_name in request.POST:
                competitor.is_validated = True
            else:
                competitor.is_validated = False
            competitor.save()
        
        # Add custom competitors
        custom_competitors = request.POST.get('custom_competitors', '')
        if custom_competitors:
            for comp_name in custom_competitors.split('\n'):
                comp_name = comp_name.strip()
                if comp_name:
                    Competitor.objects.get_or_create(
                        project=project,
                        name=comp_name,
                        defaults={
                            'is_ai_suggested': False,
                            'is_validated': True
                        }
                    )
        
        # Update prompt selection
        for prompt in project.prompts.all():
            checkbox_name = f'prompt_{prompt.id}'
            prompt.is_selected = checkbox_name in request.POST
            prompt.save()
        
        # Add custom prompts
        custom_prompts = request.POST.get('custom_prompts', '')
        if custom_prompts:
            for prompt_text in custom_prompts.split('\n'):
                prompt_text = prompt_text.strip()
                if prompt_text:
                    Prompt.objects.create(
                        project=project,
                        text=prompt_text,
                        is_ai_generated=False,
                        is_selected=True
                    )
        
        project.status = 'validating'
        project.save()
        
        return redirect('select_models', project_id=project.id)
    
    competitors = project.competitors.all()
    prompts = project.prompts.all()
    
    return render(request, 'tracker/validate_project.html', {
        'project': project,
        'competitors': competitors,
        'prompts': prompts
    })


@login_required
def select_models(request, project_id):
    """Step 3: Select AI models to query"""
    project = get_object_or_404(VisibilityProject, id=project_id, user=request.user)
    
    if request.method == 'POST':
        # Get or create all models
        models_data = [
            ('chatgpt', 'ChatGPT', 1.0),
            ('claude', 'Claude', 0.9),
            ('gemini', 'Gemini', 0.8),
        ]
        
        for model_name, display_name, weight in models_data:
            model, created = AIModel.objects.get_or_create(
                name=model_name,
                defaults={
                    'display_name': display_name,
                    'weight': weight
                }
            )
            
            # Check if selected
            checkbox_name = f'model_{model_name}'
            if checkbox_name in request.POST:
                ModelSelection.objects.get_or_create(
                    project=project,
                    model=model,
                    defaults={'is_selected': True}
                )
        
        # Trigger execution
        return redirect('execute_check', project_id=project.id)
    
    # Get available models
    models = AIModel.objects.filter(is_active=True)
    
    return render(request, 'tracker/select_models.html', {
        'project': project,
        'models': models
    })


@login_required
def execute_check(request, project_id):
    """Execute visibility check (Module 2 & 3)"""
    project = get_object_or_404(VisibilityProject, id=project_id, user=request.user)
    
    if request.method == 'POST':
        # Start execution in background
        def run_full_check():
            # Run Module 2
            success = run_module2(project.id)
            
            if success:
                # Run Module 3
                run_module3(project.id)
        
        thread = threading.Thread(target=run_full_check)
        thread.daemon = True
        thread.start()
        
        messages.success(request, 'Visibility check started! This may take a few minutes...')
        return redirect('check_status', project_id=project.id)
    
    # Show summary
    selected_prompts = project.prompts.filter(is_selected=True).count()
    selected_models = project.selected_models.filter(is_selected=True).count()
    total_queries = selected_prompts * selected_models
    
    return render(request, 'tracker/execute_check.html', {
        'project': project,
        'selected_prompts': selected_prompts,
        'selected_models': selected_models,
        'total_queries': total_queries
    })


@login_required
def check_status(request, project_id):
    """Check execution status"""
    project = get_object_or_404(VisibilityProject, id=project_id, user=request.user)
    
    return render(request, 'tracker/check_status.html', {
        'project': project
    })


@login_required
@require_http_methods(["GET"])
def api_project_status(request, project_id):
    """API endpoint to check project status"""
    project = get_object_or_404(VisibilityProject, id=project_id, user=request.user)
    
    return JsonResponse({
        'status': project.status,
        'is_complete': project.status == 'completed',
        'is_failed': project.status == 'failed'
    })


@login_required
def view_report(request, project_id):
    """View final report"""
    project = get_object_or_404(VisibilityProject, id=project_id, user=request.user)
    
    if project.status != 'completed':
        messages.warning(request, 'Report not ready yet')
        return redirect('check_status', project_id=project.id)
    
    # Get report
    report = get_object_or_404(DetailedReport, project=project)
    
    # Get visibility scores
    scores = VisibilityScore.objects.filter(project=project).order_by('-normalized_score')
    
    return render(request, 'tracker/view_report.html', {
        'project': project,
        'report': report,
        'scores': scores
    })


@login_required
def competitor_impersonation(request, project_id, competitor_id):
    """Run analysis from competitor's perspective"""
    original_project = get_object_or_404(VisibilityProject, id=project_id, user=request.user)
    competitor = get_object_or_404(Competitor, id=competitor_id, project=original_project)
    
    # Create new project with competitor as main brand
    new_project = VisibilityProject.objects.create(
        user=request.user,
        name=f"{competitor.name} Visibility Check (Impersonation)",
        company_name=competitor.name,
        company_description=competitor.description,
        area_of_work=original_project.area_of_work,
        status='setup',
        is_competitor_view=True,
        competitor_brand_id=competitor.id
    )
    
    # Copy data from original project
    Brand.objects.create(
        project=new_project,
        name=competitor.name,
        description=competitor.description
    )
    
    # Copy competitors (excluding the one that's now main brand)
    for comp in original_project.competitors.exclude(id=competitor.id):
        Competitor.objects.create(
            project=new_project,
            name=comp.name,
            description=comp.description,
            is_ai_suggested=comp.is_ai_suggested,
            is_validated=comp.is_validated
        )
    
    # Add original company as competitor
    Competitor.objects.create(
        project=new_project,
        name=original_project.company_name,
        description=original_project.company_description,
        is_ai_suggested=False,
        is_validated=True
    )
    
    messages.success(request, f'Created impersonation view for {competitor.name}')
    return redirect('validate_project', project_id=new_project.id)
