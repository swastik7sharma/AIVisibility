"""
LangChain configuration and model setup
"""
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings
import time
import logging

logger = logging.getLogger(__name__)


class AIModelConfig:
    """Configuration for AI models with retry logic"""
    
    MAX_RETRIES = 3
    BASE_DELAY = 2  # seconds
    
    @staticmethod
    def get_openai_model(temperature=0.7):
        """Get configured OpenAI ChatGPT model"""
        return ChatOpenAI(
            model="gpt-4o",
            temperature=temperature,
            api_key=settings.OPENAI_API_KEY,
            request_timeout=60
        )
    
    @staticmethod
    def get_claude_model(temperature=0.7):
        """Get configured Claude model"""
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            api_key=settings.CLAUDE_API_KEY,
            timeout=60
        )
    
    @staticmethod
    def get_gemini_model(temperature=0.7):
        """Get configured Gemini model"""
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=temperature,
            google_api_key=settings.GEMINI_API_KEY,
            request_timeout=60
        )
    
    @staticmethod
    def get_model_by_name(model_name, temperature=0.7):
        """Get model instance by name"""
        model_map = {
            'chatgpt': AIModelConfig.get_openai_model,
            'claude': AIModelConfig.get_claude_model,
            'gemini': AIModelConfig.get_gemini_model,
        }
        
        model_func = model_map.get(model_name)
        if not model_func:
            raise ValueError(f"Unknown model: {model_name}")
        
        return model_func(temperature)
    
    @staticmethod
    def invoke_with_retry(model, prompt, max_retries=None):
        """
        Invoke model with exponential backoff retry logic
        
        Returns: (success: bool, response: str, error: str)
        """
        if max_retries is None:
            max_retries = AIModelConfig.MAX_RETRIES
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = model.invoke(prompt)
                return True, response.content, None
                
            except Exception as e:
                last_error = str(e)
                error_lower = last_error.lower()
                
                # Check for rate limit or quota errors
                if any(term in error_lower for term in ['rate limit', 'quota', 'timeout', 'temporary']):
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        delay = AIModelConfig.BASE_DELAY * (2 ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed: {last_error}. Retrying in {delay}s...")
                        time.sleep(delay)
                        continue
                
                # Non-retryable error
                logger.error(f"Non-retryable error: {last_error}")
                return False, "", last_error
        
        # All retries exhausted
        logger.error(f"All {max_retries} retries exhausted. Last error: {last_error}")
        return False, "", last_error


# Convenience functions
def get_chatgpt():
    """Get primary reasoning model (currently Gemini)"""
    return AIModelConfig.get_gemini_model()


def invoke_chatgpt(prompt):
    """Invoke primary reasoning model with retry logic (currently Gemini)"""
    model = get_chatgpt()
    return AIModelConfig.invoke_with_retry(model, prompt)
