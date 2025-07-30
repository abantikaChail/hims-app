from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.models import User
from sqlalchemy.orm import Session
from app.database import get_db
from passlib.context import CryptContext
from starlette.status import HTTP_303_SEE_OTHER
from app.crud import (
    get_inventory_count,
    get_all_inventory,
    get_inventory_paginated,
    add_inventory_item,
    search_inventory,
    update_inventory_item_if_changed,
    delete_inventory_item,
    get_inventory_summary_by_type,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/login")
def login_page(request: Request):
    error = request.session.pop("error", None)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error, "username": "", "password": ""},
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.hashed_password):
        request.session["user"] = user.username
        return RedirectResponse(url="/home", status_code=HTTP_303_SEE_OTHER)
    else:
        request.session["error"] = "Invalid username or password"
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)


@router.get("/home")
def home(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    dark_mode = request.session.get("dark_mode", False)
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "user": {"username": user}, "dark_mode": dark_mode},
    )


@router.get("/insights")
def insights(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)

    data = get_inventory_summary_by_type(db)

    labels = [item[0] for item in data]
    values = [item[1] for item in data]

    return templates.TemplateResponse(
        "insights.html",
        {
            "request": request,
            "user": {"username": user},
            "labels": labels,
            "values": values,
        },
    )


@router.get("/add_data")
def add_data(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    items = get_all_inventory(db)
    return templates.TemplateResponse(
        "add.html", {"request": request, "user": {"username": user}, "items": items}
    )


@router.post("/add_data/add")
def add_item(
    request: Request,
    name: str = Form(...),
    quantity: int = Form(...),
    item_type: str = Form(...),
    db: Session = Depends(get_db),
):
    add_inventory_item(db, name, quantity, item_type)
    request.session["item_added"] = True
    return RedirectResponse("/add_data", status_code=HTTP_303_SEE_OTHER)


@router.get("/search")
def search(
    request: Request,
    query: str = Query(default=None),
    page: int = 1,
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    per_page = 5

    if query:
        all_matched = search_inventory(db, query)
        total = len(all_matched)
        items = all_matched[(page - 1) * per_page : page * per_page]
    else:
        total = get_inventory_count(db)
        items = get_inventory_paginated(db, skip=(page - 1) * per_page, limit=per_page)

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "items": items,
            "user": {"username": user},
            "page": page,
            "total_pages": (total + per_page - 1) // per_page,
            "toast": request.session.pop("toast", None),
            "query": query,
        },
    )


@router.post("/search/update/{item_id}")
def update_item(
    item_id: int,
    name: str = Form(...),
    quantity: int = Form(...),
    item_type: str = Form(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    result = update_inventory_item_if_changed(db, item_id, name, quantity, item_type)

    if result == "updated":
        request.session["toast"] = {
            "message": "Item updated successfully!",
            "icon": "success",
        }
    elif result == "no_change":
        request.session["toast"] = {"message": "No values updated.", "icon": "info"}
    else:
        request.session["toast"] = {"message": "Item not found.", "icon": "error"}

    return RedirectResponse("/search", status_code=303)


@router.get("/search/delete/{item_id}")
def delete_inventory(item_id: int, request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    success = delete_inventory_item(db, item_id)
    if success:
        request.session["toast"] = {
            "icon": "success",
            "message": "Item successfully deleted",
        }
    else:
        request.session["toast"] = {"icon": "error", "message": "Item not found"}

    return RedirectResponse(url="/search", status_code=303)
