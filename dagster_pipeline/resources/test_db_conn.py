#  ce ficheir c'est pour teste rla connexion avec la BDD duck db 
import duckdb

conn = duckdb.connect("../../data/crypto.duckdb")
print(conn.execute("SHOW TABLES").fetchdf())