from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.product import (
    delete_product,
    get_all_products,
    get_product,
    post_product,
    update_product,
    hard_delete_product
)
from app.db.db_setup import get_session
from app.models.product import Product, ProductCreate, ProductUpdate

router = APIRouter(
    tags=["products"], 
    responses={404: {"description": "No products found, sorry!"}}
)

@router.post("/products/", response_model=Product, status_code=201)
def create(product: ProductCreate, session: Session = Depends(get_session)) -> Product:
    new_product = Product.model_validate(product)
    return post_product(session, new_product)


@router.get("/products/{product_name}", response_model=Product, status_code=200)
def get_by_name(product_name: str, session: Session = Depends(get_session)) -> Product:
    product = get_product(session, product_name)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or has been deleted")
    return product

@router.get("/products/", response_model=list[Product], status_code=200)
def get_all(session: Session = Depends(get_session)) -> list[Product]:
    products = get_all_products(session)
    return products

@router.patch("/products/{product_name}", response_model=Product, status_code=200)
def update(product_name: str, product_update: ProductUpdate, session: Session = Depends(get_session)) -> Product:
    updated_product = update_product(session, product_name, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or has been deleted")
    return updated_product

@router.delete("/products/{product_name}", response_model=Product, status_code=200)
def remove_product(product_name: str, session: Session = Depends(get_session)) -> Product:
    """
    Soft delete a product.
    """
    deleted_product = delete_product(session, product_name)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found or already soft-deleted")
    return deleted_product

@router.delete("/products/{product_name}/permanent", status_code=200)
async def permanently_remove_product(product_name: str, session: Session = Depends(get_session)) -> dict:
    """
    Permanently delete a product from the database.
    Use with caution.
    """
    result = hard_delete_product(session, product_name)
    if "not found" in result.get("message", "").lower():
        raise HTTPException(status_code=404, detail=result.get("message", "Product not found"))
    return result