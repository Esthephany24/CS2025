#backend/models/mysql_autoress_model.py
from backend.models.mysql_connection_pool import MySQLPool

class AutorModel:
    def __init__(self):
        self.mysql_pool = MySQLPool()

    def get_autor(self, autor_id):
        params = {'id': autor_id}
        rv = self.mysql_pool.execute("SELECT * FROM autores WHERE id = %(id)s", params)
        data = []
        for result in rv:
            data.append({'id': result[0], 'nombre': result[1], 'nacionalidad': result[2]})
        return data

    def get_autores(self):
        rv = self.mysql_pool.execute("SELECT * FROM autores")
        data = [{'id': r[0], 'nombre': r[1], 'nacionalidad': r[3]} for r in rv]
        return data

    def create_autor(self, nombre, nacionalidad):
        data = {'nombre': nombre, 'nacionalidad': nacionalidad}
        query = "INSERT INTO autores (nombre, nacionalidad) VALUES (%(nombre)s, %(nacionalidad)s)"
        cursor = self.mysql_pool.execute(query, data, commit=True)
        data['id'] = cursor.lastrowid
        return data

    def update_autor(self, autor_id, nombre, nacionalidad):
        data = {'id': autor_id, 'nombre': nombre, 'nacionalidad': nacionalidad}
        query = "UPDATE autores SET nombre = %(nombre)s, nacionalidad = %(nacionalidad)s WHERE id_autor = %(id)s"
        self.mysql_pool.execute(query, data, commit=True)
        return {'Se actualilzo correctamente': 1}

    def delete_autor(self, autor_id):
        query = "UPDATE autores SET eliminado = 1 WHERE id_autor = %s"
        self.mysql_pool.execute(query, (autor_id,), commit=True)
        return {'message': 'Autor eliminado lógicamente'}