import psycopg2

try:
    conn = psycopg2.connect(
        dbname="shaosheng",
        user="fabio",
        password="1234",
        host="localhost",
        port="5432"
    )
    print("Conexão bem-sucedida!")
except Exception as e:
    print("Erro:", e)
