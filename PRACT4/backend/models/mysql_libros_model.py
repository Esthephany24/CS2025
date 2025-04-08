#backend/models/mysql_libros_model.py
from backend.models.mysql_connection_pool import MySQLPool

class LibroModel:
    def __init__(self):
        self.mysql_pool = MySQLPool()

    def libro_exists(self, libro_id):
        rv = self.mysql_pool.execute("SELECT COUNT(*) FROM libros WHERE id_libro = %s", (libro_id,))
        return rv[0][0] > 0

    def autor_exists(self, autor_id):
        rv = self.mysql_pool.execute("SELECT COUNT(*) FROM autores WHERE id_autor = %s AND eliminado = FALSE", (autor_id,))
        return rv[0][0] > 0

    def genero_exists(self, genero_id):
        rv = self.mysql_pool.execute("SELECT COUNT(*) FROM generos WHERE id_genero = %s", (genero_id,))
        return rv[0][0] > 0
    
    def create_genero(self, nombre, descripcion):
        query = """
            INSERT INTO Generos (nombre, descripcion)
            VALUES (%s, %s)
        """
        self.mysql_pool.execute(query, (nombre, descripcion), commit=True)
        return {'message': f"Género '{nombre}' creado correctamente."}

    def asociar_generos_a_libro(self, id_libro, generos_ids):
        for id_genero in generos_ids:
            self.mysql_pool.execute(
                "INSERT INTO Libros_Generos (id_libro, id_genero) VALUES (%s, %s)",
                (id_libro, id_genero),
                commit=True
            )
        return {'message': 'Géneros asociados correctamente'}


    def create_libro(self, titulo, fecha_publicacion, autores_ids):
        # Validar que los autores existan
        for autor_id in autores_ids:
            result = self.mysql_pool.execute("SELECT COUNT(*) FROM autores WHERE id_autor = %s", (autor_id,))
            if result[0][0] == 0:
                return {'error': f'El autor con ID {autor_id} no existe.'}

        # Insertar libro
        query = """
            INSERT INTO libros (titulo, fecha_publicacion)
            VALUES (%s, %s)
        """
        cursor = self.mysql_pool.execute(query, (titulo, fecha_publicacion), commit=True)
        libro_id = cursor.lastrowid

        # Insertar relación con autores
        for autor_id in autores_ids:
            self.mysql_pool.execute(
                "INSERT INTO Libros_Autores (id_libro, id_autor) VALUES (%s, %s)",
                (libro_id, autor_id),
                commit=True
            )

        return {'message': 'Libro creado correctamente', 'id_libro': libro_id}

    
    def get_libros_por_autor(self, id_autor):
        query = """
            SELECT L.id_libro, L.titulo, L.fecha_publicacion
            FROM Libros L
            JOIN Libros_Autores LA ON L.id_libro = LA.id_libro
            WHERE LA.id_autor = %s AND L.eliminado = 0
        """
        rv = self.mysql_pool.execute(query, (id_autor,))
        return [{'id': r[0], 'titulo': r[1], 'fecha_publicacion': r[2]} for r in rv]

    def get_autores_de_libro(self, id_libro):
        if not self.libro_exists(id_libro):
            return {'error': 'Libro no existe.'}
        query = """ 
            SELECT A.id_autor, A.nombre
            FROM autores A
            JOIN libros_autores LA ON A.id_autor = LA.id_autor
            WHERE LA.id_libro = %s AND A.eliminado = FALSE
        """ 
        result = self.mysql_pool.execute(query, (id_libro,))
        return [{'id': r[0], 'nombre': r[1]} for r in result]

    def delete_libro(self, libro_id):
        query = "UPDATE libros SET eliminado = 1 WHERE id_libro = %s"
        self.mysql_pool.execute(query, (libro_id,), commit=True)
        return {'message': 'Libro eliminado lógicamente'}   

    def get_libros(self):
        query = """
            SELECT id_libro, titulo, fecha_publicacion, descripcion
            FROM libros
            WHERE eliminado = FALSE
        """
        result = self.mysql_pool.execute(query)
        return [{'id': r[0], 'titulo': r[1], 'fecha_publicacion': r[2], 'descripcion': r[3]} for r in result]
