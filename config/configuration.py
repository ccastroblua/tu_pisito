import os
import dotenv
import sqlalchemy as alch

dotenv.load_dotenv()

password = os.getenv("sql_pass")
db_name = "tu_pisito"

connection = f"mysql+pymysql://root:{password}@localhost/{db_name}"
engine = alch.create_engine(connection)
print(f"Conectado a mysql / base de datos: {db_name}")