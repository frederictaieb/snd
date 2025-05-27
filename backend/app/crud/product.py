from sqlmodel import Session, select

from app.db.db_setup import engine
from app.models.product import Product, ProductCreate, ProductUpdate


def post_product(session: Session, product: ProductCreate) -> Product:
    db_product = Product.model_validate(product) 
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def get_product(session: Session, product_name: str) -> Product | None:
    query = select(Product).where(Product.name == product_name, Product.is_deleted == False)
    return session.exec(query).first()


def get_all_products(session: Session) -> list[Product]:
    query = select(Product).where(Product.is_deleted == False)
    return list(session.exec(query).all())


def update_product(session: Session, product_name: str, product_update: ProductUpdate) -> Product | None:
    db_product = get_product(session, product_name)
    if not db_product:
        return None
    
    product_data = product_update.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def delete_product(session: Session, product_name: str) -> Product | None:
    product = get_product(session, product_name)
    if not product:
        return None
    
    product.is_deleted = True
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def hard_delete_product(session: Session, product_name: str) -> dict:
    query = select(Product).where(Product.name == product_name)
    product_to_delete = session.exec(query).first()

    if not product_to_delete:
        return {"message": "Product not found"}
    
    session.delete(product_to_delete)
    session.commit()
    return {"message": f"Product '{product_name}' permanently deleted"}