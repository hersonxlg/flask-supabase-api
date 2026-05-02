import os
import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos (URL de conexión de Supabase)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Crea una conexión a la base de datos de Supabase."""
    try:
        # En Psycopg 3 se usa .connect() directamente
        conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        return conn
    except Exception as e:
        print(f"Error crítico al conectar a la base de datos: {e}")
        return None

@app.route('/', methods=['GET'])
def index():
    """Ruta principal con información de la API."""
    return jsonify({
        "estado": "API Flask + Supabase funcionando 🚀",
        "rutas_disponibles": [
            "/clientes",
            "/productos",
            "/ventas"
        ]
    })

@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Obtiene todos los registros de la tabla clientes."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM clientes ORDER BY id;')
        clientes = cur.fetchall()
    
    conn.close()
    return jsonify(clientes)

@app.route('/productos', methods=['GET'])
def get_productos():
    """Obtiene todos los registros de la tabla productos."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM productos ORDER BY id;')
        productos = cur.fetchall()
    
    conn.close()
    return jsonify(productos)

@app.route('/ventas', methods=['GET'])
def get_ventas():
    """Obtiene las ventas cruzando datos con clientes y productos."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    
    with conn.cursor() as cur:
        # Consulta SQL para unir las tablas según tu esquema
        query = '''
            SELECT 
                v.id, 
                c.nombre as cliente, 
                p.nombre as producto, 
                v.cantidad, 
                v.fecha_venta, 
                v.total 
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha_venta DESC;
        '''
        cur.execute(query)
        ventas = cur.fetchall()
    
    conn.close()
    return jsonify(ventas)

if __name__ == '__main__':
    # Obtiene el puerto de Railway o usa el 5000 por defecto para local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
