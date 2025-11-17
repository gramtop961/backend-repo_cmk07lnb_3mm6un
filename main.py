import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import MenuItem, Order

app = FastAPI(title="Tutti Amici API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Tutti Amici API"}


# Utility to convert Mongo docs

def serialize_doc(doc):
    doc["id"] = str(doc.pop("_id"))
    return doc


# Menu endpoints
@app.post("/api/menu", status_code=201)
def create_menu_item(item: MenuItem):
    try:
        item_id = create_document("menuitem", item)
        return {"id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/menu")
def list_menu_items(category: Optional[str] = None):
    try:
        filt = {"category": category} if category else None
        items = get_documents("menuitem", filt)
        return [serialize_doc(i) for i in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Orders
@app.post("/api/orders", status_code=201)
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orders")
def list_orders(status: Optional[str] = None):
    try:
        filt = {"status": status} if status else None
        orders = get_documents("order", filt)
        return [serialize_doc(o) for o in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
