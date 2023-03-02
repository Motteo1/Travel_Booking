#!/usr/bin/python3
import sys
sys.path.append("C:/Users/TIM/Desktop/Code/Travel_Booking/")
from src.database.engine import DBStorage

storage = DBStorage()
storage.reload()