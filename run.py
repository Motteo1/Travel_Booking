#!/usr/bin/python3
"""RUN APP"""
import sys
sys.path.append("C:/Users/TIM/Desktop/Code/Travel_Booking/")
from src import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)