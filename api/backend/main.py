from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse 
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

app = FastAPI()

# Configuração do CORS para permitir requisições do frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Monta a pasta frontend para servir arquivos estáticos
# app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Monta a pasta frontend para servir arquivos estáticos
app.mount("/styles", StaticFiles(directory="styles/build"), name="styles")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
def read_root():
    return FileResponse(Path(__file__).parent.parent / "frontend" / "index.html")

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = 'pt'
    target_lang: str = 'en'

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    url = "https://api.mymemory.translated.net/get"
    params = {
        'q': text,
        'langpair': f'{source_lang}|{target_lang}'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['responseData']['translatedText']
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro na API de tradução")

@app.post("/translate")
async def translate(request: TranslationRequest):
    translated_text = translate_text(request.text, request.source_lang, request.target_lang)
    return {"translated_text": translated_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
