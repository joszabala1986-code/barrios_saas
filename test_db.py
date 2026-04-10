import psycopg2

conn = psycopg2.connect(
    "postgresql://postgres:Paula_1986_26@db.vgmehkebzqgmyfwmbpll.supabase.co:5432/postgres",
    sslmode="require"
)

print("Conectado correctamente")
conn.close()
