from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version
import schemas, models
from database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/product/{product_id}")
@version(1)
async def product(product_id: int):
    return {"message": "produto"}

@app.get("/products/")
@version(1)
async def products(provider: str=None, type: str=None, skip: int=0, limit: int=None):
    return {"return": f"lista de produtos"}

@app.get("/providers/")
@version(1)
async def products(provider: str=None, skip: int=0, limit: int=None):
    return {"return": f"lista de fornecedores"}

@app.post("/product/")
@version(1)
async def product(product: schemas.Product):
    return {"return": product.id }

@app.put("/product/{product_id}")
@version(1)
async def product(product_id: int, product: schemas.UpdateProduct):
    return {"update": product_id}

@app.delete("/product/{product_id}")
@version(1)
async def product(product_id: int):
    return{"delete": product_id}

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')