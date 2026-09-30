import os
import google.generativeai as genai

def generate_story(outline: list) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: System context parameters lack a verified GEMINI_API_KEY node."
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    formatted_items = []
    for item in outline:
        panel_num = item.get("panel", "?")
        title = item.get("title", "Untitled")
        desc = item.get("scene_description", "")
        formatted_items.append(f"Panel {panel_num}: '{title}' context coordinates description: {desc}")
        
    formatted_outline = "\n".join(formatted_items)
    
    prompt = f"""
You are an expert comic book scriptwriter.
Expand the structured layout mapping parameters into continuous storytelling transcripts featuring descriptive narrations and character dialogue lines.

Panel Sequence Target Framework:
{formatted_outline}

Guidelines:
- Maintain high thematic cohesion across continuous layout panels.
- For each section, begin with the exact line format "**Panel X" where X matches the sequence index number.
- Explicitly output clear components labels inside panels like: **CAPTION:**, **NARRATION:**, and character dialog strings.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error executing context creation routines: {str(e)}"
