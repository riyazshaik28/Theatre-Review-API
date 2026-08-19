from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_
from sqlmodel import Session, select

from database import get_session
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/review", tags=["reviews"])


@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, db: Session = Depends(get_session)):
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/get", response_model=List[ReviewRead])
def listreviews(
    play_name: Optional[str] = Query(default=None, description="Filter by play name"),
    reviewer_name: Optional[str] = Query(default=None, description="Filter by reviewer name"),
    search: Optional[str] = Query(default=None, description="Search in play name or comment"),
    min_rating: Optional[int] = Query(default=None, ge=1, le=5),
    max_rating: Optional[int] = Query(default=None, ge=1, le=5),
    sort_by: str = Query(default="newest", description="newest, oldest, highest, lowest"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_session),
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name.ilike(f"%{play_name}%"))

    if reviewer_name:
        query = query.where(Review.reviewer_name.ilike(f"%{reviewer_name}%"))

    if min_rating is not None:
        query = query.where(Review.rating >= min_rating)

    if max_rating is not None:
        query = query.where(Review.rating <= max_rating)

    if search:
        term = f"%{search}%"
        query = query.where(or_(Review.play_name.ilike(term), Review.comment.ilike(term)))

    if sort_by == "newest":
        query = query.order_by(Review.created_at.desc())
    elif sort_by == "oldest":
        query = query.order_by(Review.created_at.asc())
    elif sort_by == "highest":
        query = query.order_by(Review.rating.desc(), Review.created_at.desc())
    elif sort_by == "lowest":
        query = query.order_by(Review.rating.asc(), Review.created_at.desc())
    else:
        query = query.order_by(Review.created_at.desc())

    query = query.offset(offset).limit(limit)
    reviews = db.exec(query).all()
    return reviews


@router.get("/plays")
def get_play_names(db: Session = Depends(get_session)):
    play_names = db.exec(select(Review.play_name).distinct().order_by(Review.play_name.asc())).all()
    return {"play_names": play_names}


@router.get("/summary")
def get_summary(db: Session = Depends(get_session)):
    results = db.exec(
        select(
            Review.play_name,
            func.avg(Review.rating).label("average_rating"),
            func.count(Review.id).label("total_reviews"),
            func.max(Review.created_at).label("latest_review"),
        )
        .group_by(Review.play_name)
        .order_by(func.avg(Review.rating).desc())
    ).all()

    summary = []
    for play_name, average_rating, total_reviews, latest_review in results:
        summary.append(
            {
                "play_name": play_name,
                "average_rating": round(float(average_rating), 2),
                "total_reviews": total_reviews,
                "latest_review": latest_review,
            }
        )

    return summary


@router.get("/{id}", response_model=ReviewRead)
def readall(id: int, db: Session = Depends(get_session)):
    review = db.exec(select(Review).where(Review.id == id)).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


@router.get("/avg/{play_name}")
def avg_calculation(play_name: str, db: Session = Depends(get_session)):
    result = db.exec(
        select(
            func.avg(Review.rating),
            func.count(Review.id),
            func.max(Review.created_at),
        ).where(Review.play_name.ilike(f"%{play_name}%"))
    ).first()

    avg_rating, total_reviews, latest_review = result

    if total_reviews == 0:
        raise HTTPException(status_code=404, detail=f"No reviews found for {play_name}")

    return {
        "play_name": play_name,
        "average_rating": round(float(avg_rating), 2),
        "total_reviews": total_reviews,
        "latest_review": latest_review,
    }


@router.get("/getbyid/{id}", response_model=ReviewRead)
def getbyid(id: int, db: Session = Depends(get_session)):
    review = db.get(Review, id)
    if not review:
        raise HTTPException(status_code=404, detail=f"no review found {id}")
    return review


@router.patch("/getbyid/{id}", response_model=ReviewRead)
def updatebyid(id: int, update: ReviewUpdate, db: Session = Depends(get_session)):
    review = db.get(Review, id)
    if not review:
        raise HTTPException(status_code=404, detail=f"no review found {id}")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/deletebyid/{id}")
def deletebyid(id: int, db: Session = Depends(get_session)):
    review = db.get(Review, id)

    if not review:
        raise HTTPException(status_code=404, detail=f"Review with id {id} not found")

    db.delete(review)
    db.commit()

    return {"message": f"The review with id {id} was deleted successfully"}
