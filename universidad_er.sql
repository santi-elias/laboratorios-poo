-- =============================================
-- SISTEMA DE GESTIÓN UNIVERSITARIA
-- Diagrama Entidad-Relación - 5 Tablas
-- Para ejecutar en DBeaver CE con SQLite
-- =============================================

-- 1. Tabla Departamentos
CREATE TABLE Departamentos (
    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          VARCHAR(100) NOT NULL UNIQUE,
    edificio        VARCHAR(50)  NOT NULL
);

-- 2. Tabla Profesores
CREATE TABLE Profesores (
    id_profesor      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           VARCHAR(50)  NOT NULL,
    apellido         VARCHAR(50)  NOT NULL,
    especialidad     VARCHAR(100),
    id_departamento  INTEGER,
    FOREIGN KEY (id_departamento)
        REFERENCES Departamentos(id_departamento)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 3. Tabla Materias
CREATE TABLE Materias (
    id_materia   INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       VARCHAR(100) NOT NULL,
    creditos     INTEGER      NOT NULL,
    id_profesor  INTEGER,
    FOREIGN KEY (id_profesor)
        REFERENCES Profesores(id_profesor)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 4. Tabla Estudiantes
CREATE TABLE Estudiantes (
    id_estudiante    INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           VARCHAR(50)  NOT NULL,
    apellido         VARCHAR(50)  NOT NULL,
    email            VARCHAR(100) UNIQUE,
    fecha_nacimiento DATE
);

-- 5. Tabla Inscripciones (tabla intermedia N:M)
CREATE TABLE Inscripciones (
    id_inscripcion    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante     INTEGER NOT NULL,
    id_materia        INTEGER NOT NULL,
    fecha_inscripcion DATE    NOT NULL,
    calificacion      DECIMAL(4,1),
    FOREIGN KEY (id_estudiante)
        REFERENCES Estudiantes(id_estudiante)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_materia)
        REFERENCES Materias(id_materia)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =============================================
-- DATOS DE EJEMPLO
-- =============================================

INSERT INTO Departamentos (nombre, edificio) VALUES
('Ingeniería en Software', 'Edificio A'),
('Ciencias Básicas', 'Edificio B'),
('Administración', 'Edificio C');

INSERT INTO Profesores (nombre, apellido, especialidad, id_departamento) VALUES
('Carlos', 'García', 'Bases de Datos', 1),
('María', 'López', 'Matemáticas', 2),
('Roberto', 'Hernández', 'Finanzas', 3);

INSERT INTO Materias (nombre, creditos, id_profesor) VALUES
('Bases de Datos', 6, 1),
('Cálculo Diferencial', 5, 2),
('Contabilidad', 4, 3);

INSERT INTO Estudiantes (nombre, apellido, email, fecha_nacimiento) VALUES
('Santi', 'Martínez', 'santi@universidad.edu', '2004-03-15'),
('Ana', 'Torres', 'ana@universidad.edu', '2003-11-22'),
('Luis', 'Ramírez', 'luis@universidad.edu', '2004-07-08');

INSERT INTO Inscripciones (id_estudiante, id_materia, fecha_inscripcion, calificacion) VALUES
(1, 1, '2026-08-15', 95.0),
(1, 2, '2026-08-15', 88.5),
(2, 1, '2026-08-15', 92.0),
(3, 3, '2026-08-15', NULL);
