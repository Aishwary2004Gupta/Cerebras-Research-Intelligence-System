from utils.cerebras_client import CerebrasClient
from typing import Dict

class AnalystAgent:
    def __init__(self):
        self.client = CerebrasClient()
        self.name = "Analyst Agent"
        
    def analyze_research(self, research_data: Dict) -> Dict:
        """Analyze research data and extract insights"""
        
        topic = research_data.get('topic', 'Unknown')
        research = research_data.get('research', '')
        
        prompt = f"""You are an expert analyst. Analyze the following research on "{topic}":

{research}

Provide a detailed analysis including:

1. **Key Insights**: What are the most important takeaways?
2. **Strengths**: What aspects are well-covered and strong?
3. **Gaps**: What's missing or could be explored further?
4. **Implications**: What are the practical implications?
5. **Data Quality**: Assess the depth and breadth of the research
6. **Recommendations**: What actions or further research would you recommend?

Be critical, objective, and thorough."""

        messages = [
            {"role": "system", "content": "You are an expert analytical agent specializing in research evaluation."},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.client.generate_response(messages, temperature=0.4)
        
        return {
            "agent": self.name,
            "topic": topic,
            "analysis": analysis,
            "original_research": research
        }
    
    def extract_key_points(self, text: str, max_points: int = 10) -> list:
        """Extract key points from text"""
        
        prompt = f"""Extract the {max_points} most important key points from the following text:

{text}

Format each point as a clear, concise bullet point."""

        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.generate_response(messages, temperature=0.3)
        points = [line.strip() for line in response.split('\n') if line.strip() and (line.strip().startswith('-') or line.strip().startswith('•'))]
        
        return points