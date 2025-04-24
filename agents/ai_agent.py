import openai
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    GEMINI_API_KEY
)
from utils.logger import logger
from utils.data_models import AIResult

class AzureWrapper:
    def __init__(self):
        openai.api_type = "azure"
        openai.api_base = AZURE_OPENAI_ENDPOINT
        openai.api_key = AZURE_OPENAI_KEY
        self.deployment = AZURE_OPENAI_DEPLOYMENT

    def generate_response(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                engine=self.deployment,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Azure OpenAI error: {e}")
            raise

class GeminiWrapper:
    def __init__(self):
        openai.api_key = GEMINI_API_KEY
        self.model = "gemini-1.5-turbo"

    def generate_response(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise

class AIAgent:
    def __init__(self):
        self.azure = AzureWrapper()
        self.gemini = GeminiWrapper()

    def analyze(self, data) -> AIResult:
        """
        Analyze market data using AI models with fallback
        """
        try:
            response = self.azure.generate_response(self._format_prompt(data))
            return AIResult(
                analysis=response,
                source="azure",
                confidence=0.9
            )
        except Exception as e:
            logger.warning(f"Azure analysis failed, falling back to Gemini: {e}")
            try:
                response = self.gemini.generate_response(self._format_prompt(data))
                return AIResult(
                    analysis=response,
                    source="gemini",
                    confidence=0.7
                )
            except Exception as e:
                logger.error(f"Both AI services failed: {e}")
                raise

    def _format_prompt(self, data) -> str:
        """
        Format market data into a prompt for AI analysis
        """
        return f"""
        Analyze the following market data and provide trading insights:
        Symbol: {data.get('symbol')}
        Current Price: {data.get('price')}
        Volume: {data.get('volume')}
        Technical Indicators: {data.get('indicators')}
        
        Please provide:
        1. Market sentiment
        2. Key support/resistance levels
        3. Trading recommendation
        """ 