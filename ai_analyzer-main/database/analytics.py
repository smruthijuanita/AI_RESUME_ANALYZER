import sqlite3
import pandas as pd
from config.config import DB_PATH


def load_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql("SELECT * FROM analyses", conn)

    return df