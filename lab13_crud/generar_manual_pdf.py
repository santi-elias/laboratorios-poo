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
            return
        
        self.set_font("Carlito", "B", 8)
        self.set_text_color(*self.c_secondary)
        self.cell(100, 5, "PROGRAMACIÓN ORIENTADA A OBJETOS — LABORATORIO 13", align="L")
        self.set_font("Carlito", "I", 8)
        self.set_text_color(*self.c_muted)
        self.cell(0, 5, "CRUD Completo con Spring Boot, Service y MySQL", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        
        self.set_draw_color(*self.c_secondary)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return
        
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
    pdf.cell(0, 8, "Laboratorio 13: CRUD Completo con Spring Boot y MySQL", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "I", 11)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(0, 6, "Arquitectura en Capas (Controller-Service-Repository), Base de Datos MySQL y Vistas Unificadas", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(28)
    
    # Recuadro institucional de datos
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
    pdf.cell(0, 6, "Unidad 13 — CRUD y Conexión a Base de Datos Real", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
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
        "En el Laboratorio 12 se conectó Spring Boot a una base de datos en memoria H2. Si bien H2 es idónea para pruebas iniciales, "
        "en entornos de producción reales los datos deben almacenarse en un gestor de base de datos relacional independiente y robusto "
        "como MySQL Server, garantizando persistencia permanente incluso tras reiniciar o reinstalar la aplicación."
    )
    pdf.print_paragraph(
        "En este Laboratorio 13 se culmina la transición hacia una arquitectura de grado empresarial: se incorpora la capa de Servicio (@Service) "
        "para aislar la lógica de negocio, se conecta la aplicación a MySQL Community Server mediante el driver oficial mysql-connector-j, "
        "y se unifican las interfaces web con Thymeleaf implementando un único formulario inteligente capaz de crear y editar registros."
    )
    
    pdf.print_section_title("1.1", "Objetivos Específicos")
    pdf.print_bullet("Persistencia Externa", "Configurar la conexión a MySQL Server en localhost:3306 con el esquema 'agenda'.")
    pdf.print_bullet("Capa de Negocio (Service)", "Crear ContactoService para desacoplar el Controlador del Repositorio de acceso a datos.")
    pdf.print_bullet("CRUD Completo", "Implementar las 4 operaciones esenciales: Create (POST /guardar), Read (GET /contactos), Update (GET /editar + POST /actualizar) y Delete (GET /eliminar/{id}).")
    pdf.print_bullet("Vista Unificada", "Construir formulario.html utilizando operadores ternarios en SpEL y campos ocultos para manejar altas y modificaciones en un solo archivo.")

    pdf.print_chapter_title("2", "ARQUITECTURA EN CAPAS: CONTROLLER - SERVICE - REPOSITORY")
    pdf.print_paragraph(
        "El flujo de peticiones se estructura de acuerdo al patrón de diseño en capas (Layered Architecture):"
    )
    pdf.print_bullet("Capa Web / Controller", "Recibe la petición HTTP desde el navegador web y delega la ejecución al Service. No realiza operaciones directas sobre el Repository.")
    pdf.print_bullet("Capa de Negocio / Service", "Contiene las validaciones, reglas de negocio y orquestación transaccional (@Service). Llama a ContactoRepository.")
    pdf.print_bullet("Capa de Acceso a Datos / Repository", "Extiende JpaRepository<Contacto, Long>, permitiendo que Spring Data JPA interactúe con Hibernate.")
    pdf.print_bullet("Base de Datos MySQL", "Motor relacional persistente que ejecuta las sentencias SQL nativas (INSERT, SELECT, UPDATE, DELETE).")

    pdf.print_callout(
        "Gracias a la abstracción de Spring Data JPA y Hibernate, el cambio de H2 a MySQL solo requirió cambiar la dependencia en pom.xml y las credenciales en application.properties. El código Java de la entidad y el repositorio no sufrió alteraciones.",
        is_warning=False
    )

    pdf.print_chapter_title("3", "ESTRUCTURA DEL PROYECTO ENTREGABLE")
    tree_text = (
        "lab13_crud/\n"
        "├── pom.xml                                   # Dependencias: Web, Thymeleaf, Data JPA, MySQL Connector\n"
        "├── mvnw & mvnw.cmd                           # Scripts multiplataforma con auto-detección JDK\n"
        "├── .mvn/wrapper/maven-wrapper.properties     # Configuración oficial de Maven Wrapper 3.9.9\n"
        "├── .gitignore                                # Exclusiones de build (target/) y temporales\n"
        "├── respuestas.txt                            # Respuestas teóricas y fundamentación técnica\n"
        "├── Manual_Laboratorio_13_Santiago_Chaparro.pdf # Documento PDF institucional\n"
        "└── src/\n"
        "    ├── main/\n"
        "    │   ├── java/com/gremio/\n"
        "    │   │   ├── AgendaWebApplication.java     # Punto de entrada @SpringBootApplication\n"
        "    │   │   ├── model/\n"
        "    │   │   │   └── Contacto.java             # Entidad JPA (@Entity, @Table(name = 'contacto'))\n"
        "    │   │   ├── repository/\n"
        "    │   │   │   └── ContactoRepository.java   # Interfaz JpaRepository<Contacto, Long>\n"
        "    │   │   ├── service/\n"
        "    │   │   │   └── ContactoService.java      # Capa Service con lógica CRUD desacoplada\n"
        "    │   │   └── controller/\n"
        "    │   │       └── ContactoController.java   # Controlador MVC con rutas HTTP hacia el Service\n"
        "    │   └── resources/\n"
        "    │       ├── templates/\n"
        "    │       │   ├── contactos.html            # Tabla dinámica con acciones Editar y Eliminar\n"
        "    │       │   └── formulario.html           # Vista unificada para creación y actualización\n"
        "    │       └── application.properties        # Cadena de conexión MySQL, dialecto y ddl-auto\n"
        "    └── test/\n"
        "        ├── java/com/gremio/\n"
        "        │   └── AgendaWebApplicationTests.java # Prueba unitaria de arranque de contexto\n"
        "        └── resources/\n"
        "            └── application.properties        # Perfil de pruebas autónomo con H2 en memoria"
    )
    pdf.print_code_box("Árbol de Directorios (lab13_crud)", tree_text)

    # =========================================================================
    # IMPLEMENTACIÓN DE CÓDIGO FUENTE
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("4", "CÓDIGO FUENTE DETALLADO")
    
    with open("lab13_crud/pom.xml", "r") as f:
        pom_code = f.read()
    pdf.print_code_box("pom.xml", pom_code)
    
    with open("lab13_crud/src/main/resources/application.properties", "r") as f:
        props_code = f.read()
    pdf.print_code_box("src/main/resources/application.properties", props_code)

    pdf.add_page()
    with open("lab13_crud/src/main/java/com/gremio/AgendaWebApplication.java", "r") as f:
        app_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/AgendaWebApplication.java", app_code)

    with open("lab13_crud/src/main/java/com/gremio/model/Contacto.java", "r") as f:
        model_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/model/Contacto.java", model_code)

    pdf.add_page()
    with open("lab13_crud/src/main/java/com/gremio/repository/ContactoRepository.java", "r") as f:
        repo_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/repository/ContactoRepository.java", repo_code)

    with open("lab13_crud/src/main/java/com/gremio/service/ContactoService.java", "r") as f:
        serv_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/service/ContactoService.java", serv_code)

    pdf.add_page()
    with open("lab13_crud/src/main/java/com/gremio/controller/ContactoController.java", "r") as f:
        ctrl_code = f.read()
    pdf.print_code_box("src/main/java/com/gremio/controller/ContactoController.java", ctrl_code)

    pdf.add_page()
    with open("lab13_crud/src/main/resources/templates/formulario.html", "r") as f:
        form_html = f.read()
    pdf.print_code_box("src/main/resources/templates/formulario.html", form_html)

    pdf.add_page()
    with open("lab13_crud/src/main/resources/templates/contactos.html", "r") as f:
        contactos_html = f.read()
    pdf.print_code_box("src/main/resources/templates/contactos.html", contactos_html)

    # =========================================================================
    # PREGUNTAS DE REFLEXIÓN
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("5", "PREGUNTAS DE REFLEXIÓN Y FUNDAMENTACIÓN TEÓRICA")
    
    pdf.print_section_title("5.1", "¿Por qué agregamos la capa Service? ¿Qué problema resuelve?")
    pdf.print_paragraph(
        "La capa Service implementa el principio de Separación de Responsabilidades (SoC). El Controller debe ocuparse exclusivamente "
        "de recibir peticiones web HTTP y retornar vistas o respuestas, mientras que el Service concentra la lógica de negocio, validaciones complejas "
        "y demarcación transaccional (@Transactional).",
        space_after=2
    )
    pdf.print_paragraph(
        "Problemas resueltos:\n"
        "1. Desacoplamiento: Si cambia la persistencia o las reglas de negocio, el controlador no se altera.\n"
        "2. Reutilización (DRY): Si se añade una API REST móvil, ambos controladores reutilizan el mismo ContactoService.\n"
        "3. Testabilidad: Permite realizar pruebas unitarias aislando el controlador mediante mocks del servicio."
    )

    pdf.print_section_title("5.2", "¿Cómo sabe Thymeleaf si es Nuevo o Editar? ¿Qué papel juega el campo oculto id?")
    pdf.print_paragraph(
        "• Evaluación de condición: Thymeleaf utiliza el operador ternario '${contacto.id} != null ? ... : ...'. "
        "Al llamar a /nuevo, se pasa un 'new Contacto()' cuyo id es null, mostrando 'Nuevo Contacto' y enviando a /guardar. "
        "Al llamar a /editar/{id}, se pasa la entidad recuperada de MySQL cuyo id existe, mostrando 'Editar Contacto' y enviando a /actualizar.",
        space_after=2
    )
    pdf.print_paragraph(
        "• Papel de <input type=\"hidden\" th:field=\"*{id}\" />: Al enviar el formulario por POST, los campos no presentes en el formulario "
        "no viajan al servidor. Si no se incluye el campo oculto, el objeto Contacto llega con id = null y Hibernate ejecutaría un INSERT "
        "duplicando el registro. Con el campo oculto, el ID viaja y Hibernate sabe qué registro debe modificar con un UPDATE."
    )

    pdf.print_section_title("5.3", "¿Cómo distingue JPA entre INSERT y UPDATE con save()? Explicación de Service, @PostMapping y @GetMapping")
    pdf.print_paragraph(
        "• Lógica de save(): En SimpleJpaRepository, JPA examina 'entity.getId()'. Si es null, considera que la entidad es nueva e invoca "
        "'entityManager.persist()' generando un SQL INSERT. Si posee un ID no nulo, considera que la entidad ya existe e invoca "
        "'entityManager.merge()' generando un SQL UPDATE. Esta operación se denomina Upsert.",
        space_after=2
    )
    pdf.print_paragraph(
        "• ContactoService: Componente gestionado (@Service) que encapsula las operaciones de acceso a datos, implementando métodos seguros "
        "como 'buscarPorId' con '.orElseThrow()' para prevenir excepciones de puntero nulo.",
        space_after=2
    )
    pdf.print_paragraph(
        "• @GetMapping vs @PostMapping: @GetMapping maneja peticiones de solo lectura seguras e idempotentes (/contactos, /nuevo, /editar/{id}, /eliminar/{id}), "
        "mientras que @PostMapping procesa envíos con efectos colaterales donde los datos viajan protegidos en el cuerpo de la petición (/guardar, /actualizar)."
    )

    # =========================================================================
    # GUÍA DE EJECUCIÓN Y VALIDACIÓN
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("6", "GUÍA DE EJECUCIÓN Y VALIDACIÓN DE RESULTADOS")
    
    pdf.print_section_title("6.1", "Preparación de la Base de Datos MySQL")
    mysql_script = (
        "-- Entrar a MySQL en la terminal\n"
        "$ mysql -u root -p\n\n"
        "-- Crear la base de datos con codificación UTF-8 internacional\n"
        "CREATE DATABASE agenda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n\n"
        "-- Verificar creación\n"
        "SHOW DATABASES;\n\n"
        "-- Salir de la consola\n"
        "EXIT;"
    )
    pdf.print_code_box("Instrucciones SQL para inicializar MySQL", mysql_script)
    
    pdf.print_section_title("6.2", "Ejecución de la Aplicación")
    terminal_run_sample = (
        "$ cd lab13_crud && ./mvnw spring-boot:run\n"
        "[INFO] Scanning for projects...\n"
        "[INFO] Building agenda-crud-mysql 0.0.1-SNAPSHOT\n"
        "[INFO] --- spring-boot:run (default-cli) @ agenda-crud-mysql ---\n"
        "  .   ____          _            __ _ _\n"
        " /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\\n"
        "( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\\n"
        " \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )\n"
        "  '  |____| .__|_| |_|_| |_\\__, | / / / /\n"
        " =========|_|==============|___/=/_/_/_/\n"
        " :: Spring Boot ::                (v3.3.5)\n\n"
        "2026-11-15T19:30:00.120-06:00  INFO --- [agenda-crud-mysql] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 8080 (http)\n"
        "2026-11-15T19:30:01.350-06:00  INFO --- [agenda-crud-mysql] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...\n"
        "2026-11-15T19:30:01.890-06:00  INFO --- [agenda-crud-mysql] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection com.mysql.cj.jdbc.ConnectionImpl@...\n"
        "2026-11-15T19:30:02.100-06:00  INFO --- [agenda-crud-mysql] org.hibernate.SQL                         : create table if not exists contacto (...)\n"
        "2026-11-15T19:30:02.500-06:00  INFO --- [agenda-crud-mysql] com.gremio.AgendaWebApplication          : Started AgendaWebApplication in 2.38 seconds"
    )
    pdf.print_terminal_box(terminal_run_sample)
    
    pdf.print_chapter_title("7", "CONCLUSIONES DE LA PRÁCTICA")
    pdf.print_paragraph(
        "El Laboratorio 13 consolida el desarrollo de aplicaciones web empresariales con Java y Spring Boot. Al incorporar una "
        "base de datos relacional independiente (MySQL), se garantiza la persistencia definitiva de los datos. La adopción de la arquitectura "
        "en tres capas (Controller - Service - Repository) dota al sistema de alta mantenibilidad, escalabilidad y testabilidad, "
        "mientras que la unificación de vistas con Thymeleaf optimiza el código frontend evitando redundancias.",
        space_after=4
    )
    pdf.print_paragraph(
        "Con este laboratorio se alcanza el dominio completo del patrón MVC, el ciclo de vida de entidades JPA y el flujo CRUD integral en Java."
    )

    output_pdf = "Manual_Laboratorio_13_Santiago_Chaparro.pdf"
    pdf.output(output_pdf)
    print(f"Manual generado con éxito: {output_pdf}")
    
    pdf.output("lab13_crud/Manual_Laboratorio_13_Santiago_Chaparro.pdf")
    print("Copia generada en lab13_crud/Manual_Laboratorio_13_Santiago_Chaparro.pdf")

if __name__ == "__main__":
    generate_manual()
