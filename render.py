import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models import Base
from eralchemy import render_er
from sqlalchemy import create_engine

engine = create_engine('sqlite:///instagram.db')
render_er(Base, 'diagram.png')
