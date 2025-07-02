from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers
from modules.produtor.controllers.produtor_controller import router as produtor_router
from modules.propriedade.controllers.propriedade_controller import router as propriedade_router
from modules.cultura.controllers.cultura_controller import router as cultura_router
from modules.safra.controllers.safra_controller import router as safra_router
from modules.dashboard.controllers.dashboard_controller import router as dashboard_router

app = FastAPI(title="Cadastro de Produtores Rurais")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(produtor_router)
app.include_router(propriedade_router)
app.include_router(cultura_router)
app.include_router(safra_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "API de Cadastro de Produtores Rurais"} 