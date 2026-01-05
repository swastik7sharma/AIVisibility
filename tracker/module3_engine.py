"""
Module 3: Analysis and Think Engine
Generates insights, comparisons, and actionable recommendations
"""
import json
import logging
from typing import Dict, List, Any
from django.db.models import Avg, Count, Q
from .ai_config import invoke_chatgpt
from .models import (
    VisibilityProject, VisibilityScore, BrandMention, 
    SentimentScore, PromptResponse, DetailedReport, ExecutionLog
)

logger = logging.getLogger(__name__)


class AnalysisEngine:
    """Generate comprehensive analysis and recommendations"""
    
    def __init__(self, project_id: int):
        self.project = VisibilityProject.objects.get(id=project_id)
        self.brand_name = self.project.company_name
    
    def run(self):
        """Execute full analysis"""
        try:
            ExecutionLog.objects.create(
                project=self.project,
                module='module3',
                level='info',
                message='Starting analysis engine'
            )
            
            # Generate all analysis sections
            competitor_comparison = self.generate_competitor_comparison()
            prompt_wise = self.generate_prompt_wise_analysis()
            model_wise = self.generate_model_wise_analysis()
            negative_sentiment = self.analyze_negative_sentiment()
            research_sources = self.extract_research_sources()
            
            # Generate insights using ChatGPT
            insights = self.generate_insights(
                competitor_comparison,
                prompt_wise,
                model_wise,
                negative_sentiment
            )
            
            # Generate action plan
            action_plan = self.generate_action_plan(insights)
            
            # Create or update report
            report, created = DetailedReport.objects.update_or_create(
                project=self.project,
                defaults={
                    'competitor_comparison': competitor_comparison,
                    'prompt_wise_analysis': prompt_wise,
                    'model_wise_analysis': model_wise,
                    'negative_sentiment_analysis': negative_sentiment,
                    'research_sources': research_sources,
                    'why_competitors_win': insights.get('why_competitors_win', ''),
                    'content_gaps': insights.get('content_gaps', ''),
                    'messaging_gaps': insights.get('messaging_gaps', ''),
                    'positioning_weaknesses': insights.get('positioning_weaknesses', ''),
                    'content_ideas': action_plan.get('content_ideas', []),
                    'seo_pr_recommendations': action_plan.get('seo_pr', []),
                    'messaging_improvements': action_plan.get('messaging', [])
                }
            )
            
            self.project.status = 'completed'
            self.project.save()
            
            ExecutionLog.objects.create(
                project=self.project,
                module='module3',
                level='info',
                message='Analysis completed successfully'
            )
            
            return True
            
        except Exception as e:
            logger.exception("Error in AnalysisEngine")
            self.project.status = 'failed'
            self.project.save()
            
            ExecutionLog.objects.create(
                project=self.project,
                module='module3',
                level='error',
                message=f'Analysis failed: {str(e)}'
            )
            
            return False
    
    def generate_competitor_comparison(self) -> Dict:
        """Generate competitor leaderboard and comparison"""
        scores = VisibilityScore.objects.filter(
            project=self.project
        ).order_by('-normalized_score')
        
        leaderboard = []
        main_brand_score = None
        
        for score in scores:
            entry = {
                'brand': score.brand_name,
                'visibility_score': round(score.normalized_score, 2),
                'frequency': round(score.frequency_score * 100, 1),
                'prominence': round(score.prominence_score, 3),
                'sentiment': round(score.sentiment_score, 3),
                'mentions': score.total_mentions,
                'prompts_appeared': score.prompts_appeared_in
            }
            
            leaderboard.append(entry)
            
            if score.is_main_brand:
                main_brand_score = entry
        
        # Calculate gaps
        if leaderboard:
            top_competitor = leaderboard[0] if not leaderboard[0]['brand'].lower() == self.brand_name.lower() else (leaderboard[1] if len(leaderboard) > 1 else None)
            
            gap_analysis = {}
            if main_brand_score and top_competitor:
                gap_analysis = {
                    'score_gap': round(top_competitor['visibility_score'] - main_brand_score['visibility_score'], 2),
                    'frequency_gap': round(top_competitor['frequency'] - main_brand_score['frequency'], 1),
                    'prominence_gap': round(top_competitor['prominence'] - main_brand_score['prominence'], 3)
                }
        else:
            gap_analysis = {}
        
        return {
            'leaderboard': leaderboard,
            'main_brand': main_brand_score,
            'gap_analysis': gap_analysis
        }
    
    def generate_prompt_wise_analysis(self) -> Dict:
        """Analyze which brands win for which prompts"""
        prompts = self.project.prompts.filter(is_selected=True)
        
        prompt_analysis = []
        
        for prompt in prompts:
            # Get all mentions for this prompt across all models
            mentions = BrandMention.objects.filter(
                response__prompt=prompt,
                response__project=self.project
            ).select_related('response', 'sentiment').order_by('position')
            
            if not mentions.exists():
                continue
            
            # Group by brand
            brand_mentions = {}
            for mention in mentions:
                brand = mention.brand_name
                if brand not in brand_mentions:
                    brand_mentions[brand] = {
                        'positions': [],
                        'sentiments': [],
                        'count': 0
                    }
                
                brand_mentions[brand]['positions'].append(mention.position)
                brand_mentions[brand]['count'] += 1
                
                if hasattr(mention, 'sentiment'):
                    brand_mentions[brand]['sentiments'].append(mention.sentiment.sentiment)
            
            # Determine winner (lowest average position)
            winner = None
            winner_avg_pos = float('inf')
            
            for brand, data in brand_mentions.items():
                avg_pos = sum(data['positions']) / len(data['positions'])
                if avg_pos < winner_avg_pos:
                    winner = brand
                    winner_avg_pos = avg_pos
            
            main_brand_present = self.brand_name in brand_mentions
            main_brand_position = None
            
            if main_brand_present:
                main_brand_position = round(
                    sum(brand_mentions[self.brand_name]['positions']) / 
                    len(brand_mentions[self.brand_name]['positions']), 
                    2
                )
            
            prompt_analysis.append({
                'prompt': prompt.text,
                'winner': winner,
                'winner_avg_position': round(winner_avg_pos, 2),
                'main_brand_present': main_brand_present,
                'main_brand_position': main_brand_position,
                'brands_mentioned': list(brand_mentions.keys())
            })
        
        return {'prompts': prompt_analysis}
    
    def generate_model_wise_analysis(self) -> Dict:
        """Analyze which model favors which brand"""
        models = self.project.selected_models.filter(is_selected=True)
        
        model_analysis = []
        
        for model_selection in models:
            model = model_selection.model
            
            # Get mentions for this model
            mentions = BrandMention.objects.filter(
                response__model=model,
                response__project=self.project
            ).values('brand_name').annotate(
                count=Count('id'),
                avg_position=Avg('position')
            ).order_by('avg_position')
            
            top_brand = None
            main_brand_data = None
            
            for mention_data in mentions:
                if not top_brand:
                    top_brand = mention_data
                
                if mention_data['brand_name'].lower() == self.brand_name.lower():
                    main_brand_data = mention_data
            
            model_analysis.append({
                'model': model.display_name,
                'top_brand': top_brand['brand_name'] if top_brand else None,
                'top_brand_avg_position': round(top_brand['avg_position'], 2) if top_brand else None,
                'main_brand_avg_position': round(main_brand_data['avg_position'], 2) if main_brand_data else None,
                'main_brand_mentions': main_brand_data['count'] if main_brand_data else 0
            })
        
        return {'models': model_analysis}
    
    def analyze_negative_sentiment(self) -> Dict:
        """Find and analyze negative sentiment instances"""
        negative_sentiments = SentimentScore.objects.filter(
            mention__response__project=self.project,
            sentiment='negative'
        ).select_related('mention', 'mention__response', 'mention__response__prompt', 'mention__response__model')
        
        negative_instances = []
        
        for sent in negative_sentiments:
            negative_instances.append({
                'brand': sent.mention.brand_name,
                'prompt': sent.mention.response.prompt.text,
                'model': sent.mention.response.model.display_name,
                'context': sent.mention.context,
                'reasoning': sent.reasoning
            })
        
        return {
            'total_negative': len(negative_instances),
            'instances': negative_instances
        }
    
    def extract_research_sources(self) -> List[str]:
        """Extract any URLs or sources mentioned in responses"""
        responses = PromptResponse.objects.filter(
            project=self.project,
            status='success'
        )
        
        sources = []
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        
        import re
        
        for response in responses:
            urls = re.findall(url_pattern, response.raw_response)
            sources.extend(urls)
        
        # Return unique sources
        return list(set(sources))
    
    def generate_insights(
        self, 
        competitor_comparison: Dict,
        prompt_wise: Dict,
        model_wise: Dict,
        negative_sentiment: Dict
    ) -> Dict:
        """Use Gemini to generate strategic insights"""
        
        # Prepare data summary
        data_summary = f"""
VISIBILITY ANALYSIS DATA:

Main Brand: {self.brand_name}

LEADERBOARD:
{json.dumps(competitor_comparison.get('leaderboard', []), indent=2)}

GAP ANALYSIS:
{json.dumps(competitor_comparison.get('gap_analysis', {}), indent=2)}

PROMPT-WISE WINNERS:
{json.dumps(prompt_wise.get('prompts', [])[:5], indent=2)}

MODEL-WISE PERFORMANCE:
{json.dumps(model_wise.get('models', []), indent=2)}

NEGATIVE SENTIMENT:
{json.dumps(negative_sentiment, indent=2)}
"""
        
        prompt = f"""You are a strategic brand consultant. Analyze this AI visibility data and provide insights:

{data_summary}

Provide a comprehensive analysis addressing:

1. WHY COMPETITORS WIN
   - What makes top competitors more visible?
   - What patterns emerge from their mentions?
   - How do they position themselves?

2. CONTENT GAPS
   - What topics/angles are competitors covering that {self.brand_name} isn't?
   - What use cases are missing?

3. MESSAGING GAPS
   - How do competitors communicate their value?
   - What messaging resonates with AI models?

4. POSITIONING WEAKNESSES
   - Where does {self.brand_name} fall short?
   - What positioning adjustments are needed?

Return as JSON:
{{
    "why_competitors_win": "Detailed explanation...",
    "content_gaps": "Specific gaps...",
    "messaging_gaps": "Messaging issues...",
    "positioning_weaknesses": "Positioning problems..."
}}
"""
        
        success, response, error = invoke_chatgpt(prompt)
        
        if success:
            try:
                insights = json.loads(response)
                return insights
            except json.JSONDecodeError:
                logger.warning("Failed to parse insights JSON")
        
        # Fallback
        return {
            'why_competitors_win': 'Analysis pending',
            'content_gaps': 'Analysis pending',
            'messaging_gaps': 'Analysis pending',
            'positioning_weaknesses': 'Analysis pending'
        }
    
    def generate_action_plan(self, insights: Dict) -> Dict:
        """Generate actionable recommendations"""
        
        prompt = f"""Based on these insights about {self.brand_name}'s AI visibility:

{json.dumps(insights, indent=2)}

Generate a concrete ACTION PLAN with:

1. CONTENT IDEAS (5-7 specific pieces)
   - Blog posts, guides, comparisons
   - Topics that will improve visibility

2. SEO/PR RECOMMENDATIONS (5-7 actions)
   - Link building strategies
   - PR opportunities
   - Authority building

3. MESSAGING IMPROVEMENTS (5-7 changes)
   - Value proposition refinements
   - Positioning adjustments
   - Key messages to emphasize

Be specific and actionable.

Return as JSON:
{{
    "content_ideas": ["Idea 1", "Idea 2", ...],
    "seo_pr": ["Action 1", "Action 2", ...],
    "messaging": ["Change 1", "Change 2", ...]
}}
"""
        
        success, response, error = invoke_chatgpt(prompt)
        
        if success:
            try:
                action_plan = json.loads(response)
                return action_plan
            except json.JSONDecodeError:
                logger.warning("Failed to parse action plan JSON")
        
        # Fallback
        return {
            'content_ideas': [],
            'seo_pr': [],
            'messaging': []
        }


def run_module3(project_id: int) -> bool:
    """Execute Module 3 workflow"""
    engine = AnalysisEngine(project_id)
    return engine.run()
