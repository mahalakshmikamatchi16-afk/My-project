# Full Single App version also included for redundancy
import os
import re
import json
import torch
import traceback
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from diffusers import StableDiffusionPipeline
from fpdf import FPDF

load_dotenv()
app = FastAPI()
# ... 
