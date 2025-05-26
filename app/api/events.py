from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.event import EventCreate, EventRead, EventUpdate
from app.models.event import Event
from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User
from datetime import datetime, timedelta
from dateutil.rrule import rrulestr

router = APIRouter(prefix="/events", tags=["Events"])

# Helper to expand event occurrences in a window
def get_event_occurrences(event, window_start, window_end):
    occurrences = []
    if event.is_recurring and event.recurrence_pattern:
        rule = rrulestr(event.recurrence_pattern, dtstart=event.start_time)
        # Only get occurrences in the window
        for occ_start in rule.between(window_start, window_end, inc=True):
            occ_end = occ_start + (event.end_time - event.start_time)
            occurrences.append((occ_start, occ_end))
    else:
        # Non-recurring event
        if event.start_time <= window_end and event.end_time >= window_start:
            occurrences.append((event.start_time, event.end_time))
    return occurrences

# Helper to check for conflicts
def has_conflict(new_occurrences, existing_events, window_start, window_end):
    for existing in existing_events:
        existing_occurrences = get_event_occurrences(existing, window_start, window_end)
        for new_start, new_end in new_occurrences:
            for exist_start, exist_end in existing_occurrences:
                if new_start < exist_end and new_end > exist_start:
                    return True
    return False

@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event_in: EventCreate, db: Session = Depends(get_db), user: User = Depends(require_role(["owner", "editor"]))):
    window_start = datetime.utcnow()
    window_end = window_start + timedelta(days=90)
    # Prepare new event occurrences
    temp_event = Event(**event_in.dict(), owner_id=user.id)
    new_occurrences = get_event_occurrences(temp_event, window_start, window_end)
    # Get all existing events for user
    existing_events = db.query(Event).filter(Event.owner_id == user.id).all()
    if has_conflict(new_occurrences, existing_events, window_start, window_end):
        raise HTTPException(status_code=409, detail="Event time conflict detected with existing events.")
    event = Event(**event_in.dict(), owner_id=user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=List[EventRead])
def list_events(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Event).filter(Event.owner_id == user.id).all()

@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventRead)
def update_event(event_id: int, event_in: EventUpdate, db: Session = Depends(get_db), user: User = Depends(require_role(["owner", "editor"]))):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    # Prepare updated event for conflict check
    data = event_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(event, field, value)
    window_start = datetime.utcnow()
    window_end = window_start + timedelta(days=90)
    new_occurrences = get_event_occurrences(event, window_start, window_end)
    # Exclude self from conflict check
    existing_events = db.query(Event).filter(Event.owner_id == user.id, Event.id != event_id).all()
    if has_conflict(new_occurrences, existing_events, window_start, window_end):
        raise HTTPException(status_code=409, detail="Event time conflict detected with existing events.")
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db), user: User = Depends(require_role(["owner", "editor"]))):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return None 

@router.post("/batch", response_model=List[EventRead], status_code=status.HTTP_201_CREATED)
def batch_create_events(
    events_in: List[EventCreate],
    db: Session = Depends(get_db),
    user: User = Depends(require_role(["owner", "editor"]))
):
    created_events = []
    for event_in in events_in:
        event = Event(**event_in.dict(), owner_id=user.id)
        db.add(event)
        created_events.append(event)
    db.commit()
    for event in created_events:
        db.refresh(event)
    return created_events
