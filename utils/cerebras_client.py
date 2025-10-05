import os
from cerebras.cloud.sdk import Cerebras
from typing import List, Dict, Optional
import time

class CerebrasClient:
    def __init__(self):
        self.api_key = os.getenv('CEREBRAS_API_KEY')
        if not self.api_key:
            raise ValueError("CEREBRAS_API_KEY not found in environment variables")
        
        self.client = Cerebras(api_key=self.api_key)
        self.model = os.getenv('MODEL_NAME', 'llama3.1-8b')
        
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> str:
        """Generate a response using Cerebras API"""
        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            end_time = time.time()
            
            if stream:
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                return full_response
            else:
                content = response.choices[0].message.content
                
            inference_time = end_time - start_time
            print(f"⚡ Inference time: {inference_time:.2f}s")
            
            return content
            
        except Exception as e:
            print(f"Error generating response: {e}")
            raise
    
    def generate_streaming_response(self, messages: List[Dict[str, str]], temperature: float = 0.7):
        """Generate streaming response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2048,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error in streaming: {e}")
            raise