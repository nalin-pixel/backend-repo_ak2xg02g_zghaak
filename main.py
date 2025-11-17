import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from database import create_document, get_documents
from schemas import Program, Event, ContactMessage, VolunteerApplication, Subscriber

app = FastAPI(title="Digital Literacy & Youth STEM Nonprofit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Nonprofit backend is running"}


# Public content endpoints
@app.get("/api/programs", response_model=List[Program])
def list_programs():
    try:
        docs = get_documents("program", {}, limit=50)
        # Convert Mongo documents to Program dicts, removing _id
        programs = []
        for d in docs:
            d.pop("_id", None)
            programs.append(Program(**d))
        return programs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events", response_model=List[Event])
def list_events():
    try:
        docs = get_documents("event", {}, limit=50)
        events: List[Event] = []
        for d in docs:
            d.pop("_id", None)
            events.append(Event(**d))
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Forms
@app.post("/api/contact")
def submit_contact(payload: ContactMessage):
    try:
        _id = create_document("contactmessage", payload)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/volunteer")
def submit_volunteer(payload: VolunteerApplication):
    try:
        _id = create_document("volunteerapplication", payload)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/subscribe")
def subscribe(payload: Subscriber):
    try:
        _id = create_document("subscriber", payload)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db

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

    except ImportError:
        response["database"] = "❌ Database module not found"
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
