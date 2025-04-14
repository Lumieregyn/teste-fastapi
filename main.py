from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import shutil, os
from processador import atualizar_estoques

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
RESULTADO_PATH = "resultado.xlsx"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
def processar_arquivos(estoque: UploadFile = File(...), produto: UploadFile = File(...)):
    estoque_path = os.path.join(UPLOAD_DIR, estoque.filename)
    produto_path = os.path.join(UPLOAD_DIR, produto.filename)

    with open(estoque_path, "wb") as buffer:
        shutil.copyfileobj(estoque.file, buffer)

    with open(produto_path, "wb") as buffer:
        shutil.copyfileobj(produto.file, buffer)

    atualizar_estoques(estoque_path, produto_path, RESULTADO_PATH)
    return FileResponse(RESULTADO_PATH, filename="planilha_atualizada.xlsx")
