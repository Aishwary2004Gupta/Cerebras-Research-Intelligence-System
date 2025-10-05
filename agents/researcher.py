from utils.cerebras_client import CerebrasClient
from typing import Dict, List

class ResearchAgent:
    def __init__(self):
        self.client = CerebrasClient()
        self.name = "Research Agent"
        
    def research_topic(self, topic: str, depth: str = "comprehensive") -> Dict:
        """Conduct initial research on a topic"""
        
        # Adjust prompt based on depth
        depth_instructions = {
            "quick": "Provide a concise overview focusing on the most important 3-5 key points.",
            "comprehensive": "Provide detailed, thorough research covering all major aspects.",
            "deep": "Provide exhaustive, in-depth research with extensive details, examples, and analysis."
        }
        
        instruction = depth_instructions.get(depth, depth_instructions["comprehensive"])
        
        prompt = f"""You are an expert research agent. {instruction}

Topic: {topic}

Provide:
1. **Overview and Definition**: Clear explanation of what this is
2. **Key Concepts and Principles**: Core ideas and fundamentals
3. **Current State and Recent Developments**: Latest trends and updates (2024)
4. **Important Facts and Statistics**: Data-driven insights
5. **Main Challenges and Opportunities**: What's difficult and what's possible
6. **Future Trends and Predictions**: Where this is heading

Be thorough, accurate, and insightful. Use concrete examples where applicable."""

        messages = [
            {"role": "system", "content": "You are an expert research agent specializing in comprehensive topic analysis with up-to-date knowledge."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.generate_response(messages, temperature=0.3, max_tokens=3000 if depth == "deep" else 2048)
        
        return {
            "agent": self.name,
            "topic": topic,
            "research": response,
            "depth": depth
        }
    
    def find_related_topics(self, topic: str, count: int = 5) -> List[str]:
        """Find related research topics"""
        
        prompt = f"""Given the topic: "{topic}"

List {count} closely related topics or subtopics that would be valuable to research further.
Provide only the topic names, one per line, without numbering or explanations."""

        messages = [
            {"role": "system", "content": "You are an expert at identifying related research topics."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.generate_response(messages, temperature=0.5)
        topics = [line.strip() for line in response.split('\n') if line.strip() and not line.strip().startswith('#')]
        
        return topics[:count]
    
    def generate_media_suggestions(self, topic: str) -> List[Dict]:
        """Generate suggestions for relevant images and videos"""
        
        prompt = f"""For the topic "{topic}", suggest 4 relevant visual content pieces that would enhance understanding:

Provide 2 image suggestions and 2 video suggestions.

Format each as:
TYPE: image or video
TITLE: Short descriptive title
DESCRIPTION: What this visual shows (one sentence)
SEARCH_QUERY: Exact search term to find this content

Example:
TYPE: image
TITLE: Quantum Computer Chip
DESCRIPTION: Close-up of a quantum computing processor showing qubits
SEARCH_QUERY: quantum computer chip close up

Provide 4 suggestions now:"""

        messages = [
            {"role": "system", "content": "You are an expert at identifying relevant visual content for educational topics."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.generate_response(messages, temperature=0.6)
        
        # Parse the response
        media_items = []
        current_item = {}
        
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('TYPE:'):
                if current_item:
                    media_items.append(current_item)
                current_item = {'type': line.split(':', 1)[1].strip()}
            elif line.startswith('TITLE:'):
                current_item['title'] = line.split(':', 1)[1].strip()
            elif line.startswith('DESCRIPTION:'):
                current_item['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('SEARCH_QUERY:'):
                current_item['query'] = line.split(':', 1)[1].strip()
        
        if current_item and len(current_item) >= 4:
            media_items.append(current_item)
        
        return media_items[:4]