from utils.cerebras_client import CerebrasClient
from typing import Dict

class CriticAgent:
    def __init__(self):
        self.client = CerebrasClient()
        self.name = "Critic Agent"
        
    def critique_analysis(self, analysis_data: Dict) -> Dict:
        """Provide critical review of the analysis"""
        
        topic = analysis_data.get('topic', 'Unknown')
        analysis = analysis_data.get('analysis', '')
        research = analysis_data.get('original_research', '')
        
        prompt = f"""You are a critical thinking expert. Review the following analysis on "{topic}":

ORIGINAL RESEARCH:
{research[:1000]}...

ANALYSIS:
{analysis}

Provide a critical review:

1. **Logical Consistency**: Are there any logical flaws or contradictions?
2. **Bias Detection**: Are there any apparent biases or one-sided views?
3. **Evidence Quality**: Is the reasoning well-supported?
4. **Alternative Perspectives**: What alternative viewpoints are missing?
5. **Assumptions**: What assumptions are being made?
6. **Overall Assessment**: Rate the quality and provide constructive feedback

Be constructively critical and help improve the analysis."""

        messages = [
            {"role": "system", "content": "You are an expert critical thinking agent specializing in logical analysis and bias detection."},
            {"role": "user", "content": prompt}
        ]
        
        critique = self.client.generate_response(messages, temperature=0.5)
        
        return {
            "agent": self.name,
            "topic": topic,
            "critique": critique
        }