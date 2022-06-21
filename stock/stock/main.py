from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi_versioning import VersionedFastAPI, version
import stock.schemas as schemas
import stock.models as models
from stock.database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)


print("Hello from api")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/product/{product_id}", status_code=200)
@version(1)
async def product(product_id: int, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with the id {product_id} is not available")
    return product


@app.get("/products/")
@version(1)
async def products(provider: int = None, type: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if provider and type:
        products = db.query(models.Product).filter(
            models.Product.provider_id == provider, models.Product.type == type).all()
    elif provider:
        products = db.query(models.Product).filter(
            models.Product.provider_id == provider).all()
    elif type:
        products = db.query(models.Product).filter(
            models.Product.type == type).all()
    else:
        products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@app.post("/product/", status_code=status.HTTP_201_CREATED)
@version(1)
async def product(product: schemas.Product, response: Response, db: Session = Depends(get_db)):
    provider = db.query(models.Provider).filter(
        models.Provider.id == product.provider_id).first()
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Provider with the id {product.provider_id} is not available")
    new_product = models.Product(name=product.name,
                                 location=product.location,
                                 price=product.price,
                                 quantity=product.quantity,
                                 type=product.type,
                                 provider_id=product.provider_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/product/{product_id}", status_code=status.HTTP_202_ACCEPTED)
@version(1)
async def product(product_id: int, product: schemas.UpdateProduct, db: Session = Depends(get_db)):
    update_product = db.query(models.Product).filter(
        models.Product.id == product_id)
    if not update_product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with the id {product_id} is not available")

    if product.name:
        update_product.update({'name': product.name})
    if product.location:
        update_product.update({'location': product.location})
    if product.price:
        update_product.update({'price': product.price})
    if product.quantity:
        update_product.update({'quantity': product.quantity})
    if product.type:
        update_product.update({'type': product.type})
    if product.provider_id:
        update_product.update({'provider_id': product.provider_id})
    db.commit()
    return {"update": product_id}


@app.delete("/product/{product_id}", status_code=status.HTTP_200_OK)
@version(1)
async def product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with the id {product_id} is not available")
    product.delete(synchronize_session=False)
    db.commit()
    return {"deleted": f"Product whit the id: {product_id}"}


@app.post("/provider/", status_code=status.HTTP_201_CREATED)
@version(1)
async def provider(provider: schemas.Provider,  db: Session = Depends(get_db)):
    new_provider = models.Provider(name=provider.name,
                                   contact=provider.contact,
                                   mail=provider.mail)
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider


@app.get("/provider/{provider_id}", status_code=200)
@version(1)
async def product(provider_id: int, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Provider).filter(
        models.Provider.id == provider_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Provider with the id {provider_id} is not available")
    return product


@app.get("/providers/")
@version(1)
async def providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    providers = db.query(models.Provider).offset(skip).limit(limit).all()
    return providers


@app.put("/provider/{provider_id}", status_code=status.HTTP_202_ACCEPTED)
@version(1)
async def provider(provider_id: int, provider: schemas.UpdateProvider, db: Session = Depends(get_db)):
    update_provider = db.query(models.Provider).filter(
        models.Provider.id == provider_id)
    if not update_provider.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with the id {provider_id} is not available")

    if provider.name:
        update_provider.update({'name': provider.name})
    if provider.contact:
        update_provider.update({'contact': provider.contact})
    if provider.mail:
        update_provider.update({'mail': provider.mail})
    db.commit()
    return {"update": provider_id}


@app.delete("/provider/{provider_id}", status_code=status.HTTP_200_OK)
@version(1)
async def product(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(models.Provider).filter(
        models.Provider.id == provider_id)
    if not provider.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with the id {provider_id} is not available")
    product = db.query(models.Product).filter(
        models.Product.provider_id == provider_id)
    if product.first():
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Provider {provider_id} has associated products")
    provider.delete(synchronize_session=False)
    db.commit()
    return {"deleted": f"Provider whit the id: {provider_id}"}

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}')
