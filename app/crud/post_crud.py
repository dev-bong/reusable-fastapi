from sqlalchemy.orm import Session

from app.models import Post
from app.schemas.post_schema import PostCreate


def create_post(session: Session, post_create: PostCreate, user_id: int) -> Post:
    post = Post(
        subject=post_create.subject,
        content=post_create.content,
        user_id=user_id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    return post


def update_post(session: Session, post: Post, post_update: PostCreate):
    if post_update.subject:
        post.subject = post_update.subject
    if post_update.content:
        post.content = post_update.content

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


def get_posts(session: Session, page: int, size: int) -> list[Post]:
    return (
        session.query(Post)
        .order_by(Post.create_date)
        .offset(size * (page - 1))
        .limit(size)
        .all()
    )


def get_post(session: Session, id: int) -> Post | None:
    return session.get(Post, id)
