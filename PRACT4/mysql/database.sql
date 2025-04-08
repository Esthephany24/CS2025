-- Crear la base de datos
CREATE DATABASE biblioteca;

-- Usar la base de datos
USE biblioteca;

-- Crear la tabla de autores
CREATE TABLE autores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50)
);

-- Crear la tabla de libros
CREATE TABLE libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    año_publicacion YEAR,
    id_autor INT,
    FOREIGN KEY (id_autor) REFERENCES autores(id) ON DELETE CASCADE ON UPDATE CASCADE
);