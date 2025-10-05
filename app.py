from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import os
import time
from agents.researcher import ResearchAgent
from agents.analyst import AnalystAgent
from agents.critic import CriticAgent
from agents.synthesizer import SynthesizerAgent
import markdown
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize agents
researcher = ResearchAgent()
analyst = AnalystAgent()
critic = CriticAgent()
synthesizer = SynthesizerAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/research', methods=['POST'])
def research():
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        depth = data.get('depth', 'comprehensive')
        include_media = data.get('include_media', False)
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        # Multi-agent pipeline
        results = {
            "topic": topic,
            "stages": [],
            "total_time": 0
        }
        
        start_time = time.time()
        
        # Stage 1: Research
        print(f"🔍 Stage 1: Researching '{topic}' with {depth} depth...")
        research_result = researcher.research_topic(topic, depth)
        results["stages"].append({
            "name": "Research",
            "agent": "Research Agent",
            "output": research_result['research']
        })
        
        # Stage 2: Analysis
        print(f"📊 Stage 2: Analyzing research...")
        analysis_result = analyst.analyze_research(research_result)
        results["stages"].append({
            "name": "Analysis",
            "agent": "Analyst Agent",
            "output": analysis_result['analysis']
        })
        
        # Stage 3: Critique
        print(f"🎯 Stage 3: Critical review...")
        critique_result = critic.critique_analysis(analysis_result)
        results["stages"].append({
            "name": "Critique",
            "agent": "Critic Agent",
            "output": critique_result['critique']
        })
        
        # Stage 4: Synthesis
        print(f"✨ Stage 4: Synthesizing final report...")
        synthesis_result = synthesizer.synthesize_all(
            research_result,
            analysis_result,
            critique_result
        )
        results["stages"].append({
            "name": "Final Synthesis",
            "agent": "Synthesizer Agent",
            "output": synthesis_result['final_report']
        })
        
        # Generate media suggestions if requested
        if include_media:
            print(f"🎬 Generating media suggestions...")
            media_suggestions = researcher.generate_media_suggestions(topic)
            results["media"] = media_suggestions
        
        results["total_time"] = time.time() - start_time
        results["final_report"] = synthesis_result['final_report']
        
        # Save to file
        filename = f"outputs/report_{int(time.time())}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Research Intelligence Report: {topic}\n\n")
            f.write(f"Generated: {synthesis_result['timestamp']}\n\n")
            f.write(f"Total Processing Time: {results['total_time']:.2f}s\n\n")
            f.write(f"Research Depth: {depth}\n\n")
            f.write("---\n\n")
            f.write(synthesis_result['final_report'])
        
        results["download_file"] = filename
        
        print(f"✅ Complete! Total time: {results['total_time']:.2f}s")
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/related-topics', methods=['POST'])
def related_topics():
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        
        topics = researcher.find_related_topics(topic, count=5)
        return jsonify({"topics": topics})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs('outputs', exist_ok=True)
    print("🚀 Starting Cerebras Research Intelligence System...")
    print("⚡ Powered by Cerebras ultra-fast inference")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)