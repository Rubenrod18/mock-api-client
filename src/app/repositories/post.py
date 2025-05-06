from app.models import Post
from app.repositories.base import SessionRepository


class PostRepository(SessionRepository):
    def __init__(self):
        super().__init__(model=Post, session_key='posts')
