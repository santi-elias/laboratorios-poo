import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ManualPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        
        # Load fonts
        self.add_font("Carlito", "", "/usr/share/fonts/google-carlito-fonts/Carlito-Regular.ttf")
        self.add_font("Carlito", "B", "/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf")
        self.add_font("Carlito", "I", "/usr/share/fonts/google-carlito-fonts/Carlito-Italic.ttf")
        self.add_font("Carlito", "BI", "/usr/share/fonts/google-carlito-fonts/Carlito-BoldItalic.ttf")
        self.add_font("Mono", "", "/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf")
        self.add_font("Mono", "B", "/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Bold.ttf")
        
        # Color palette
        self.c_primary = (26, 54, 93)      # Deep Navy #1A365D
        self.c_secondary = (43, 108, 176)  # Blue #2B6CB0
        self.c_accent = (197, 48, 48)      # Burgundy #C53030
        self.c_dark = (45, 55, 72)         # Charcoal #2D3748
        self.c_muted = (113, 128, 150)     # Gray #718096
        self.c_bg_light = (247, 250, 252)  # Soft gray #F7FAFC
        self.c_border = (226, 232, 240)    # Border #E2E8F0
        self.c_terminal_bg = (26, 32, 44)  # Terminal dark #1A202C
        self.c_terminal_fg = (72, 187, 120)# Terminal green #48BB78

    def header(self):
        if self.page_no() == 1:
            return  # No header on cover page
        
        self.set_font("Carlito", "B", 8)
        self.set_text_color(*self.c_secondary)
        self.cell(100, 5, "PROGRAMACIÓN ORIENTADA A OBJETOS — LABORATORIO 07", align="L")
        self.set_font("Carlito", "I", 8)
        self.set_text_color(*self.c_muted)
        self.cell(0, 5, "Manejo de Excepciones en Java", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        
        # Horizontal separator
        self.set_draw_color(*self.c_secondary)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return  # No footer on cover page
        
        self.set_y(-15)
        self.set_draw_color(*self.c_border)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        
        self.set_font("Carlito", "", 8)
        self.set_text_color(*self.c_muted)
        self.cell(120, 5, "Santiago Elias Chaparro | Matrícula: 2225342 | Noviembre 14 del 2026", align="L")
        self.set_font("Carlito", "B", 8)
        self.cell(0, 5, f"Página {self.page_no()} de {{nb}}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def print_chapter_title(self, num_str, title):
        self.ln(4)
        self.set_font("Carlito", "B", 14)
        self.set_text_color(*self.c_primary)
        
        # Left colored accent bar
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
        # Calculate if code fits, else page break
        line_count = len(code_text.strip().split("\n"))
        needed_height = 8 + (line_count * 3.8)
        
        if self.get_y() + needed_height > (self.h - self.b_margin) and needed_height < (self.h - 50):
            self.add_page()
            
        # Header banner for code
        self.set_fill_color(*self.c_secondary)
        self.set_text_color(255, 255, 255)
        self.set_font("Carlito", "B", 9)
        self.cell(0, 6, f"  Archivo: {filename}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Code body
        self.set_fill_color(*self.c_bg_light)
        self.set_draw_color(*self.c_border)
        self.set_line_width(0.2)
        self.set_font("Mono", "", 7.5)
        self.set_text_color(26, 32, 44)
        
        formatted_code = code_text.strip()
        self.multi_cell(0, 3.8, formatted_code, border=1, fill=True)
        self.ln(4)

    def print_terminal_box(self, output_text):
        # Terminal top bar
        self.set_fill_color(45, 55, 72)
        self.set_text_color(240, 240, 240)
        self.set_font("Carlito", "B", 8.5)
        self.cell(0, 5.5, "  Consola de Ejecución: javac --release 25 *.java && java Main", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Terminal content
        self.set_fill_color(*self.c_terminal_bg)
        self.set_text_color(*self.c_terminal_fg)
        self.set_font("Mono", "", 7.6)
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


def generate_manual_instance(page_numbers=None):
    pdf = ManualPDF()
    pdf.alias_nb_pages()
    pdf.set_margins(18, 18, 18)
    
    chapter_pages = {}
    
    # =========================================================================
    # PORTADA
    # =========================================================================
    pdf.add_page()
    
    # Outer decorative border
    pdf.set_draw_color(26, 54, 93)
    pdf.set_line_width(1.2)
    pdf.rect(10, 10, pdf.w - 20, pdf.h - 20)
    
    pdf.set_draw_color(43, 108, 176)
    pdf.set_line_width(0.4)
    pdf.rect(12, 12, pdf.w - 24, pdf.h - 24)
    
    pdf.set_y(26)
    
    # University Name
    pdf.set_font("Carlito", "B", 18)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "B", 13)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(0, 6, "FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "I", 10)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(0, 5, "Coordinación de Ciencias Computacionales e Ingeniería de Software", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(12)
    
    # Decorative line
    pdf.set_draw_color(26, 54, 93)
    pdf.set_line_width(0.8)
    pdf.line(40, pdf.get_y(), pdf.w - 40, pdf.get_y())
    pdf.ln(16)
    
    # Materia
    pdf.set_font("Carlito", "B", 12)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(0, 6, "UNIDAD DE APRENDIZAJE:", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Carlito", "B", 16)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "PROGRAMACIÓN ORIENTADA A OBJETOS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(10)
    
    # Document Type & Lab Title
    pdf.set_font("Carlito", "B", 20)
    pdf.set_text_color(197, 48, 48)
    pdf.cell(0, 9, "MANUAL DE PRÁCTICA DE LABORATORIO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "B", 15)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "Laboratorio 07: Manejo de Excepciones en Java", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Carlito", "I", 11)
    pdf.set_text_color(74, 85, 104)
    pdf.cell(0, 6, "Arquitectura Robusta y Tolerante a Fallos en un Motor RPG", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(22)
    
    # Student and Submission Details Box
    box_w = 140
    box_x = (pdf.w - box_w) / 2
    box_y = pdf.get_y()
    
    pdf.set_fill_color(247, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.4)
    pdf.rect(box_x, box_y, box_w, 62, style="FD")
    
    pdf.set_xy(box_x + 8, box_y + 6)
    
    pdf.set_font("Carlito", "B", 11)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(38, 7, "Estudiante:", align="L")
    pdf.set_font("Carlito", "B", 12)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(0, 7, "Santiago Elias Chaparro", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 8)
    pdf.set_font("Carlito", "B", 11)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(38, 7, "Matrícula:", align="L")
    pdf.set_font("Carlito", "B", 12)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 7, "2225342", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 8)
    pdf.set_font("Carlito", "B", 11)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(38, 7, "Catedrático:", align="L")
    pdf.set_font("Carlito", "", 11)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 7, "Mtro. Jorge Alberto Pineda Islas", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 8)
    pdf.set_font("Carlito", "B", 11)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(38, 7, "Semestre / Ciclo:", align="L")
    pdf.set_font("Carlito", "", 11)
    pdf.set_text_color(45, 55, 72)
    pdf.cell(0, 7, "Tercer Semestre — Agosto-Diciembre 2026", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(box_x + 8)
    pdf.set_font("Carlito", "B", 11)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(38, 7, "Fecha de Entrega:", align="L")
    pdf.set_font("Carlito", "B", 11)
    pdf.set_text_color(197, 48, 48)
    pdf.cell(0, 7, "Noviembre 14 del 2026", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(box_y + 72)
    pdf.set_font("Carlito", "I", 9.5)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(0, 5, "San Nicolás de los Garza, Nuevo León, México", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # =========================================================================
    # TABLA DE CONTENIDO / ÍNDICE
    # =========================================================================
    pdf.add_page()
    pdf.print_chapter_title("Índice", "Contenido del Manual")
    
    p = page_numbers or {}
    toc_items = [
        ("1. Objetivo de la Práctica", "Propósitos y competencias a desarrollar en la sesión", f"Pág. {p.get('ch1', 2)}"),
        ("2. Introducción y Antecedentes", "Evolución desde Lab 04-06 y problemática de estados inválidos", f"Pág. {p.get('ch2', 2)}"),
        ("3. Explicación del Tema", "Manejo de excepciones en Java, jerarquía Throwable y buenas prácticas", f"Pág. {p.get('ch3', 3)}"),
        ("4. Arquitectura y Diagrama de Excepciones", "Taxonomía de clases de error y flujo de control try-catch-finally", f"Pág. {p.get('ch4', 4)}"),
        ("5. Código Fuente del Sistema RPG", "Implementación completa comentada de las 13 clases e interfaces", f"Pág. {p.get('ch5', 5)}"),
        ("6. ScreenShoots y Outputs de la Ejecución", "Verificación exhaustiva de los 6 escenarios en tiempo de ejecución", f"Pág. {p.get('ch6', 10)}"),
        ("7. Preguntas de Reflexión (respuestas.docx)", "Respuestas teóricas rigurosas sobre Checked/Unchecked, finally, throw/throws", f"Pág. {p.get('ch7', 11)}"),
        ("8. Conclusiones y Lecciones Aprendidas", "Síntesis del impacto de las excepciones en software profesional", f"Pág. {p.get('ch8', 12)}"),
    ]
    
    for title, subtitle, page_str in toc_items:
        pdf.set_font("Carlito", "B", 10.5)
        pdf.set_text_color(*pdf.c_primary)
        pdf.cell(140, 5.5, title)
        pdf.set_font("Carlito", "B", 9.5)
        pdf.set_text_color(*pdf.c_secondary)
        pdf.cell(0, 5.5, page_str, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Carlito", "I", 9)
        pdf.set_text_color(*pdf.c_muted)
        pdf.cell(0, 4.5, f"   {subtitle}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1.5)
        
    pdf.ln(5)
    pdf.print_callout("Este manual documenta el diseño, la implementación y la validación formal del sistema de manejo de excepciones en Java para la arquitectura del videojuego RPG, asegurando tolerancia total a fallos en tiempo de ejecución.")

    # =========================================================================
    # 1. OBJETIVO
    # =========================================================================
    chapter_pages['ch1'] = pdf.page_no()
    pdf.print_chapter_title("1", "Objetivo de la Práctica")
    pdf.print_paragraph(
        "El propósito primordial de esta práctica es dotar a la arquitectura del videojuego RPG desarrollada "
        "en los laboratorios previos de un mecanismo formal y robusto de gestión de errores en tiempo de ejecución, "
        "garantizando que ninguna condición imprevista o acción inválida provoque la interrupción abrupta de la aplicación "
        "(cuelgue o crash) ni la corrupción de las variables de estado de los personajes."
    )
    
    pdf.print_bullet("Estructuras de Control Formal", "Dominar la sintaxis y semántica de los bloques try, catch y finally para capturar y contener anomalías operativas.")
    pdf.print_bullet("Excepciones de Dominio Específico", "Diseñar e implementar una jerarquía de clases de excepción personalizadas que expresen con precisión los fallos de las reglas del RPG.")
    pdf.print_bullet("Diferenciación de Taxonomías", "Distinguir de manera teórica y aplicada las excepciones chequeadas (Checked Exceptions) de las no chequeadas (Unchecked Exceptions / RuntimeException).")
    pdf.print_bullet("Cláusulas throw y throws", "Utilizar la instrucción throw para disparar eventos de error y la cláusula throws en las firmas de métodos para documentar contratos y propagación.")
    pdf.print_bullet("Auditoría y Bitácora Transaccional", "Asegurar el registro incondicional de turnos mediante el bloque finally en la clase MotorCombate.")

    # =========================================================================
    # 2. INTRODUCCIÓN
    # =========================================================================
    chapter_pages['ch2'] = pdf.page_no()
    pdf.print_chapter_title("2", "Introducción y Antecedentes")
    pdf.print_paragraph(
        "A lo largo de los laboratorios 04, 05 y 06, la jerarquía de personajes del videojuego evolucionó notablemente. "
        "En el Laboratorio 04 se implementó la herencia simple a partir de una clase Personaje concreta. En el Laboratorio 05 "
        "se integró polimorfismo dinámico para que cada clase calculara su daño de forma diferenciada. En el Laboratorio 06 "
        "se resolvió el problema conceptual de un 'personaje genérico' convirtiendo a Personaje en una clase abstracta y "
        "definiendo capacidades opcionales mediante las interfaces Hechicero y Sanador."
    )
    pdf.print_paragraph(
        "Sin embargo, el motor aún presentaba una falla de diseño crítica: no validaba situaciones imposibles o ilegales dentro del juego. "
        "Por ejemplo, se permitía infligir daño negativo (guerrero.recibirDanio(-50)), invocar curaciones sobre personajes ya derrotados o sobre "
        "referencias nulas (druida.curarAliado(null)), y ejecutar ataques sin contar con los recursos mínimos (como un arquero sin flechas o un druida sin maná)."
    )
    pdf.print_paragraph(
        "Hasta ahora, el programa se limitaba a imprimir un mensaje por consola con System.out.println() y continuaba la ejecución. "
        "En un sistema de software profesional esto es inaceptable, ya que la aplicación continúa en un estado corrupto e inconsistente. "
        "El lenguaje Java resuelve este problema proveyendo un mecanismo de excepciones basado en la clase Throwable, separando el flujo normal "
        "de ejecución del código de recuperación y contingencia."
    )

    # =========================================================================
    # 3. EXPLICACIÓN DEL TEMA
    # =========================================================================
    pdf.add_page()
    chapter_pages['ch3'] = pdf.page_no()
    pdf.print_chapter_title("3", "Explicación del Tema")
    
    pdf.print_section_title("3.1", "Jerarquía Estándar de Excepciones en Java")
    pdf.print_paragraph(
        "En Java, todos los tipos de error y condiciones anormales heredan directa o indirectamente de la clase java.lang.Throwable. "
        "A partir de Throwable se ramifican dos familias fundamentales:"
    )
    pdf.print_bullet("java.lang.Error", "Representa condiciones críticas externas a la lógica de la aplicación y difícilmente recuperables por código (por ejemplo: OutOfMemoryError, StackOverflowError). La aplicación no debe intentar capturarlas.")
    pdf.print_bullet("java.lang.Exception", "Representa condiciones anormales pero recuperables que un programa bien diseñado debe anticipar y manejar para continuar operando con estabilidad.")

    pdf.print_section_title("3.2", "Excepciones Chequeadas (Checked) vs. No Chequeadas (Unchecked)")
    pdf.print_paragraph(
        "Dentro de java.lang.Exception, la plataforma Java establece una distinción vital:"
    )
    
    # Table comparison
    pdf.set_fill_color(*pdf.c_primary)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Carlito", "B", 9)
    pdf.cell(40, 6, "  Característica", fill=True, border=1)
    pdf.cell(65, 6, "  Excepción Chequeada (Checked)", fill=True, border=1)
    pdf.cell(0, 6, "  Excepción No Chequeada (Unchecked)", fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    rows_comp = [
        ("Clase Base", "Hereda de java.lang.Exception", "Hereda de java.lang.RuntimeException"),
        ("Verificación", "Obligatoria en tiempo de compilación", "En tiempo de ejecución (Runtime)"),
        ("Exigencia sintáctica", "Requiere try-catch o firma throws", "No requiere try-catch ni throws"),
        ("Semántica", "Fallos anticipables y recuperables de negocio", "Defectos lógicos y bugs de programación"),
        ("Ejemplos en el RPG", "RpgException, PersonajeDerrotadoException", "PersonajeNuloException"),
    ]
    
    for cat, chk, unchk in rows_comp:
        pdf.set_fill_color(247, 250, 252)
        pdf.set_font("Carlito", "B", 8.5)
        pdf.set_text_color(*pdf.c_primary)
        pdf.cell(40, 5.5, f"  {cat}", fill=True, border=1)
        pdf.set_font("Carlito", "", 8.5)
        pdf.set_text_color(*pdf.c_dark)
        pdf.cell(65, 5.5, f"  {chk}", fill=True, border=1)
        pdf.cell(0, 5.5, f"  {unchk}", fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
    pdf.ln(3)

    pdf.print_section_title("3.3", "Ciclo y Mecánica de throw, throws y Bloques try-catch-finally")
    pdf.print_paragraph(
        "El manejo estructurado de errores se compone de elementos complementarios bien delimitados:"
    )
    pdf.print_bullet("Cláusula throws", "Se escribe en la firma o cabecera de un método para declarar explícitamente qué excepciones chequeadas es capaz de propagar. Obliga a quien lo invoca a asumir la responsabilidad de su captura.")
    pdf.print_bullet("Sentencia throw", "Instrucción imperativa que se coloca dentro del bloque de código para instanciar y lanzar activamente un objeto de excepción en cuanto se detecta una condición ilícita.")
    pdf.print_bullet("Bloque try", "Delimita el conjunto de instrucciones susceptibles a fallas que se someterán a vigilancia.")
    pdf.print_bullet("Bloques catch", "Capturan y neutralizan las excepciones lanzadas en el try. El orden de declaración es estricto: deben ubicarse de la clase más específica (subclase) a la más general (superclase), evitando errores de compilación por código inalcanzable.")
    pdf.print_bullet("Bloque finally", "Instrucciones de ejecución garantizada. Se ejecutan invariablemente sin importar si el bloque try terminó con éxito o si se lanzó y capturó una excepción. Resulta indispensable para auditoría y liberación de recursos.")

    # =========================================================================
    # 4. ARQUITECTURA Y DIAGRAMA
    # =========================================================================
    pdf.add_page()
    chapter_pages['ch4'] = pdf.page_no()
    pdf.print_chapter_title("4", "Arquitectura y Jerarquía de Excepciones del RPG")
    
    pdf.print_paragraph(
        "A continuación se presenta la taxonomía de excepciones creada para el videojuego, organizada de acuerdo a los principios de diseño de software:"
    )
    
    diagram_text = (
        "                    java.lang.Throwable\n"
        "                             │\n"
        "            ┌────────────────┴────────────────┐\n"
        "            │                                 │\n"
        "    java.lang.Error                  java.lang.Exception\n"
        "   (fallos críticos)                          │\n"
        "                                 ┌────────────┴────────────┐\n"
        "                                 │                         │\n"
        "                           RpgException        java.lang.RuntimeException\n"
        "                        (Base Checked RPG)                 │\n"
        "                                 │                         │\n"
        "             ┌───────────────────┼───────────────────┐     │\n"
        "             │                   │                   │     │\n"
        "  PersonajeDerrotadoException    │   AccionInvalidaException\n"
        "  (vida <= 0 en combate)         │   (daño negativo / curar muerto)\n"
        "                                 │                         │\n"
        "                    RecursoInsuficienteException           │\n"
        "                    (sin mana o sin flechas)               │\n"
        "                                                           ▼\n"
        "                                                 PersonajeNuloException\n"
        "                                                 (referencia null: Unchecked)"
    )
    
    pdf.set_fill_color(240, 244, 248)
    pdf.set_draw_color(180, 195, 210)
    pdf.set_font("Mono", "", 7.5)
    pdf.set_text_color(26, 54, 93)
    pdf.multi_cell(0, 3.8, diagram_text, border=1, fill=True)
    pdf.ln(3)

    pdf.print_section_title("4.1", "Diagrama de Clases del Sistema y Manejador de Combate")
    class_diagram = (
        "┌────────────────────────────────────────────────────────────────────────┐\n"
        "│                          «abstract» Personaje                          │\n"
        "├────────────────────────────────────────────────────────────────────────┤\n"
        "│ # nombre: String, nivel: int, puntosVida: int, estaVivo: boolean       │\n"
        "├────────────────────────────────────────────────────────────────────────┤\n"
        "│ + recibirDanio(int danio): void throws AccionInvalidaException        │\n"
        "│ + «abstract» atacar(): void throws RpgException                       │\n"
        "│ + «abstract» calcularDanio(): int                                     │\n"
        "└───────────────────────────────────┬────────────────────────────────────┘\n"
        "                                    │ extends\n"
        "             ┌──────────────────────┼──────────────────────┐\n"
        "             ▼                      ▼                      ▼\n"
        "          Arquero                 Druida               Nigromante\n"
        "     (valida vida y          (valida vida,         (valida vida y\n"
        "      flechas > 0)            mana >= 10,           mana >= 15)\n"
        "                              curarAliado)\n"
        "\n"
        "┌────────────────────────────────────────────────────────────────────────┐\n"
        "│                              MotorCombate                              │\n"
        "├────────────────────────────────────────────────────────────────────────┤\n"
        "│ - bitacora: ArrayList<String>                                          │\n"
        "├────────────────────────────────────────────────────────────────────────┤\n"
        "│ + ejecutarTurno(Personaje atacante, Personaje defensor): void          │\n"
        "│     try   { atacante.atacar(); defensor.recibirDanio(...); }           │\n"
        "│     catch (PersonajeDerrotadoException e)   { registrar DERROTA }      │\n"
        "│     catch (RecursoInsuficienteException e)  { registrar SIN RECURSO }  │\n"
        "│     catch (RpgException e)                  { registrar ERROR RPG }    │\n"
        "│     finally { bitacora.add(...); System.out.println(Turno registrado); }│\n"
        "│ + mostrarBitacora(): void                                              │\n"
        "└────────────────────────────────────────────────────────────────────────┘"
    )
    
    pdf.set_fill_color(247, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_font("Mono", "", 7.2)
    pdf.set_text_color(45, 55, 72)
    pdf.multi_cell(0, 3.5, class_diagram, border=1, fill=True)
    pdf.ln(3)

    # =========================================================================
    # 5. CÓDIGO FUENTE
    # =========================================================================
    pdf.add_page()
    chapter_pages['ch5'] = pdf.page_no()
    pdf.print_chapter_title("5", "Código Fuente del Sistema RPG")
    pdf.print_paragraph(
        "A continuación se documenta el código fuente íntegro de los 13 módulos del proyecto, "
        "desarrollados de acuerdo a las pautas de clean code y modularidad exigidas en la práctica:"
    )

    src_dir = "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones"
    
    def read_src(name):
        path = os.path.join(src_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    pdf.print_section_title("5.1", "Jerarquía de Excepciones del Dominio")
    pdf.print_code_box("RpgException.java", read_src("RpgException.java"))
    pdf.print_code_box("PersonajeDerrotadoException.java", read_src("PersonajeDerrotadoException.java"))
    pdf.print_code_box("RecursoInsuficienteException.java", read_src("RecursoInsuficienteException.java"))
    pdf.print_code_box("AccionInvalidaException.java", read_src("AccionInvalidaException.java"))
    pdf.print_code_box("PersonajeNuloException.java", read_src("PersonajeNuloException.java"))

    pdf.add_page()
    pdf.print_section_title("5.2", "Interfaces y Clase Abstracta Base")
    pdf.print_code_box("Hechicero.java", read_src("Hechicero.java"))
    pdf.print_code_box("Sanador.java", read_src("Sanador.java"))
    pdf.print_code_box("Personaje.java", read_src("Personaje.java"))

    pdf.add_page()
    pdf.print_section_title("5.3", "Clases Concretas con Validación de Estados y Recursos")
    pdf.print_code_box("Arquero.java", read_src("Arquero.java"))
    pdf.print_code_box("Druida.java", read_src("Druida.java"))
    pdf.print_code_box("Nigromante.java", read_src("Nigromante.java"))
    
    pdf.add_page()
    pdf.print_section_title("5.4", "Motor de Combate y Clase Principal")
    pdf.print_code_box("MotorCombate.java", read_src("MotorCombate.java"))
    pdf.print_code_box("Main.java", read_src("Main.java"))

    # =========================================================================
    # 6. OUTPUTS / SCREENSHOTS
    # =========================================================================
    pdf.add_page()
    chapter_pages['ch6'] = pdf.page_no()
    pdf.print_chapter_title("6", "ScreenShoots y Outputs de la Ejecución")
    pdf.print_paragraph(
        "A continuación se presenta la salida real generada por la terminal al compilar y ejecutar el proyecto con OpenJDK 25. "
        "Dicha corrida cubre de forma exhaustiva los seis escenarios solicitados en los criterios de evaluación:"
    )

    terminal_output = (
        "=== RPG — Sistema con Manejo de Excepciones ===\n\n"
        "--- Turno: Sylva vs Malachar ---\n"
        "[Sylva] invoca raíces del bosque y ataca con furia natural.\n"
        "Malachar recibe 265 de daño. Vida: 0\n"
        "Malachar ha sido derrotado.\n"
        "[Bitácora] Turno registrado.\n"
        "Sylva recibe 9999 de daño. Vida: 0\n"
        "Sylva ha sido derrotado.\n\n"
        "--- Turno: Sylva vs Malachar ---\n"
        "⚠ El personaje 'Sylva' está derrotado y no puede realizar esta acción.\n"
        "[Bitácora] Turno registrado.\n\n"
        "--- Turno: Legolas vs Malachar ---\n"
        "⚠ Recurso insuficiente: flechas. Disponible: 0\n"
        "[Bitácora] Turno registrado.\n\n"
        "-- Intento de curar aliado derrotado --\n"
        "No se pudo curar: Acción inválida 'curarAliado': No se puede curar a un personaje derrotado\n\n"
        "-- Bloque manual try-catch-finally --\n"
        "Capturado: Acción inválida 'recibirDanio': El daño no puede ser negativo: -50\n"
        "El bloque finally siempre se ejecuta.\n\n"
        "=== Bitácora de Combate ===\n"
        "1. OK           | Sylva atacó a Malachar (daño: 265)\n"
        "2. DERROTA      | Sylva no pudo actuar\n"
        "3. SIN RECURSO  | Legolas no pudo atacar"
    )
    
    pdf.print_terminal_box(terminal_output)
    
    pdf.print_section_title("6.1", "Análisis Detallado de los 6 Escenarios Demostrados")
    scenarios_desc = [
        ("Escenario 1 (Turno Normal)", "Sylva (Druida) ataca a Malachar (Nigromante). Se calculan 265 puntos de daño, se restan 10 puntos de maná a Sylva, y Malachar recibe el daño hasta caer a 0 de vida. Se registra OK en la bitácora."),
        ("Escenario 2 (Personaje Derrotado)", "Tras sufrir 9999 de daño letal, Sylva intenta atacar. El motor intercepta PersonajeDerrotadoException; el juego no colapsa y se registra el evento DERROTA en la bitácora."),
        ("Escenario 3 (Recurso Insuficiente)", "Legolas (Arquero) es instanciado con 0 flechas e intenta atacar. El método atacar() valida flechasDisponibles <= 0 y detona RecursoInsuficienteException. Se captura y se registra SIN RECURSO."),
        ("Escenario 4 (Curación Inválida)", "Eldrin (Druida sanador) intenta curar a Sylva, quien ya se encuentra derrotada. Se dispara AccionInvalidaException impidiendo restaurar vida a un personaje caído."),
        ("Escenario 5 (Daño Negativo y finally)", "Se intenta aplicar -50 de daño a Malachar. El método recibirDanio valida danio < 0 y lanza AccionInvalidaException. El bloque finally ejecuta obligatoriamente su mensaje confirmando la garantía de terminación."),
        ("Escenario 6 (Bitácora Transaccional)", "La clase MotorCombate despliega la bitácora consolidada demostrando que los turnos fueron auditados con éxito independientemente de los fallos surgidos."),
    ]
    
    for s_title, s_desc in scenarios_desc:
        pdf.print_bullet(s_title, s_desc)

    # =========================================================================
    # 7. PREGUNTAS DE REFLEXIÓN
    # =========================================================================
    pdf.add_page()
    chapter_pages['ch7'] = pdf.page_no()
    pdf.print_chapter_title("7", "Preguntas de Reflexión (respuestas.docx)")
    pdf.print_paragraph(
        "A continuación se transcriben las respuestas a las tres preguntas teóricas formativas requeridas para la entrega:"
    )

    pdf.print_section_title("Pregunta 1", "¿Cuál es la diferencia entre una excepción chequeada y una no chequeada? ¿Por qué PersonajeNuloException extiende RuntimeException y no Exception?")
    pdf.print_paragraph(
        "Respuesta:\n"
        "La diferencia fundamental radica en el momento de verificación por parte del compilador de Java:\n"
        "• Excepciones Chequeadas (Checked): Heredan directamente de java.lang.Exception. El compilador de Java exige estrictamente "
        "que el desarrollador las atienda mediante un bloque try-catch o las declare explícitamente en la firma del método mediante la cláusula throws. "
        "Se utilizan para modelar contingencias normales del entorno o del dominio de negocio que un programa bien concebido puede anticipar, "
        "mitigar y recuperarse de ellas (por ejemplo, quedarse sin maná, o que un personaje ya esté derrotado).\n\n"
        "• Excepciones No Chequeadas (Unchecked): Heredan de java.lang.RuntimeException. El compilador no exige ni su captura ni su declaración en la firma. "
        "Representan fallas de lógica, bugs de programación o violaciones a contratos del código que no deberían ocurrir si el software estuviera correctamente programado.\n\n"
        "Justificación de PersonajeNuloException:\n"
        "PersonajeNuloException extiende RuntimeException porque pasar una referencia null a métodos críticos como ejecutarTurno() o curarAliado() "
        "constituye un error imputable al programador que invoca la función (una negligencia que debe solventarse antes de llamar al método mediante comprobaciones previas), "
        "y no una condición ordinaria del juego. Obligar a declarar throws PersonajeNuloException en todos los métodos saturaría el código de firmas innecesarias."
    )

    pdf.print_section_title("Pregunta 2", "¿Para qué sirve el bloque finally? Da un ejemplo real de cuándo es indispensable.")
    pdf.print_paragraph(
        "Respuesta:\n"
        "El bloque finally garantiza la ejecución incondicional de un conjunto de sentencias, sin importar si el bloque try concluyó exitosamente, "
        "si una excepción fue interceptada por un catch, o si una excepción no capturada aborta el contexto de ejecución actual.\n\n"
        "Ejemplo real indispensable en la industria:\n"
        "La liberación de recursos a nivel de Sistema Operativo, tales como conexiones a bases de datos relacionales (java.sql.Connection), "
        "descriptores de archivos (FileInputStream / FileOutputStream) o canales de comunicación en red (java.net.Socket). "
        "Si ocurre un error durante la lectura o consulta de datos, el archivo o la conexión quedarían bloqueados en la memoria del sistema operativo indefinidamente, "
        "provocando fugas de recursos (resource leaks) y saturación del servidor. El bloque finally (o el mecanismo try-with-resources) "
        "garantiza el cierre formal del recurso mediante el método close(), asegurando la estabilidad del servidor."
    )

    pdf.print_section_title("Pregunta 3", "¿Cuál es la diferencia entre throw y throws? Muestra un ejemplo de cada uno tomado de este laboratorio.")
    pdf.print_paragraph(
        "Respuesta:\n"
        "1. throws (con 's' al final): Es una palabra reservada utilizada en la cabecera (firma) de un método para anunciar y advertir al compilador "
        "y a otros desarrolladores que dicho método es susceptible de propagar una o más excepciones chequeadas, delegando su manejo al llamador.\n"
        "   Ejemplos del laboratorio:\n"
        "   • public abstract void atacar() throws RpgException;\n"
        "   • public void recibirDanio(int danio) throws AccionInvalidaException;\n\n"
        "2. throw (sin 's'): Es una sentencia imperativa ejecutable que se utiliza dentro del cuerpo de un método para instanciar y detonar activamente "
        "un objeto de excepción en el instante exacto en que se detecta una violación a las reglas.\n"
        "   Ejemplo del laboratorio:\n"
        "   if (flechasDisponibles <= 0) {\n"
        "       throw new RecursoInsuficienteException(\"flechas\", flechasDisponibles);\n"
        "   }"
    )

    # =========================================================================
    # 8. CONCLUSIONES
    # =========================================================================
    pdf.add_page()
    chapter_pages['ch8'] = pdf.page_no()
    pdf.print_chapter_title("8", "Conclusiones")
    
    conclusiones_list = [
        ("Tolerancia a Fallos y Robustez", "La introducción del sistema de excepciones transforma el motor RPG en un software resistente, eliminando la corrupción de variables por daño negativo o curaciones inválidas."),
        ("Separación de Responsabilidades", "Se logra desacoplar de manera limpia la detección del error (throw en Arquero, Druida, Personaje) de su resolución y reporte (catch y finally en MotorCombate), haciendo el código altamente mantenible."),
        ("Riqueza Semántica del Dominio", "El diseño de una jerarquía especializada (RpgException y sus subtipos) comunica con absoluta claridad la causa de las fallas de juego, superando con creces el uso de excepciones genéricas o mensajes de texto efímeros."),
        ("Garantía de Auditoría Transaccional", "El empleo del bloque finally demostró cómo asegurar que la bitácora de combate registre puntualmente cada evento, un patrón idéntico al empleado en sistemas financieros y empresariales críticos."),
        ("Madurez del Diseño Orientado a Objetos", "La integración armónica de Clases Abstractas, Interfaces, Polimorfismo Dinámico y Manejo de Excepciones consolida una comprensión profunda de las mejores prácticas de la ingeniería de software en Java.")
    ]
    
    for c_title, c_desc in conclusiones_list:
        pdf.print_bullet(c_title, c_desc)
        
    pdf.ln(8)
    
    # Signature box
    sig_w = 120
    sig_x = (pdf.w - sig_w) / 2
    sig_y = pdf.get_y() + 10
    
    pdf.set_draw_color(45, 55, 72)
    pdf.set_line_width(0.4)
    pdf.line(sig_x, sig_y, sig_x + sig_w, sig_y)
    
    pdf.set_xy(sig_x, sig_y + 2)
    pdf.set_font("Carlito", "B", 10.5)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(sig_w, 5, "Santiago Elias Chaparro", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Carlito", "", 9.5)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(sig_w, 4.5, "Matrícula: 2225342 | Alumno Titular", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(sig_w, 4.5, "Facultad de Ingeniería Mecánica y Eléctrica — UANL", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return pdf, chapter_pages


def build_manual_pdf(pdf_path):
    # Pass 1: compute exact page numbers
    temp_pdf, pages_dict = generate_manual_instance(None)
    
    # Pass 2: generate with accurate page numbers in Table of Contents
    final_pdf, _ = generate_manual_instance(pages_dict)
    final_pdf.output(pdf_path)
    print(f"Manual en PDF generado exitosamente en: {pdf_path}")
    print(f"Páginas de capítulos detectadas: {pages_dict}")


if __name__ == "__main__":
    out_pdf = "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Manual_Laboratorio_07_Santiago_Chaparro.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    build_manual_pdf(out_pdf)
