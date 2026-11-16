# 🎓 Prácticas y Laboratorios — Programación Orientada a Objetos

**Universidad Autónoma de Nuevo León (UANL)**  
**Facultad de Ciencias Físico Matemáticas (FCFM)**  
**Licenciatura en Ciencias Computacionales**  

- **Estudiante:** Santiago Elias Chaparro  
- **Matrícula:** 2225342  
- **Docente:** Jorge Alberto Pineda Islas  

---

## 📚 Índice de Laboratorios y Proyectos

| Directorio | Práctica / Laboratorio | Tecnologías / Temas | Entregable / Reporte |
| :--- | :--- | :--- | :--- |
| [`lab06_abstractas_interfaces/`](./lab06_abstractas_interfaces) | **Lab 06** — Clases Abstractas e Interfaces | Polimorfismo, interfaces, simulación RPG | Código fuente Java |
| [`lab07_excepciones/`](./lab07_excepciones) | **Lab 07** — Manejo de Excepciones | Excepciones personalizadas, `try-catch-finally` | [`Manual_Laboratorio_07_Santiago_Chaparro.pdf`](./Manual_Laboratorio_07_Santiago_Chaparro.pdf) |
| [`lab10_concurrencia/`](./lab10_concurrencia) | **Lab 10** — Programación Concurrente | Hilos (`Thread`, `Runnable`), `synchronized`, Race conditions | [`Manual_Laboratorio_10_LaTeX_Santiago_Chaparro.pdf`](./Manual_Laboratorio_10_LaTeX_Santiago_Chaparro.pdf) |
| [`lab11_holamundo/`](./lab11_holamundo) | **Lab 11** — Hola Mundo con Spring Boot | Spring Boot 3.3, Spring MVC, Thymeleaf, Tomcat embebido | [`Manual_Laboratorio_11_Santiago_Chaparro.pdf`](./Manual_Laboratorio_11_Santiago_Chaparro.pdf) |
| [`lab12_agenda/`](./lab12_agenda) | **Lab 12** — Agenda de Contactos con JPA y H2 | Spring Data JPA, H2 Database, CRUD completo en memoria | [`Manual_Laboratorio_12_Santiago_Chaparro.pdf`](./Manual_Laboratorio_12_Santiago_Chaparro.pdf) |
| [`lab13_crud/`](./lab13_crud) | **Lab 13** — CRUD Completo con Spring Boot y MySQL | Arquitectura en capas (`Service`), MySQL Database, vistas unificadas | [`Manual_Laboratorio_13_Santiago_Chaparro.pdf`](./Manual_Laboratorio_13_Santiago_Chaparro.pdf) |
| [`practica14_crud/`](./practica14_crud) | **Práctica 14** — CRUD Completo Integrador | Nuevo proyecto basado en las prácticas previas, Capa Service, MySQL, pruebas completas | [`Manual_Practica_14_Santiago_Chaparro.pdf`](./Manual_Practica_14_Santiago_Chaparro.pdf) |

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
- Java Development Kit (JDK) 17 o superior (`javac -version`).
- No se requiere tener Maven instalado globalmente; cada proyecto incluye **Maven Wrapper** (`mvnw` / `mvnw.cmd`).
- Para el Laboratorio 13: servicio de MySQL activo en `localhost:3306` con la base de datos `agenda` (`CREATE DATABASE agenda;`).

### Ejecutar Laboratorio 11 (Hola Mundo Spring Boot)
```bash
cd lab11_holamundo
./mvnw spring-boot:run
```
Acceder en el navegador:
- Saludo: `http://localhost:8080/saludo`
- Ficha de Aventurero: `http://localhost:8080/aventurero`

### Ejecutar Laboratorio 12 (Agenda con Base de Datos H2)
```bash
cd lab12_agenda
./mvnw spring-boot:run
```
Acceder en el navegador:
- Lista de Contactos: `http://localhost:8080/contactos`
- Consola Web H2: `http://localhost:8080/h2-console` (JDBC URL: `jdbc:h2:mem:agenda`)

### Ejecutar Laboratorio 13 (CRUD Completo con MySQL y Capa Service)
1. Iniciar MySQL y crear la base de datos:
   ```sql
   CREATE DATABASE agenda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Ejecutar la aplicación:
   ```bash
   cd lab13_crud
   ./mvnw spring-boot:run
   ```
3. Acceder en el navegador:
   - Lista de Contactos (CRUD): `http://localhost:8080/contactos`
   - Formulario de Nuevo Contacto: `http://localhost:8080/nuevo`
   - Formulario de Edición: `http://localhost:8080/editar/{id}`

---

## 📄 Archivos y Documentación
Cada laboratorio incluye:
1. Su respectivo archivo `respuestas.txt` con la fundamentación teórica y respuestas académicas a las preguntas de reflexión.
2. Archivo comprimido `.zip` listo para entrega académica.
3. Manual formal en formato PDF con portada institucional de la UANL FCFM.
