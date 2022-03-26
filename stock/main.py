from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI()

class Provider(BaseModel):
    name: str
    contact: int
    mail: str

class Product(BaseModel):
    name: str
    id: int
    location: str
    price: int
    quantity: int
    type: str
    provider: Provider

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    price: Optional[int] = int
    quantity: Optional[int] = int
    type: Optional[str] = None
    provider: Optional[Provider] = None

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
async def product(product: Product):
    return {"return": product.id }

@app.put("/product/{product_id}")
@version(1)
async def product(product_id: int, product: UpdateProduct):
    return {"update": product_id}

@app.delete("/product/{product_id}")
@version(1)
async def product(product_id: int):
    return{"delete": product_id}

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')