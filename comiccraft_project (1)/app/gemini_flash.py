import json
import os
import google.generativeai as genai

def generate_outline(user_prompt: str) -> list:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("System configurations lack valid GEMINI_API_KEY tokens.")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
You are a professional AI comic planner.
Your task is to generate a *strictly formatted* JSON array containing exactly 5 panel descriptions for a comic book strip layout based on the user criteria provided below:

STORY IDEA INPUT TRACE: "{user_prompt}"

Each JSON structure object block must include the exact configuration data mapping parameters defined here:
- "panel" (integer)
- "title" (string)
- "scene_description" (string)
- "image_prompt" (string)

CRITICAL: Return raw unformatted plain text valid JSON format array sequence ONLY. 
Do NOT surround outputs with markdown character flags, backticks, or comment blocks.
"""

    try:
        response = model.generate_content(prompt)
        output_text = response.text.strip()
        
        if output_text.startswith("```json"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()
        elif output_text.startswith("```"):
            output_text = output_text.replace("```", "").strip()
            
        panel_data = json.loads(output_text)
        return panel_data
    except Exception as e:
        print("❌ Unexpected runtime error on model interaction node:", e)
        return [{"error": f"Generation failed: {str(e)}"}]
