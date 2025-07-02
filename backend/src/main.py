from fastapi import FastAPI

app = FastAPI(title="Cadastro de Produtores Rurais")

@app.get("/")
def root():
    return {"message": "API de Cadastro de Produtores Rurais"} 