"""Creates the api_automation_db and user_management table."""
from __future__ import annotations

import mysql.connector

from configs import Config
from utils import get_logger

logger = get_logger("db.init")


def _connect_without_db():
    return mysql.connector.connect(
        host=Config.get("database.host", "localhost"),
        port=Config.get("database.port", 3306),
        user=Config.get("database.user", "root"),
        password=Config.get("database.password", ""),
    )


DDL_TABLE = """
CREATE TABLE IF NOT EXISTS user_management (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150) UNIQUE,
  password VARCHAR(100),
  title VARCHAR(10),
  birth_date VARCHAR(5),
  birth_month VARCHAR(15),
  birth_year VARCHAR(5),
  firstname VARCHAR(100),
  lastname VARCHAR(100),
  company VARCHAR(150),
  address1 VARCHAR(255),
  address2 VARCHAR(255),
  country VARCHAR(100),
  zipcode VARCHAR(20),
  state VARCHAR(100),
  city VARCHAR(100),
  mobile_number VARCHAR(20),
  api_response_id VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
"""


def init_database() -> None:
    db_name = Config.get("database.name", "api_automation_db")
    cnx = _connect_without_db()
    cur = cnx.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cnx.commit()
    cur.close()
    cnx.close()
    logger.info("Database ready: %s", db_name)

    cnx = mysql.connector.connect(
        host=Config.get("database.host", "localhost"),
        port=Config.get("database.port", 3306),
        user=Config.get("database.user", "root"),
        password=Config.get("database.password", ""),
        database=db_name,
    )
    cur = cnx.cursor()
    cur.execute(DDL_TABLE)
    cnx.commit()
    cur.close()
    cnx.close()
    logger.info("Table ready: user_management")


if __name__ == "__main__":
    init_database()
    print("DB initialization complete.")

