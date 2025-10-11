from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import Base, engine
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
from sqlalchemy import (
    create_engine, ForeignKey, String, Integer, Boolean, Date, Text
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Войти', render_kw={"class": "w-100 btn btn-lg btn-primary"})

class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    projects: Mapped[List["Project"]] = relationship(back_populates="user")
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")
    habits: Mapped[List["Habit"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username!r})>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped["User"] = relationship(back_populates="projects")
    tasks: Mapped[List["Task"]] = relationship(back_populates="project")

    def __repr__(self):
        return f"<Project(title={self.title!r})>"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[Optional[str]] = mapped_column(String(20))
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped["User"] = relationship(back_populates="tasks")
    project: Mapped["Project"] = relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task(title={self.title!r})>"


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    frequency: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped["User"] = relationship(back_populates="habits")
    logs: Mapped[List["HabitLog"]] = relationship(back_populates="habit")

    def __repr__(self):
        return f"<Habit(name={self.name!r})>"


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))
    log_date: Mapped[date] = mapped_column(Date, default=date.today)
    is_done: Mapped[bool] = mapped_column(Boolean, default=True)

    habit: Mapped["Habit"] = relationship(back_populates="logs")

    def __repr__(self):
        return f"<HabitLog(habit_id={self.habit_id}, date={self.log_date})>"

if __name__ == "__main__":
    Base.metadata.create_all(engine)