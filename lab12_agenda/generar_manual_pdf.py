import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ManualPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        
        # Cargar fuentes del sistema
        self.add_font("Carlito", "", "/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf")
        self.add_font("Carlito", "B", "/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf")
        self.add_font("Carlito", "I", "/usr/share/fonts/google-carlito-fonts/Carlito-Italic.ttf")
        self.add_font("Carlito", "BI", "/usr/share/fonts/google-carlito-fonts/Carlito-BoldItalic.ttf")
        self.add_font("Mono", "", "/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf")
        self.add_font("Mono", "B", "/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Bold.ttf")
        
        # Paleta de colores institucionales y de desarrollo
        self.c_primary = (26, 54, 93)      # Deep Navy #1A365D
        self.c_secondary = (43, 108, 176)  # Blue #2B6CB0
        self.c_accent = (197, 48, 48)      # Burgundy #C53030
        self.c_spring = (109, 179, 63)     # Spring Green #6DB33F
        self.c_dark = (45, 55, 72)         # Charcoal #2D3748
        self.c_muted = (113, 128, 150)     # Gray #718096
        self.c_bg_light = (247, 250, 252)  # Soft gray #F7FAFC
        self.c_border = (226, 232, 240)    # Border #E2E8F0
        self.c_terminal_bg = (26, 32, 44)  # Terminal dark #1A202C
        self.c_terminal_fg = (72, 187, 120)# Terminal green #48BB78

    def header(self):
        if self.page_no() == 1:
            return  # Sin encabezado en portada
        
        self.set_font("Carlito", "B", 8)
        self.set_text_color(*self.c_secondary)
        self.cell(100, 5, "PROGRAMACIÓN ORIENTADA A OBJETOS — LABORATORIO 12", align="L")
        self.set_font("Carlito", "I", 8)
        self.set_text_color(*self.c_muted)
        self.cell(0, 5, "Agenda de Contactos con Spring Boot, JPA y H2", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        
        self.set_draw_color(*self.c_secondary)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return  # Sin pie de página en portada
        
        self.set_y(-15)
        self.set_draw_color(*self.c_border)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        
        self.set_font("Carlito", "", 8)
        self.set_text_color(*self.c_muted)
        self.cell(120, 5, "Santiago Elias Chaparro | Matrícula: 2225342 | Noviembre 2026", align="L")
        self.set_font("Carlito", "B", 8)
        self.cell(0, 5, f"Página {self.page_no()} de {{nb}}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def print_chapter_title(self, num_str, title):
        self.ln(4)
        self.set_font("Carlito", "B", 14)
        self.set_text_color(*self.c_primary)
        
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(*self.c_secondary)
        self.rect(x, y + 0.5, 3, 7, style="F")
        self.set_x(x + 5)
        self.cell(0, 8, f"{num_str}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def print_section_title(self, num_str, title):
        self.ln(2)
        self.set_font("Carlito", "B", 11)
        self.set_text_color(*self.c_secondary)
        self.cell(0, 6, f"{num_str} {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def print_paragraph(self, text, space_after=3):
        self.set_font("Carlito", "", 10)
        self.set_text_color(*self.c_dark)
        self.multi_cell(0, 5.2, text)
        if space_after > 0:
            self.ln(space_after)

    def print_bullet(self, title, desc):
        self.set_font("Carlito", "B", 10)
        self.set_text_color(*self.c_primary)
        self.write(5.2, f"  • {title}: ")
        self.set_font("Carlito", "", 10)
        self.set_text_color(*self.c_dark)
        self.write(5.2, f"{desc}\n")
        self.ln(1.5)

    def print_code_box(self, filename, code_text):
        line_count = len(code_text.strip().split("\n"))
        needed_height = 8 + (line_count * 3.8)
        
        if self.get_y() + needed_height > (self.h - self.b_margin) and needed_height < (self.h - 50):
            self.add_page()
            
        self.set_fill_color(*self.c_secondary)
        self.set_text_color(255, 255, 255)
        self.set_font("Carlito", "B", 9)
        self.cell(0, 6, f"  Archivo: {filename}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_fill_color(*self.c_bg_light)
        self.set_draw_color(*self.c_border)
        self.set_line_width(0.2)
        self.set_font("Mono", "", 7.4)
        self.set_text_color(26, 32, 44)
        
        formatted_code = code_text.strip()
        self.multi_cell(0, 3.8, formatted_code, border=1, fill=True)
        self.ln(4)

    def print_terminal_box(self, output_text):
        self.set_fill_color(45, 55, 72)
        self.set_text_color(240, 240, 240)
        self.set_font("Carlito", "B", 8.5)
        self.cell(0, 5.5, "  Consola de Ejecución: ./mvnw spring-boot:run", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_fill_color(*self.c_terminal_bg)
        self.set_text_color(*self.c_terminal_fg)
        self.set_font("Mono", "", 7.4)
        self.multi_cell(0, 3.8, output_text.strip(), fill=True, border=1)
        self.ln(4)

    def print_callout(self, text, is_warning=False):
        fill_col = (254, 235, 235) if is_warning else (235, 248, 255)
        border_col = (229, 62, 62) if is_warning else (49, 130, 206)
        text_col = (155, 44, 44) if is_warning else (43, 108, 176)
        
        self.set_fill_color(*fill_col)
        self.set_draw_color(*border_col)
        self.set_line_width(0.6)
        
        self.set_text_color(*text_col)
        self.set_font("Carlito", "I", 9.5)
        self.multi_cell(0, 4.8, f"Nota importante: {text}", border=1, fill=True)
        self.ln(3)


def generate_manual():
    pdf = ManualPDF()
    pdf.alias_nb_pages()
    pdf.set_margins(18, 18, 18)
    
    # =========================================================================
    # PORTADA
    # =========================================================================
    pdf.add_page()
    
    pdf.set_draw_color(26, 54, 93)
    pdf.set_line_width(1.2)
    pdf.rect(10, 10, pdf.w - 20, pdf.h - 20)
    
    pdf.set_draw_color(43, 108, 176)
    pdf.set_line_width(0.4)
    pdf.rect(12, 12, pdf.w - 24, pdf.h - 24)
    
    pdf.set_y(26)
    
    pdf.set_font("Carlito", "B", 18)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "B", 13)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(0, 6, "FACULTAD DE CIENCIAS FÍSICO MATEMÁTICAS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "I", 10)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(0, 5, "Licenciatura en Ciencias Computacionales", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(12)
    
    pdf.set_draw_color(26, 54, 93)
    pdf.set_line_width(0.8)
    pdf.line(40, pdf.get_y(), pdf.w - 40, pdf.get_y())
    pdf.ln(14)
    
    pdf.set_font("Carlito", "B", 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 6, "PROGRAMACIÓN ORIENTADA A OBJETOS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(16)
    
    pdf.set_font("Carlito", "B", 20)
    pdf.set_text_color(197, 48, 48)
    pdf.cell(0, 9, "MANUAL DE PRÁCTICA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "B", 15)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "Laboratorio 12: Agenda de Contactos con Spring Boot y BD", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "I", 11)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(0, 6, "Persistencia con Spring Data JPA, H2 Database y Ciclo CRUD Completo (Create, Read, Update, Delete)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(28)
    
    # Recuadro de datos del estudiante
    pdf.set_fill_color(247, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.set_line_width(0.5)
    box_w = 140
    box_x = (pdf.w - box_w) / 2
    pdf.rect(box_x, pdf.get_y(), box_w, 48, style="FD")
    
    pdf.set_xy(box_x + 10, pdf.get_y() + 6)
    pdf.set_font("Carlito", "B", 10.5)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(40, 6, "Estudiante:", align="L")
    pdf.set_font("Carlito", "", 10.5)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 6, "Santiago Elias Chaparro", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 10)
    pdf.set_font("Carlito", "B", 10.5)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(40, 6, "Matrícula:", align="L")
    pdf.set_font("Carlito", "", 10.5)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 6, "2225342", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 10)
    pdf.set_font("Carlito", "B", 10.5)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(40, 6, "Semestre / Unidad:", align="L")
    pdf.set_font("Carlito", "", 10.5)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 6, "Unidad 12 — Persistencia de Datos con Spring Boot", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 10)
    pdf.set_font("Carlito", "B", 10.5)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(40, 6, "Docente:", align="L")
    pdf.set_font("Carlito", "", 10.5)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 6, "Jorge Alberto Pineda Islas", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 10)
    pdf.set_font("Carlito", "B", 10.5)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(40, 6, "Fecha:", align="L")
    pdf.set_font("Carlito", "", 10.5)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 6, "Noviembre 15 del 2026", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(260)
    pdf.set_font("Carlito", "I", 9)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(0, 5, "San Nicolás de los Garza, Nuevo León, México", align="C")

    # =========================================================================
    # CAPÍTULO 1: INTRODUCCIÓN Y OBJETIVOS
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("1", "INTRODUCCIÓN Y OBJETIVOS DE LA PRÁCTICA")
    pdf.print_paragraph(
        "En el Laboratorio 11 se introdujo el desarrollo web con Spring Boot y Thymeleaf; no obstante, los datos residían "
        "únicamente en memoria como variables locales dentro del controlador, perdiéndose de forma instantánea al recargar "
        "o reiniciar el servidor. En cualquier aplicación informática real, la persistencia de datos es un pilar indispensable: "
        "la información debe ser almacenada, recuperada, modificada y eliminada de un soporte transaccional permanente."
    )
    pdf.print_paragraph(
        "En este laboratorio se implementa una arquitectura empresarial conectando Spring Boot con una base de datos relacional "
        "utilizando el estándar Java Persistence API (JPA) mediante Hibernate como motor ORM y Spring Data JPA para la generación "
        "automática de repositorios. Para enriquecer la práctica, se implementa el ciclo CRUD completo, incorporando los módulos "
        "requeridos de actualización (Update) y eliminación (Delete) de contactos."
    )
    
    pdf.print_section_title("1.1", "Objetivos Específicos")
    pdf.print_bullet("Persistencia Relacional", "Configurar una base de datos relacional embebida H2 y habilitar su consola de monitoreo web.")
    pdf.print_bullet("Mapeo Objeto-Relacional (ORM)", "Diseñar la entidad Contacto con anotaciones JPA (@Entity, @Table, @Id, @GeneratedValue).")
    pdf.print_bullet("Spring Data Repositories", "Implementar ContactoRepository heredando de JpaRepository para delegar las operaciones SQL a Spring.")
    pdf.print_bullet("Formularios Dinámicos", "Capturar y validar datos web mediante Thymeleaf (th:object, th:field, th:action) con vinculación bidireccional.")
    pdf.print_bullet("CRUD Completo", "Implementar la creación (/nuevo), lectura (/contactos), edición (/editar/{id}) y borrado seguro (/eliminar/{id}).")

    pdf.print_chapter_title("2", "ARQUITECTURA DE PERSISTENCIA Y PATRÓN REPOSITORY")
    pdf.print_paragraph(
        "La interacción entre la capa web y la base de datos se desacopla mediante capas bien diferenciadas:"
    )
    pdf.print_bullet("Vista (Thymeleaf)", "Formularios HTML (nuevo.html, editar.html) y tabla de visualización (contactos.html).")
    pdf.print_bullet("Controlador (ContactoController)", "Gestiona rutas HTTP GET y POST, validando y transfiriendo entidades al repositorio.")
    pdf.print_bullet("Capa de Acceso a Datos (ContactoRepository)", "Interfaz que extiende JpaRepository<Contacto, Long>; Spring Data genera su implementación en runtime.")
    pdf.print_bullet("Motor ORM (Hibernate / JPA)", "Mapea objetos Contacto a filas de la tabla CONTACTO, administrando el ciclo de vida y generando SQL nativo.")
    pdf.print_bullet("Base de Datos (H2 Database)", "Motor SQL embebido en memoria (jdbc:h2:mem:agenda) que no requiere servidores externos.")

    pdf.print_callout(
        "Spring Data JPA elimina la necesidad de escribir sentencias SQL (INSERT, SELECT, UPDATE, DELETE). A través de la interfaz JpaRepository, Spring genera dinámicamente un Proxy en tiempo de ejecución que ejecuta las operaciones de persistencia en milisegundos.",
        is_warning=False
    )

    pdf.print_chapter_title("3", "ESTRUCTURA DEL PROYECTO ENTREGABLE")
    tree_text = (
        "lab12_agenda/\n"
        "├── pom.xml                                   # Dependencias: Web, Thymeleaf, Data JPA, H2\n"
        "├── mvnw & mvnw.cmd                           # Scripts multiplataforma con auto-detección JDK\n"
        "├── .mvn/wrapper/maven-wrapper.properties     # Configuración oficial de Maven 3.9.9\n"
        "├── .gitignore                                # Exclusión de temporales y target/\n"
        "├── respuestas.txt                            # Respuestas teóricas y análisis técnico\n"
        "├── Manual_Laboratorio_12_Santiago_Chaparro.pdf # Documento PDF institucional\n"
        "└── src/\n"
        "    ├── main/\n"
        "    │   ├── java/com/gremio/\n"
        "    │   │   ├── AgendaWebApplication.java     # Punto de entrada @SpringBootApplication\n"
        "    │   │   ├── model/\n"
        "    │   │   │   └── Contacto.java             # Entidad JPA (@Entity, @Id, @GeneratedValue)\n"
        "    │   │   ├── repository/\n"
        "    │   │   │   └── ContactoRepository.java   # Interfaz JpaRepository<Contacto, Long>\n"
        "    │   │   └── controller/\n"
        "    │   │       └── ContactoController.java   # Controlador CRUD (listar, nuevo, guardar, editar, eliminar)\n"
        "    │   └── resources/\n"
        "    │       ├── templates/\n"
        "    │       │   ├── contactos.html            # Lista con tabla, contador, th:each, Editar/Eliminar\n"
        "    │       │   ├── nuevo.html                # Formulario de alta de contacto\n"
        "    │       │   └── editar.html               # Formulario de edición con ID oculto\n"
        "    │       └── application.properties        # Configuración H2, dialecto, consola web y caché\n"
        "    └── test/java/com/gremio/\n"
        "        └── AgendaWebApplicationTests.java    # Prueba unitaria de contexto JPA y Spring"
    )
    pdf.print_code_box("Árbol de Directorios (lab12_agenda)", tree_text)

    # =========================================================================
    # IMPLEMENTACIÓN DE CÓDIGO FUENTE
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("4", "CÓDIGO FUENTE DETALLADO")
    
    with open("lab12_agenda/pom.xml", "r") as f:
        pom_code = f.read()
    pdf.print_code_box("pom.xml", pom_code)
    
    with open("lab12_agenda/src/main/resources/application.properties", "r") as f:
        props_code = f.read()
    pdf.print_code_box("src/main/resources/application.properties", props_code)

    pdf.add_page()
    with open("lab12_agenda/src/main/java/com/gremio/AgendaWebApplication.java", "r") as f:
        app_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/AgendaWebApplication.java", app_code)

    with open("lab12_agenda/src/main/java/com/gremio/model/Contacto.java", "r") as f:
        model_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/model/Contacto.java", model_code)

    pdf.add_page()
    with open("lab12_agenda/src/main/java/com/gremio/repository/ContactoRepository.java", "r") as f:
        repo_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/repository/ContactoRepository.java", repo_code)

    with open("lab12_agenda/src/main/java/com/gremio/controller/ContactoController.java", "r") as f:
        ctrl_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/controller/ContactoController.java", ctrl_code)

    pdf.add_page()
    with open("lab12_agenda/src/main/resources/templates/contactos.html", "r") as f:
        contactos_html = f.read()
    pdf.print_code_box("src/main/resources/templates/contactos.html", contactos_html)

    pdf.add_page()
    with open("lab12_agenda/src/main/resources/templates/nuevo.html", "r") as f:
        nuevo_html = f.read()
    pdf.print_code_box("src/main/resources/templates/nuevo.html", nuevo_html)

    with open("lab12_agenda/src/main/resources/templates/editar.html", "r") as f:
        editar_html = f.read()
    pdf.print_code_box("src/main/resources/templates/editar.html", editar_html)

    # =========================================================================
    # PREGUNTAS DE REFLEXIÓN
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("5", "PREGUNTAS DE REFLEXIÓN Y FUNDAMENTACIÓN TEÓRICA")
    
    pdf.print_section_title("5.1", "¿Qué hace @Entity? ¿Por qué se requiere el constructor vacío?")
    pdf.print_paragraph(
        "• Rol de @Entity: Marca la clase Java como una Entidad JPA administrada por el EntityManager de Hibernate, mapeando sus "
        "campos con las columnas de una tabla relacional ('contacto') y permitiendo la generación automática de sentencias DDL (CREATE TABLE) "
        "y el seguimiento de cambios (dirty checking) de objetos.",
        space_after=2
    )
    pdf.print_paragraph(
        "• Importancia del constructor vacío: Hibernate utiliza la Java Reflection API para reconstruir las entidades en memoria a partir "
        "de las filas obtenidas en una consulta SQL. Hibernate ejecuta 'Contacto.class.getDeclaredConstructor().newInstance()', que requiere "
        "estrictamente el constructor sin argumentos. Posteriormente, inyecta los valores en las propiedades mediante setters o acceso a campos. "
        "Sin este constructor, se produce una excepción fatal 'InstantiationException'."
    )

    pdf.print_section_title("5.2", "¿Por qué ContactoRepository no tiene métodos escritos y aun así funciona?")
    pdf.print_paragraph(
        "Al extender 'JpaRepository<Contacto, Long>', la interfaz hereda los contratos de CrudRepository y PagingAndSortingRepository. "
        "Durante el arranque de Spring Boot, el motor de Spring Data detecta la interfaz y crea un objeto Proxy dinámico en tiempo de ejecución, "
        "delegando las llamadas a una clase genérica de implementación interna: 'SimpleJpaRepository'. "
        "Dicha clase interactúa con el EntityManager para generar las consultas SQL (SELECT, INSERT, UPDATE, DELETE) en la base de datos H2.",
        space_after=2
    )

    pdf.print_section_title("5.3", "¿Qué diferencia hay entre @GetMapping y @PostMapping? ¿Cuándo usar cada uno?")
    pdf.print_paragraph(
        "• @GetMapping (HTTP GET): Operación segura e idempotente utilizada para SOLICITAR y LEER información sin provocar efectos "
        "secundarios en el servidor. Los parámetros viajan en la URL y es cacheable. Ejemplos: consultar la lista (/contactos) o mostrar un formulario (/nuevo, /editar/1).",
        space_after=2
    )
    pdf.print_paragraph(
        "• @PostMapping (HTTP POST): Operación no segura y no idempotente utilizada para ENVIAR datos en el cuerpo de la petición (payload) "
        "con el propósito de crear o modificar registros en el servidor. Oculta la información de la URL y soporta grandes volúmenes. "
        "Ejemplo: procesar el formulario de contacto y guardarlo en la base de datos (/guardar)."
    )

    pdf.print_section_title("5.4", "Implementación de los Módulos de Update y Delete")
    pdf.print_paragraph(
        "• Update: Spring Data JPA utiliza un método inteligente 'save(entity)'. Si 'entity.getId() == null', Hibernate genera un INSERT; "
        "si 'entity.getId() != null', Hibernate genera un UPDATE. En 'editar.html' se incluye un campo oculto '<input type=\"hidden\" th:field=\"*{id}\" />' "
        "para que al enviar el formulario a '/guardar', Spring preserve la clave primaria y actualice el registro existente.",
        space_after=2
    )
    pdf.print_paragraph(
        "• Delete: Implementado en el endpoint '@GetMapping(\"/eliminar/{id}\")', que recibe el ID como variable de ruta, ejecuta 'repo.deleteById(id)' "
        "y redirige inmediatamente al usuario a la lista actualizada mediante 'redirect:/contactos'."
    )

    # =========================================================================
    # GUÍA DE EJECUCIÓN Y VALIDACIÓN
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("6", "GUÍA DE EJECUCIÓN Y PRUEBAS DEL SISTEMA")
    
    terminal_run_sample = (
        "$ cd lab12_agenda && ./mvnw spring-boot:run\n"
        "[INFO] Scanning for projects...\n"
        "[INFO] Building agenda-web 0.0.1-SNAPSHOT\n"
        "[INFO] --- spring-boot:run (default-cli) @ agenda-web ---\n"
        "  .   ____          _            __ _ _\n"
        " /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\\n"
        "( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\\n"
        " \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )\n"
        "  '  |____| .__|_| |_|_| |_\\__, | / / / /\n"
        " =========|_|==============|___/=/_/_/_/\n"
        " :: Spring Boot ::                (v3.3.5)\n\n"
        "2026-11-15T18:00:00.120-06:00  INFO --- [agenda-web] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 8080 (http)\n"
        "2026-11-15T18:00:01.350-06:00  INFO --- [agenda-web] o.h.e.t.j.p.i.JpaMySQLDialect            : HSQL default schema is [PUBLIC]\n"
        "2026-11-15T18:00:01.400-06:00  INFO --- [agenda-web] o.s.b.a.h2.H2ConsoleAutoConfiguration     : H2 console available at '/h2-console'. Database available at 'jdbc:h2:mem:agenda'\n"
        "2026-11-15T18:00:01.890-06:00  INFO --- [agenda-web] com.gremio.AgendaWebApplication          : Started AgendaWebApplication in 1.82 seconds"
    )
    pdf.print_terminal_box(terminal_run_sample)
    
    pdf.print_section_title("6.1", "Mapa de Endpoints y Vistas Web")
    
    ascii_table = (
        "GET http://localhost:8080/contactos\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "|  Agenda de Contactos                                               [+ Nuevo Contacto]   |\n"
        "|  Total de registros: 2 contactos en base de datos H2                                    |\n"
        "+----+----------+----------+-----------------------+--------------+-----------------------+\n"
        "| ID | Nombre   | Apellido | Email                 | Telefono     | Acciones              |\n"
        "+----+----------+----------+-----------------------+--------------+-----------------------+\n"
        "| 1  | Sylva    | Bosque   | sylva@gremio.com      | 81 1111 2222 | [Editar]   [Eliminar] |\n"
        "| 2  | Thorin   | Escudo   | thorin@gremio.com     | 81 3333 4444 | [Editar]   [Eliminar] |\n"
        "+----+----------+----------+-----------------------+--------------+-----------------------+"
    )
    pdf.print_code_box("Listado de Contactos (/contactos)", ascii_table)

    ascii_form = (
        "GET http://localhost:8080/nuevo  o  GET /editar/1\n"
        "+---------------------------------------------------------+\n"
        "|                 Editar Contacto                         |\n"
        "|              [ ID de Registro: 1 ]                      |\n"
        "|                                                         |\n"
        "|   Nombre:    [ Sylva                             ]      |\n"
        "|   Apellido:  [ Bosque                            ]      |\n"
        "|   Email:     [ sylva@gremio.com                  ]      |\n"
        "|   Telefono:  [ 81 1111 2222                      ]      |\n"
        "|                                                         |\n"
        "|   [           Actualizar contacto            ]          |\n"
        "|              <- Cancelar y volver a la agenda           |\n"
        "+---------------------------------------------------------+"
    )
    pdf.print_code_box("Formulario de Captura y Edición (/nuevo /editar)", ascii_form)

    pdf.print_chapter_title("7", "CONCLUSIONES DE LA PRÁCTICA")
    pdf.print_paragraph(
        "El Laboratorio 12 consolida los conocimientos de desarrollo web en Java al incorporar persistencia relacional con Spring Data JPA. "
        "La integración con una base de datos embebida como H2 permite simular con total fidelidad el comportamiento de sistemas "
        "de producción (como PostgreSQL o MySQL) sin fricción de configuración. La implementación del ciclo CRUD completo (Create, Read, "
        "Update, Delete) demuestra la versatilidad de Spring MVC y Thymeleaf para crear interfaces interactivas, seguras y modulares.",
        space_after=4
    )
    pdf.print_paragraph(
        "Con este laboratorio, se culmina la transición desde programas secuenciales de consola hasta aplicaciones web empresariales completas, "
        "estableciendo las bases para arquitecturas con servicios REST, seguridad y microservicios."
    )

    output_pdf = "Manual_Laboratorio_12_Santiago_Chaparro.pdf"
    pdf.output(output_pdf)
    print(f"Manual generado con éxito: {output_pdf}")
    
    pdf.output("lab12_agenda/Manual_Laboratorio_12_Santiago_Chaparro.pdf")
    print("Copia generada en lab12_agenda/Manual_Laboratorio_12_Santiago_Chaparro.pdf")

if __name__ == "__main__":
    generate_manual()
