import traceback
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class ComicAPIRequest(BaseModel):
    prompt: str
    character_name: str
    setting: str
    tone: str
    style: str

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

@router.get("/", response_class=HTMLResponse)
async def serve_home_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def pipeline_generate_web(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    try:
        execution_prompt_instruction = (
            f"The Story Context Prompt Instruction: {prompt}\n"
            f"Character target focus: {character_name}. Environmental scenario coordinates: {setting}. "
            f"Narrative emotional configuration matrix: {tone}. Art Style configuration visual directive: {style}."
        )
        
        outline = generate_outline(execution_prompt_instruction)
        full_story = generate_story(outline)
        
        rendered_images = []
        for panel in outline:
            path = generate_image(f"{panel['image_prompt']}, rendered using {style} aesthetic guidelines")
            rendered_images.append(path)
            
        layout = build_comic_layout(rendered_images, full_story, outline)
        pdf_storage_path = save_pdf(layout)
        
        web_accessible_pdf = "/" + pdf_storage_path.replace("\\", "/")
        
        return templates.TemplateResponse("comic_preview.html", {
            "request": request,
            "layout": layout,
            "pdf_path": web_accessible_pdf
        })
    except Exception as general_fault:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(general_fault))

@router.get("/export-success", response_class=HTMLResponse)
async def serve_success_confirmation(request: Request, pdf_path: str):
    return templates.TemplateResponse("export_success.html", {
        "request": request, 
        "pdf_path": pdf_path
    })
