from utils.cerebras_client import CerebrasClient
from typing import Dict, List
import time

class SynthesizerAgent:
    def __init__(self):
        self.client = CerebrasClient()
        self.name = "Synthesizer Agent"
        
    def synthesize_all(self, research: Dict, analysis: Dict, critique: Dict) -> Dict:
        """Synthesize all agent outputs into a comprehensive report"""
        
        topic = research.get('topic', 'Unknown')
        
        prompt = f"""You are a master synthesizer. Create a comprehensive, well-structured report on "{topic}" by synthesizing the following inputs:

RESEARCH FINDINGS:
{research.get('research', '')[:2000]}

ANALYTICAL INSIGHTS:
{analysis.get('analysis', '')[:2000]}

CRITICAL REVIEW:
{critique.get('critique', '')[:2000]}

Create a FINAL COMPREHENSIVE REPORT with:

# {topic}: Intelligence Report

## Executive Summary
[Brief overview of key findings]

## Core Findings
[Synthesized research insights]

## Strategic Insights
[Analysis highlights and implications]

## Critical Considerations
[Important critiques and alternative perspectives]

## Recommendations
[Actionable recommendations]

## Conclusion
[Final synthesis and outlook]

Make it cohesive, well-organized, and actionable."""

        messages = [
            {"role": "system", "content": "You are an expert synthesis agent that creates comprehensive, executive-level reports."},
            {"role": "user", "content": prompt}
        ]
        
        start_time = time.time()
        synthesis = self.client.generate_response(messages, temperature=0.6, max_tokens=3000)
        synthesis_time = time.time() - start_time
        
        return {
            "agent": self.name,
            "topic": topic,
            "final_report": synthesis,
            "synthesis_time": synthesis_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }