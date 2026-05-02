import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración del cliente de Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/', methods=['GET'])
def index():
    """Ruta principal con información de la API."""
    return jsonify({
        "estado": "API Flask + Supabase (Librería Oficial) funcionando 🚀",
        "rutas_disponibles": [
            "/clientes",
            "/productos",
            "/ventas"
        ]
    })

@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Obtiene todos los registros de la tabla clientes."""
    try:
        respuesta = supabase.table('clientes').select('*').order('id').execute()
        return jsonify(respuesta.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/productos', methods=['GET'])
def get_productos():
    """Obtiene todos los registros de la tabla productos."""
    try:
        respuesta = supabase.table('productos').select('*').order('id').execute()
        return jsonify(respuesta.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ventas', methods=['GET'])
def get_ventas():
    """Obtiene las ventas cruzando datos con clientes y productos."""
    try:
        # Supabase detecta las llaves foráneas y hace el JOIN automáticamente
        # al incluir clientes(nombre) y productos(nombre) en el select
        respuesta = supabase.table('ventas') \
            .select('id, cantidad, fecha_venta, total, clientes(nombre), productos(nombre)') \
            .order('fecha_venta', desc=True) \
            .execute()
            
        return jsonify(respuesta.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Obtiene el puerto de Railway o usa el 5000 por defecto para local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
