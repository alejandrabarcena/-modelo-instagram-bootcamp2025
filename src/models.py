from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime, Text, UniqueConstraint, CheckConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # relaciones
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

    # followers/following (self-referential)
    following = relationship(
        "Follower",
        foreign_keys="Follower.user_from_id",
        back_populates="user_from",
        cascade="all, delete-orphan"
    )
    followers = relationship(
        "Follower",
        foreign_keys="Follower.user_to_id",
        back_populates="user_to",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(255), nullable=True)
    caption = Column(String(2200), nullable=True)  # IG-esque
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post id={self.id} user_id={self.user_id}>"

Index("ix_post_user_created", Post.user_id, Post.created_at.desc())

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"<Comment id={self.id} post_id={self.post_id} user_id={self.user_id}>"

class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_like_user_post"),
    )

    def __repr__(self):
        return f"<Like user_id={self.user_id} post_id={self.post_id}>"

class Follower(Base):
    __tablename__ = "follower"

    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)  # quién sigue
    user_to_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)    # a quién sigue
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

    __table_args__ = (
        UniqueConstraint("user_from_id", "user_to_id", name="uq_follow_unique"),
        CheckConstraint("user_from_id <> user_to_id", name="ck_no_self_follow"),
    )

    def __repr__(self):
        return f"<Follower from={self.user_from_id} to={self.user_to_id}>"
