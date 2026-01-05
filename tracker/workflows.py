"""
LangGraph workflows for the three-module system
"""
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
import json
import logging

from .ai_config import get_chatgpt, invoke_chatgpt, AIModelConfig
from .models import (
    VisibilityProject, Brand, Competitor, Prompt, AIModel, 
    ModelSelection, PromptResponse, BrandMention, SentimentScore,
    VisibilityScore, DetailedReport, ExecutionLog
)

logger = logging.getLogger(__name__)


# ============================================================
# MODULE 1: USER INTERFACE PART - LangGraph State
# ============================================================

class Module1State(TypedDict):
    """State for Module 1 - User Interface workflow"""
    project_id: int
    company_name: str
    company_description: str
    area_of_work: str
    refined_summary: str
    competitors: List[Dict[str, str]]
    prompts: List[str]
    status: str
    error: str


def analyze_company(state: Module1State) -> Module1State:
    """Step 1: Analyze company and generate refined summary using Gemini"""
    project = VisibilityProject.objects.get(id=state['project_id'])
    
    try:
        ExecutionLog.objects.create(
            project=project,
            module='module1',
            level='info',
            message='Starting company analysis with Gemini'
        )
        
        prompt = f"""You are a business analyst. Analyze this company:

Company Name: {state['company_name']}
Description: {state['company_description']}
Area of Work: {state['area_of_work']}

Provide:
1. A refined 2-3 sentence summary of what this company does
2. Their positioning in the market

Be concise and clear. Format as JSON:
{{
    "refined_summary": "...",
    "market_positioning": "..."
}}"""
        
        success, response, error = invoke_chatgpt(prompt)
        
        if not success:
            ExecutionLog.objects.create(
                project=project,
                module='module1',
                level='error',
                message=f'Failed to analyze company: {error}'
            )
            state['error'] = error
            state['status'] = 'failed'
            return state
        
        # Parse response
        try:
            result = json.loads(response)
            state['refined_summary'] = result.get('refined_summary', state['company_description'])
            
            # Update project
            project.refined_summary = state['refined_summary']
            project.save()
            
            ExecutionLog.objects.create(
                project=project,
                module='module1',
                level='info',
                message='Company analysis completed'
            )
            
        except json.JSONDecodeError:
            state['refined_summary'] = response
            project.refined_summary = response
            project.save()
        
        state['status'] = 'analyzing_competitors'
        
    except Exception as e:
        logger.exception("Error in analyze_company")
        state['error'] = str(e)
        state['status'] = 'failed'
        
        ExecutionLog.objects.create(
            project=project,
            module='module1',
            level='error',
            message=f'Exception in analyze_company: {str(e)}'
        )
    
    return state


def discover_competitors(state: Module1State) -> Module1State:
    """Step 2: Discover competitors using Gemini"""
    project = VisibilityProject.objects.get(id=state['project_id'])
    
    try:
        ExecutionLog.objects.create(
            project=project,
            module='module1',
            level='info',
            message='Starting competitor discovery'
        )
        
        prompt = f"""You are a market research expert. Based on this company:

Company: {state['company_name']}
Summary: {state['refined_summary']}
Area: {state['area_of_work']}

Identify the top 5-7 MAIN COMPETITORS in the same space.

Return ONLY a JSON array of competitors:
[
    {{"name": "Competitor1", "description": "Brief description"}},
    {{"name": "Competitor2", "description": "Brief description"}},
    ...
]

Be specific and relevant. Only include direct competitors."""
        
        success, response, error = invoke_chatgpt(prompt)
        
        if not success:
            ExecutionLog.objects.create(
                project=project,
                module='module1',
                level='warning',
                message=f'Competitor discovery failed: {error}. Using fallback.'
            )
            state['competitors'] = []
            state['status'] = 'generating_prompts'
            return state
        
        # Parse competitors
        try:
            competitors = json.loads(response)
            
            # Save to database
            for comp in competitors:
                Competitor.objects.get_or_create(
                    project=project,
                    name=comp['name'],
                    defaults={
                        'description': comp.get('description', ''),
                        'is_ai_suggested': True,
                        'is_validated': False
                    }
                )
            
            state['competitors'] = competitors
            
            ExecutionLog.objects.create(
                project=project,
                module='module1',
                level='info',
                message=f'Discovered {len(competitors)} competitors'
            )
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse competitors JSON")
            state['competitors'] = []
        
        state['status'] = 'generating_prompts'
        
    except Exception as e:
        logger.exception("Error in discover_competitors")
        state['error'] = str(e)
        state['competitors'] = []
        state['status'] = 'generating_prompts'  # Continue anyway
    
    return state


def generate_prompts(state: Module1State) -> Module1State:
    """Step 3: Generate realistic AI prompts users might ask"""
    project = VisibilityProject.objects.get(id=state['project_id'])
    
    try:
        ExecutionLog.objects.create(
            project=project,
            module='module1',
            level='info',
            message='Starting prompt generation'
        )
        
        competitor_names = [c['name'] for c in state.get('competitors', [])]
        
        prompt = f"""You are a user behavior expert. Generate 8-12 realistic questions that users might ask AI assistants about products/services in this category:

Company: {state['company_name']}
Category: {state['area_of_work']}
Description: {state['refined_summary']}
Competitors: {', '.join(competitor_names)}

Generate questions that:
- Are natural and conversational
- Would genuinely trigger mentions of brands in this space
- Cover different angles (best, comparison, alternatives, specific use cases)
- Are specific enough to get detailed answers

Return ONLY a JSON array of strings:
["Question 1", "Question 2", ...]

Examples for a CRM tool:
["What's the best CRM for startups?", "Which CRM integrates well with Slack?", "Salesforce vs HubSpot for small teams"]
"""
        
        success, response, error = invoke_chatgpt(prompt)
        
        if not success:
            ExecutionLog.objects.create(
                project=project,
                module='module1',
                level='warning',
                message=f'Prompt generation failed: {error}. Using defaults.'
            )
            state['prompts'] = [
                f"What's the best {state['area_of_work']} tool?",
                f"Top {state['area_of_work']} solutions for businesses",
            ]
            state['status'] = 'completed'
            return state
        
        # Parse prompts
        try:
            prompts = json.loads(response)
            
            # Save to database
            for prompt_text in prompts:
                Prompt.objects.get_or_create(
                    project=project,
                    text=prompt_text,
                    defaults={
                        'is_ai_generated': True,
                        'is_selected': False
                    }
                )
            
            state['prompts'] = prompts
            
            ExecutionLog.objects.create(
                project=project,
                module='module1',
                level='info',
                message=f'Generated {len(prompts)} prompts'
            )
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse prompts JSON")
            state['prompts'] = []
        
        state['status'] = 'completed'
        project.status = 'validating'
        project.save()
        
    except Exception as e:
        logger.exception("Error in generate_prompts")
        state['error'] = str(e)
        state['prompts'] = []
        state['status'] = 'failed'
    
    return state


def create_module1_graph():
    """Create LangGraph workflow for Module 1"""
    workflow = StateGraph(Module1State)
    
    # Add nodes
    workflow.add_node("analyze_company", analyze_company)
    workflow.add_node("discover_competitors", discover_competitors)
    workflow.add_node("generate_prompts", generate_prompts)
    
    # Define flow
    workflow.set_entry_point("analyze_company")
    workflow.add_edge("analyze_company", "discover_competitors")
    workflow.add_edge("discover_competitors", "generate_prompts")
    workflow.add_edge("generate_prompts", END)
    
    return workflow.compile()


def run_module1(project_id: int) -> Dict[str, Any]:
    """Execute Module 1 workflow"""
    project = VisibilityProject.objects.get(id=project_id)
    
    initial_state = {
        'project_id': project_id,
        'company_name': project.company_name,
        'company_description': project.company_description,
        'area_of_work': project.area_of_work,
        'refined_summary': '',
        'competitors': [],
        'prompts': [],
        'status': 'started',
        'error': ''
    }
    
    graph = create_module1_graph()
    result = graph.invoke(initial_state)
    
    return result
