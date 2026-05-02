import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "estado": "API funcionando \u2705",
        "rutas_disponibles": [
            "/clientes",
            "/productos",
            "/ventas"
        ]
    })

@app.route('/clientes', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No hay conexión a la base de datos"}), 500
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM clientes ORDER BY id;')
    clientes = cur.fetchall()
    
    cur.close()
    conn.close()
    return jsonify(clientes)

@app.route('/productos', methods=['GET'])
def get_productos():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No hay conexión a la base de datos"}), 500
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM productos ORDER BY id;')
    productos = cur.fetchall()
    
    cur.close()
    conn.close()
    return jsonify(productos)

@app.route('/ventas', methods=['GET'])
def get_ventas():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No hay conexión a la base de datos"}), 500
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT v.id, c.nombre as cliente, p.nombre as producto, 
               v.cantidad, v.fecha_venta, v.total 
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha_venta DESC;
    ''')
    ventas = cur.fetchall()
    
    cur.close()
    conn.close()
    return jsonify(ventas)

if __name__ == '__main__':
    # Para desarrollo local
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
