from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, Text
from datetime import datetime
from app.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class NotificationHistory(Base):
    __tablename__ = "notification_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    template_key: Mapped[str] = mapped_column(String(50), nullable=False)
    external_user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    recipient_target: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # PENDING, SENT, FAILED
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False) # NFR-R5
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class NotificationRepository:
   
    
    async def log_notification(self, notification_id: str, template_key: str, user_id: str, target: str, status: str, error: str = None, retries: int = 0):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                record = NotificationHistory(
                    id=notification_id,
                    template_key=template_key,
                    external_user_id=user_id,
                    recipient_target=target,
                    status=status,
                    error_message=error,
                    retry_count=retries
                )
                session.add(record)
                await session.commit()