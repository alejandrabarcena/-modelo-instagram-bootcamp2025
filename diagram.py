from eralchemy import render_er
from src.models import Base
from sqlalchemy import create_engine

# Usa la misma base de datos que configuraste en models.py
engine = create_engine('sqlite:///instagram.db')

# Genera el archivo 'diagram.png'
render_er(Base, 'diagram.png')
