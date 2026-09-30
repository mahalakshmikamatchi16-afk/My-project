import re

def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    segmented_data = re.split(r'\*\*Panel\s*\d+[:\s]*', full_story, flags=re.IGNORECASE)
    cleaned_segments = [seg.strip() for seg in segmented_data if seg.strip()]
    
    while len(cleaned_segments) < len(outline):
        cleaned_segments.append("Narration context tracking records trace incomplete.")
        
    integrated_layout = []
    for idx, (img, narrative, meta) in enumerate(zip(image_paths, cleaned_segments, outline), start=1):
        integrated_layout.append({
            "panel": idx,
            "title": meta.get("title", f"Segment Sequence Frame {idx}"),
            "image_path": img,
            "text": narrative,
            "scene_description": meta.get("scene_description", ""),
            "image_prompt": meta.get("image_prompt", "")
        })
        
    return integrated_layout
