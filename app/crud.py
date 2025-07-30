from sqlalchemy.orm import Session
from app.models import Inventory
from sqlalchemy import or_, func


def get_inventory_paginated(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Inventory).offset(skip).limit(limit).all()


def get_inventory_count(db: Session):
    return db.query(Inventory).count()


def get_all_inventory(db: Session):
    return db.query(Inventory).all()


def add_inventory_item(db: Session, name: str, quantity: int, item_type: str):
    item = Inventory(name=name, quantity=quantity, item_type=item_type)
    db.add(item)
    db.commit()
    return item


def update_inventory_item_if_changed(
    db: Session, item_id: int, name: str, quantity: int, item_type: str
) -> str:
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        return "not_found"

    changed = False
    if item.name != name:
        item.name = name
        changed = True
    if item.quantity != quantity:
        item.quantity = quantity
        changed = True
    if item.item_type != item_type:
        item.item_type = item_type
        changed = True

    if changed:
        db.commit()
        return "updated"
    else:
        return "no_change"


def delete_inventory_item(db: Session, item_id: int):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def search_inventory(db: Session, query: str):
    return (
        db.query(Inventory)
        .filter(
            or_(
                Inventory.name.ilike(f"%{query}%"),
                Inventory.item_type.ilike(f"%{query}%"),
            )
        )
        .all()
    )


def get_inventory_summary_by_type(db: Session):
    """
    Groups inventory items by item_type and returns aggregated quantity totals.
    """
    return (
        db.query(Inventory.item_type, func.sum(Inventory.quantity).label("total"))
        .group_by(Inventory.item_type)
        .all()
    )
