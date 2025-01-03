# app/repositories/post_repository.py

from app import db
from app.models.posts import Post
from sqlalchemy.orm import Session

class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_posts(self):
        return self.session.query(Post).all()

    def get_post_by_id(self, post_id: int):
        return self.session.query(Post).filter(Post.id == post_id).first()

    def create_post(self, title: str, content: str, image_url: str, user_name: str):
        new_post = Post(title=title, content=content, image_url=image_url, user_name=user_name)
        self.session.add(new_post)
        self.session.commit()

    def delete_post(self, post: Post):
        self.session.delete(post)
        self.session.commit()
