from dataclasses import dataclass

from app.models import Base


@dataclass
class Post(Base):
    title: str
    body: str
    userId: int
