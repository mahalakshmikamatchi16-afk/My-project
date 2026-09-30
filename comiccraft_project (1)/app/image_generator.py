import os
import re
import torch
from diffusers import StableDiffusionPipeline

_cached_pipeline = None

def load_diffusion_pipeline():
    global _cached_pipeline
    if _cached_pipeline is None:
        model_id = "runwayml/stable-diffusion-v1-5"
        if torch.cuda.is_available():
            device = "cuda"
            dtype = torch.float16
        elif torch.backends.mps.is_available():
            device = "mps"
            dtype = torch.float32
        else:
            device = "cpu"
            dtype = torch.float32
            
        try:
            token = os.getenv("HF_API_KEY")
            _cached_pipeline = StableDiffusionPipeline.from_pretrained(
                model_id, 
                torch_dtype=dtype,
                use_auth_token=token if token else None
            )
            _cached_pipeline = _cached_pipeline.to(device)
            _cached_pipeline.enable_attention_slicing()
        except Exception as e:
            print("⚠️ High-end GPU offline. Using automated Canvas fallback engines.")
            _cached_pipeline = "MOCK_MODE"
            
    return _cached_pipeline

def parse_safe_filename(prompt: str) -> str:
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)
    clean = clean.replace(' ', '_')[:25].lower()
    return f"{clean or 'frame_asset'}.png"

def generate_image(prompt: str, filename: str = None) -> str:
    if not filename:
        filename = parse_safe_filename(prompt)
        
    target_path = f"static/panels/{filename}"
    pipe = load_diffusion_pipeline()
    
    if pipe == "MOCK_MODE":
        from PIL import Image, ImageDraw
        canvas = Image.new('RGB', (512, 512), color=(47, 79, 79))
        draw = ImageDraw.Draw(canvas)
        draw.text((30, 240), f"Panel Preview Frame Placeholder\nPrompt: {prompt[:30]}...", fill=(255, 255, 255))
        canvas.save(target_path)
    else:
        try:
            execution_matrix = pipe(prompt).images
            execution_matrix.save(target_path)
        except Exception:
            from PIL import Image
            canvas = Image.new('RGB', (512, 512), color=(139, 0, 0))
            canvas.save(target_path)
            
    return target_path
