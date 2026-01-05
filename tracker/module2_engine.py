"""
Module 2: Online Visibility Check Engine
Calculates frequency, prominence, sentiment, and model coverage scores
"""
import re
import json
import logging
from typing import List, Dict, Tuple
from django.db import transaction

from .ai_config import AIModelConfig, invoke_chatgpt
from .models import (
    VisibilityProject, Prompt, AIModel, ModelSelection,
    PromptResponse, BrandMention, SentimentScore, VisibilityScore,
    ExecutionLog, Competitor
)

logger = logging.getLogger(__name__)


class VisibilityCheckEngine:
    """Core engine for visibility checking and scoring"""
    
    def __init__(self, project_id: int):
        self.project = VisibilityProject.objects.get(id=project_id)
        self.brand_name = self.project.company_name
        self.competitor_names = list(
            self.project.competitors.values_list('name', flat=True)
        )
    
    def run(self):
        """Execute the full visibility check"""
        try:
            ExecutionLog.objects.create(
                project=self.project,
                module='module2',
                level='info',
                message='Starting visibility check engine'
            )
            
            self.project.status = 'checking'
            self.project.save()
            
            # Step 1: Query all selected models with all selected prompts
            self.query_models()
            
            # Step 2: Extract brand mentions from responses
            self.extract_mentions()
            
            # Step 3: Analyze sentiment for each mention
            self.analyze_sentiment()
            
            # Step 4: Calculate visibility scores
            self.calculate_scores()
            
            self.project.status = 'analyzing'
            self.project.save()
            
            ExecutionLog.objects.create(
                project=self.project,
                module='module2',
                level='info',
                message='Visibility check completed successfully'
            )
            
            return True
            
        except Exception as e:
            logger.exception("Error in VisibilityCheckEngine")
            self.project.status = 'failed'
            self.project.save()
            
            ExecutionLog.objects.create(
                project=self.project,
                module='module2',
                level='error',
                message=f'Visibility check failed: {str(e)}'
            )
            
            return False
    
    def query_models(self):
        """Query all selected models with all selected prompts"""
        selected_prompts = self.project.prompts.filter(is_selected=True)
        selected_models = self.project.selected_models.filter(is_selected=True)
        
        if not selected_prompts.exists():
            logger.warning("No prompts selected")
            return
        
        if not selected_models.exists():
            logger.warning("No models selected")
            return
        
        total = selected_prompts.count() * selected_models.count()
        completed = 0
        
        for prompt in selected_prompts:
            for model_selection in selected_models:
                model = model_selection.model
                
                try:
                    # Check if response already exists
                    response_obj, created = PromptResponse.objects.get_or_create(
                        project=self.project,
                        prompt=prompt,
                        model=model,
                        defaults={'status': 'pending'}
                    )
                    
                    if not created and response_obj.status == 'success':
                        # Already have successful response
                        completed += 1
                        continue
                    
                    # Query the model
                    ai_model = AIModelConfig.get_model_by_name(model.name, temperature=0.7)
                    success, response, error = AIModelConfig.invoke_with_retry(
                        ai_model, 
                        prompt.text
                    )
                    
                    if success:
                        response_obj.raw_response = response
                        response_obj.status = 'success'
                        response_obj.error_message = ''
                        
                        ExecutionLog.objects.create(
                            project=self.project,
                            module='module2',
                            level='info',
                            message=f'Successfully queried {model.display_name}'
                        )
                    else:
                        response_obj.status = 'failed'
                        response_obj.error_message = error
                        response_obj.retry_count += 1
                        
                        ExecutionLog.objects.create(
                            project=self.project,
                            module='module2',
                            level='warning',
                            message=f'Failed to query {model.display_name}: {error}'
                        )
                    
                    response_obj.save()
                    completed += 1
                    
                except Exception as e:
                    logger.exception(f"Error querying {model.name}")
                    ExecutionLog.objects.create(
                        project=self.project,
                        module='module2',
                        level='error',
                        message=f'Exception querying {model.display_name}: {str(e)}'
                    )
                    completed += 1
        
        ExecutionLog.objects.create(
            project=self.project,
            module='module2',
            level='info',
            message=f'Queried models: {completed}/{total} completed'
        )
    
    def extract_mentions(self):
        """Extract brand mentions from responses"""
        responses = PromptResponse.objects.filter(
            project=self.project,
            status='success'
        )
        
        all_brands = [self.brand_name] + self.competitor_names
        
        for response in responses:
            try:
                mentions = self._find_brand_mentions(response.raw_response, all_brands)
                
                for position, (brand, context) in enumerate(mentions, start=1):
                    is_main = (brand.lower() == self.brand_name.lower())
                    competitor_obj = None
                    
                    if not is_main:
                        competitor_obj = self.project.competitors.filter(
                            name__iexact=brand
                        ).first()
                    
                    BrandMention.objects.get_or_create(
                        response=response,
                        brand_name=brand,
                        position=position,
                        defaults={
                            'context': context,
                            'is_main_brand': is_main,
                            'competitor': competitor_obj
                        }
                    )
                
            except Exception as e:
                logger.exception(f"Error extracting mentions from response {response.id}")
    
    def _find_brand_mentions(self, text: str, brands: List[str]) -> List[Tuple[str, str]]:
        """
        Find brand mentions in text with context
        Returns: List of (brand_name, context) tuples in order of appearance
        """
        mentions = []
        text_lower = text.lower()
        
        for brand in brands:
            brand_lower = brand.lower()
            
            # Find all occurrences
            pattern = r'\b' + re.escape(brand_lower) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            
            for match in matches:
                # Extract context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                
                mentions.append((match.start(), brand, context))
        
        # Sort by position and remove duplicates
        mentions.sort(key=lambda x: x[0])
        seen_brands = set()
        unique_mentions = []
        
        for pos, brand, context in mentions:
            if brand.lower() not in seen_brands:
                unique_mentions.append((brand, context))
                seen_brands.add(brand.lower())
        
        return unique_mentions
    
    def analyze_sentiment(self):
        """Analyze sentiment for each brand mention using ChatGPT"""
        mentions = BrandMention.objects.filter(
            response__project=self.project
        ).select_related('response')
        
        for mention in mentions:
            try:
                # Check if sentiment already exists
                if hasattr(mention, 'sentiment'):
                    continue
                
                prompt = f"""Analyze the sentiment of how this brand is mentioned:

Brand: {mention.brand_name}
Context: {mention.context}
Full response: {mention.response.raw_response[:500]}

Determine the sentiment: very_positive, positive, neutral, or negative

Consider:
- Is the brand recommended?
- Are there positive attributes mentioned?
- Any criticisms or limitations?
- Overall tone

Return ONLY a JSON object:
{{
    "sentiment": "positive",
    "reasoning": "Brief explanation"
}}
"""
                
                success, response, error = invoke_chatgpt(prompt)
                
                if success:
                    try:
                        result = json.loads(response)
                        sentiment_value = result.get('sentiment', 'neutral')
                        reasoning = result.get('reasoning', '')
                        
                        SentimentScore.objects.create(
                            mention=mention,
                            sentiment=sentiment_value,
                            reasoning=reasoning,
                            confidence=1.0
                        )
                    except json.JSONDecodeError:
                        # Fallback to neutral
                        SentimentScore.objects.create(
                            mention=mention,
                            sentiment='neutral',
                            reasoning='Failed to parse sentiment',
                            confidence=0.5
                        )
                else:
                    # Fallback to neutral on error
                    SentimentScore.objects.create(
                        mention=mention,
                        sentiment='neutral',
                        reasoning=f'Error: {error}',
                        confidence=0.3
                    )
                    
            except Exception as e:
                logger.exception(f"Error analyzing sentiment for mention {mention.id}")
    
    def calculate_scores(self):
        """Calculate visibility scores for all brands"""
        all_brands = [self.brand_name] + self.competitor_names
        
        # Get all successful responses
        total_responses = PromptResponse.objects.filter(
            project=self.project,
            status='success'
        ).count()
        
        if total_responses == 0:
            logger.warning("No successful responses to calculate scores")
            return
        
        # Get selected models for weighting
        selected_models = {
            ms.model.name: ms.model.weight 
            for ms in self.project.selected_models.filter(is_selected=True)
        }
        
        for brand in all_brands:
            try:
                score = self._calculate_brand_score(
                    brand, 
                    total_responses, 
                    selected_models
                )
                
                is_main = (brand.lower() == self.brand_name.lower())
                competitor_obj = None
                
                if not is_main:
                    competitor_obj = self.project.competitors.filter(
                        name__iexact=brand
                    ).first()
                
                VisibilityScore.objects.update_or_create(
                    project=self.project,
                    brand_name=brand,
                    defaults={
                        'is_main_brand': is_main,
                        'competitor': competitor_obj,
                        **score
                    }
                )
                
            except Exception as e:
                logger.exception(f"Error calculating score for brand {brand}")
    
    def _calculate_brand_score(
        self, 
        brand: str, 
        total_responses: int,
        model_weights: Dict[str, float]
    ) -> Dict:
        """Calculate all metrics for a single brand"""
        
        mentions = BrandMention.objects.filter(
            response__project=self.project,
            brand_name__iexact=brand
        ).select_related('response', 'sentiment')
        
        if not mentions.exists():
            return {
                'frequency_score': 0.0,
                'prominence_score': 0.0,
                'sentiment_score': 0.0,
                'model_coverage_score': 0.0,
                'raw_score': 0.0,
                'normalized_score': 0.0,
                'total_mentions': 0,
                'prompts_appeared_in': 0
            }
        
        # 1. FREQUENCY: How many prompts mention this brand
        unique_prompts = mentions.values('response__prompt').distinct().count()
        total_prompts = self.project.prompts.filter(is_selected=True).count()
        frequency_score = unique_prompts / total_prompts if total_prompts > 0 else 0
        
        # 2. PROMINENCE: Average position score (1/position)
        prominence_scores = []
        for mention in mentions:
            prominence_scores.append(1.0 / mention.position)
        prominence_score = sum(prominence_scores) / len(prominence_scores) if prominence_scores else 0
        
        # 3. SENTIMENT: Weighted average
        sentiment_scores = []
        for mention in mentions:
            if hasattr(mention, 'sentiment'):
                weight = mention.sentiment.get_weight()
                sentiment_scores.append(weight)
        sentiment_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.8
        
        # 4. MODEL COVERAGE: Weighted by model importance
        model_coverage_scores = []
        for mention in mentions:
            model_name = mention.response.model.name
            weight = model_weights.get(model_name, 1.0)
            model_coverage_scores.append(weight)
        model_coverage_score = sum(model_coverage_scores) / len(model_coverage_scores) if model_coverage_scores else 0
        
        # AGGREGATE SCORE
        raw_score = (
            frequency_score * 
            prominence_score * 
            sentiment_score * 
            model_coverage_score
        )
        
        # Normalize to 0-100 scale
        # Maximum possible score would be 1.0 * 1.0 * 1.2 * 1.0 = 1.2
        # We'll normalize by assuming max is ~1.0 for practical purposes
        normalized_score = min(raw_score * 100, 100)
        
        return {
            'frequency_score': frequency_score,
            'prominence_score': prominence_score,
            'sentiment_score': sentiment_score,
            'model_coverage_score': model_coverage_score,
            'raw_score': raw_score,
            'normalized_score': normalized_score,
            'total_mentions': mentions.count(),
            'prompts_appeared_in': unique_prompts
        }


def run_module2(project_id: int) -> bool:
    """Execute Module 2 workflow"""
    engine = VisibilityCheckEngine(project_id)
    return engine.run()
