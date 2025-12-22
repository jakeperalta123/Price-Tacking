from sqlalchemy.orm import Session

def safe_commit(session: Session, obj = None):
    try:
        session.commit()
        if obj:
            session.refresh(obj)
        return obj
    except Exception as e:
        session.rollback()
        raise e