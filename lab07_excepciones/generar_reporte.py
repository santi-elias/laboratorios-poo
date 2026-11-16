import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_report():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # ==================== PORTADA ====================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(80)
    title_p.paragraph_format.space_after = Pt(10)
    
    run_uni = title_p.add_run("UNIVERSIDAD TECNOLÓGICA / INSTITUTO TECNOLÓGICO\n")
    run_uni.font.size = Pt(16)
    run_uni.font.bold = True
    run_uni.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    run_sub = title_p.add_run("FACULTAD DE INGENIERÍA / CIENCIAS COMPUTACIONALES\n\n\n")
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    p_materia = doc.add_paragraph()
    p_materia.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_materia.paragraph_format.space_after = Pt(20)
    run_mat = p_materia.add_run("PROGRAMACIÓN ORIENTADA A OBJETOS")
    run_mat.font.size = Pt(15)
    run_mat.font.bold = True
    run_mat.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    p_lab = doc.add_paragraph()
    p_lab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lab.paragraph_format.space_after = Pt(120)
    run_lab_num = p_lab.add_run("Laboratorio 07\n")
    run_lab_num.font.size = Pt(18)
    run_lab_num.font.bold = True
    run_lab_num.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    run_lab_tit = p_lab.add_run("Manejo de Excepciones en Java (RPG Engine)")
    run_lab_tit.font.size = Pt(14)
    run_lab_tit.font.italic = True
    run_lab_tit.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    p_datos = doc.add_paragraph()
    p_datos.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_datos.paragraph_format.space_before = Pt(60)
    p_datos.paragraph_format.space_after = Pt(5)
    run_alumno = p_datos.add_run("Estudiante: Santiago / Equipo de Desarrollo\n")
    run_alumno.font.size = Pt(12)
    run_alumno.font.bold = True
    run_docente = p_datos.add_run("Docente: Mtro. Jorge Alberto Pineda\n")
    run_docente.font.size = Pt(12)
    run_periodo = p_datos.add_run("Ciclo: Ago-Dic 2025 | Fecha: Octubre 2026")
    run_periodo.font.size = Pt(11)
    run_periodo.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    doc.add_page_break()

    # Helper function for section headings
    def add_section_h1(text):
        h = doc.add_heading(level=1)
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(8)
        run = h.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return h

    def add_section_h2(text):
        h = doc.add_heading(level=2)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(6)
        run = h.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
        return h

    # ==================== 1. OBJETIVO ====================
    add_section_h1("1. Objetivo")
    p_obj = doc.add_paragraph(
        "El objetivo principal de esta práctica de laboratorio es diseñar, implementar y verificar un sistema "
        "robusto de manejo de errores en tiempo de ejecución para el motor de combate de un videojuego RPG en Java, "
        "logrando los siguientes aprendizajes clave:"
    )
    p_obj.paragraph_format.space_after = Pt(6)

    items_obj = [
        "Comprender y aplicar la sintaxis formal de control de flujo con bloques try, catch y finally.",
        "Diseñar e implementar una jerarquía de excepciones personalizadas de negocio adaptadas a las reglas del juego.",
        "Diferenciar de forma práctica y teórica las excepciones chequeadas (Checked Exceptions) de las no chequeadas (Unchecked Exceptions).",
        "Emplear apropiadamente las palabras reservadas throw (para detonar fallos) y throws (para documentar y propagar firmas en métodos).",
        "Implementar un mecanismo de bitácora transaccional para garantizar la continuidad del flujo sin interrupciones abruptas del programa."
    ]
    for item in items_obj:
        bp = doc.add_paragraph(item, style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)

    # ==================== 2. INTRODUCCIÓN ====================
    add_section_h1("2. Introducción")
    p_intro1 = doc.add_paragraph(
        "En los laboratorios previos (Lab 04, 05 y 06) se construyó progresivamente una arquitectura de software orientada "
        "a objetos para un videojuego RPG, comenzando con herencia simple, luego evolucionando a polimorfismo dinámico y finalmente "
        "reestructurando el dominio con clases abstractas (Personaje) e interfaces funcionales (Hechicero, Sanador). "
        "No obstante, dicho diseño padecía de una deficiencia crítica: no validaba situaciones imposibles o ilegales dentro del juego. "
        "Por ejemplo, se permitía infligir daño negativo, intentar disparar con cero flechas, o invocar curaciones sobre personajes ya eliminados o nulos."
    )
    p_intro1.paragraph_format.space_after = Pt(6)

    p_intro2 = doc.add_paragraph(
        "Manejar estos escenarios imprimiendo un simple System.out.println() es insuficiente y peligroso en software real, pues el estado del "
        "juego se corrompe silenciosamente. Java provee un mecanismo formal basado en objetos Throwable, permitiendo separar la lógica normal "
        "de negocio de las rutinas de contingencia y recuperación. En esta práctica se transforma el motor de combate en un sistema "
        "tolerante a fallos mediante el uso de excepciones específicas del dominio."
    )
    p_intro2.paragraph_format.space_after = Pt(10)

    # ==================== 3. EXPLICACIÓN DEL TEMA ====================
    add_section_h1("3. Explicación del Tema")
    
    add_section_h2("3.1 Jerarquía de Excepciones en Java y en el RPG")
    p_exp1 = doc.add_paragraph(
        "En la biblioteca estándar de Java, todas las excepciones heredan de Throwable. De ahí se derivan Error (fallos irrecuperables de la JVM) "
        "y Exception (condiciones recuperables del programa). A su vez, Exception se bifurca en dos grandes categorías:"
    )
    p_exp1.paragraph_format.space_after = Pt(4)

    p_exp_checked = doc.add_paragraph(
        "• Excepciones Chequeadas (Checked): Heredan directamente de Exception. El compilador exige obligatoriamente que se manejen con "
        "try-catch o se declaren con throws en la firma del método. Representan condiciones imprevistas del entorno o fallos de negocio recuperables. "
        "En nuestro sistema: RpgException, PersonajeDerrotadoException, RecursoInsuficienteException y AccionInvalidaException.",
        style='List Bullet'
    )
    p_exp_checked.paragraph_format.space_after = Pt(3)

    p_exp_unchecked = doc.add_paragraph(
        "• Excepciones No Chequeadas (Unchecked): Heredan de RuntimeException. Representan errores de lógica o defectos de programación "
        "(como pasar null o un índice fuera de rango). No obligan al programador a declarar throws ni a capturarlas con try-catch. "
        "En nuestro sistema: PersonajeNuloException.",
        style='List Bullet'
    )
    p_exp_unchecked.paragraph_format.space_after = Pt(6)

    # Diagram Table
    table = doc.add_table(rows=6, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Clase de Excepción", "Tipo", "Propósito en el RPG"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "1A365D")
        for p in cell.paragraphs:
            p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(10)

    data = [
        ("RpgException", "Checked (Exception)", "Excepción raíz del juego; agrupa todos los fallos esperados del combate."),
        ("PersonajeDerrotadoException", "Checked (RpgException)", "Lanzada cuando un personaje con vida = 0 intenta atacar o curar."),
        ("RecursoInsuficienteException", "Checked (RpgException)", "Lanzada cuando faltan flechas en el Arquero o maná en Druida/Nigromante."),
        ("AccionInvalidaException", "Checked (RpgException)", "Lanzada ante operaciones ilícitas: daño negativo o curar a un muerto."),
        ("PersonajeNuloException", "Unchecked (RuntimeException)", "Lanzada cuando un atacante o aliado es pasado como null (error del dev).")
    ]
    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            for p in cell.paragraphs:
                p.runs[0].font.size = Pt(9.5)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F7FAFC")

    p_espacio = doc.add_paragraph()
    p_espacio.paragraph_format.space_after = Pt(6)

    add_section_h2("3.2 Estructura del Bloque try-catch-finally")
    p_tcf = doc.add_paragraph(
        "El motor de combate (MotorCombate) encapsula la interacción entre atacante y defensor dentro de una estructura jerárquica de bloques catch. "
        "El orden es fundamental: se capturan primero las excepciones más específicas (subclases como PersonajeDerrotadoException y RecursoInsuficienteException) "
        "y al final la excepción general (RpgException). El bloque finally se ejecuta de manera incondicional, tanto si la acción fue exitosa "
        "como si ocurrió un error, sirviendo para registrar la finalización del turno en la bitácora."
    )
    p_tcf.paragraph_format.space_after = Pt(10)

    # ==================== 4. CÓDIGO FUENTE ====================
    add_section_h1("4. Código Fuente")
    doc.add_paragraph(
        "A continuación se presenta el código fuente modularizado del sistema, organizado en sus 13 archivos correspondientes:"
    )

    source_files = [
        ("RpgException.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/RpgException.java", "Excepción base chequeada del juego RPG."),
        ("PersonajeDerrotadoException.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/PersonajeDerrotadoException.java", "Excepción chequeada cuando el personaje está derrotado."),
        ("RecursoInsuficienteException.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/RecursoInsuficienteException.java", "Excepción chequeada por falta de maná o flechas."),
        ("AccionInvalidaException.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/AccionInvalidaException.java", "Excepción chequeada por acciones no permitidas en el estado actual."),
        ("PersonajeNuloException.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/PersonajeNuloException.java", "Excepción no chequeada ante referencias nulas."),
        ("Hechicero.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Hechicero.java", "Interfaz que define la capacidad de lanzar hechizos y maná."),
        ("Sanador.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Sanador.java", "Interfaz que define la capacidad de curar aliados."),
        ("Personaje.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Personaje.java", "Clase base abstracta con validación de daño negativo en recibirDanio()."),
        ("Arquero.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Arquero.java", "Clase concreta con validación de vida y flechas."),
        ("Druida.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Druida.java", "Clase híbrida con validación de vida, maná y curación segura."),
        ("Nigromante.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Nigromante.java", "Clase oscura con validación de vida y maná."),
        ("MotorCombate.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/MotorCombate.java", "Motor que procesa turnos con try-catch-finally y bitácora."),
        ("Main.java", "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Main.java", "Clase principal que demuestra los 6 escenarios de prueba requeridos.")
    ]

    for fname, fpath, fdesc in source_files:
        add_section_h2(f"4.{source_files.index((fname, fpath, fdesc))+1} {fname}")
        p_desc = doc.add_paragraph(fdesc)
        p_desc.paragraph_format.space_after = Pt(4)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            code_text = f.read()

        # Add code box
        code_p = doc.add_paragraph()
        code_p.paragraph_format.space_before = Pt(4)
        code_p.paragraph_format.space_after = Pt(8)
        code_run = code_p.add_run(code_text)
        code_run.font.name = 'Courier New'
        code_run.font.size = Pt(8.5)
        code_run.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)

    # ==================== 5. OUTPUTS DE LA EJECUCIÓN ====================
    add_section_h1("5. ScreenShots / Outputs de la Ejecución")
    doc.add_paragraph(
        "A continuación se presenta la salida completa generada por la consola al compilar y ejecutar el programa "
        "con Java OpenJDK (javac --release 25 *.java && java Main), cubriendo punto por punto los seis escenarios solicitados:"
    )

    output_text = (
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
        "3. SIN RECURSO  | Legolas no pudo atacar\n"
    )

    out_p = doc.add_paragraph()
    out_p.paragraph_format.space_before = Pt(6)
    out_p.paragraph_format.space_after = Pt(12)
    out_run = out_p.add_run(output_text)
    out_run.font.name = 'Courier New'
    out_run.font.size = Pt(9)
    out_run.font.bold = True
    out_run.font.color.rgb = RGBColor(0x00, 0x4D, 0x40)

    # ==================== 6. PREGUNTAS DE REFLEXIÓN ====================
    add_section_h1("6. Preguntas de Reflexión (respuestas.docx)")

    add_section_h2("6.1 Diferencia entre excepción chequeada y no chequeada")
    doc.add_paragraph(
        "• Pregunta: ¿Cuál es la diferencia entre una excepción chequeada y una no chequeada? "
        "¿Por qué PersonajeNuloException extiende RuntimeException y no Exception?\n\n"
        "• Respuesta: La diferencia fundamental radica en la verificación durante el tiempo de compilación. "
        "Las excepciones chequeadas (Checked, derivadas directamente de Exception) obligan al programador a declarar "
        "la cláusula throws en el método o capturarlas mediante un bloque try-catch; se emplean para contingencias predecibles "
        "y recuperables del dominio o del entorno. En contraste, las excepciones no chequeadas (Unchecked, derivadas de RuntimeException) "
        "no son exigidas por el compilador, ya que representan fallos de lógica o errores del desarrollador (bugs). "
        "PersonajeNuloException hereda de RuntimeException porque pasar una referencia null a un método de combate "
        "es una falla de programación del desarrollador que debió evitarse antes de invocar la rutina, y no una condición normal del juego."
    )

    add_section_h2("6.2 Utilidad del bloque finally")
    doc.add_paragraph(
        "• Pregunta: ¿Para qué sirve el bloque finally? Da un ejemplo real de cuándo es indispensable.\n\n"
        "• Respuesta: El bloque finally asegura la ejecución incondicional de un conjunto de instrucciones de limpieza o cierre, "
        "independientemente de si el bloque try terminó con normalidad o si fue interrumpido por una excepción. "
        "Un ejemplo real e indispensable en la industria es la gestión de recursos de entrada/salida (I/O) y conexiones a bases de datos: "
        "si se abre un FileInputStream, un Socket de red o una conexión JDBC, es imprescindible invocar close() dentro del bloque finally "
        "(o mediante try-with-resources) para evitar fugas de memoria, conexiones colgadas o bloqueos de archivos en el sistema operativo."
    )

    add_section_h2("6.3 Diferencia entre throw y throws")
    doc.add_paragraph(
        "• Pregunta: ¿Cuál es la diferencia entre throw y throws? Muestra un ejemplo de cada uno tomado de este laboratorio.\n\n"
        "• Respuesta: \n"
        "1. throws se utiliza en la cabecera o firma de un método para declarar explícitamente qué excepciones de tipo chequeado "
        "podrían propagarse hacia quien lo invoque, delegando la responsabilidad del manejo.\n"
        "   Ejemplo del laboratorio:\n"
        "   public abstract void atacar() throws RpgException;\n"
        "   public void recibirDanio(int danio) throws AccionInvalidaException\n\n"
        "2. throw es la sentencia ejecutable que se utiliza dentro del cuerpo de un método para instanciar y detonar activamente "
        "un objeto de excepción en el momento en que se detecta la condición de fallo.\n"
        "   Ejemplo del laboratorio:\n"
        "   if (flechasDisponibles <= 0) {\n"
        "       throw new RecursoInsuficienteException(\"flechas\", flechasDisponibles);\n"
        "   }"
    )

    # ==================== 7. CONCLUSIONES ====================
    add_section_h1("7. Conclusiones")
    conclusiones = [
        "Robustez y Prevención de Corrupción de Estado: El manejo estructurado de excepciones garantiza que ante acciones inválidas (daño negativo, recursos agotados), el videojuego no deteriore sus variables de estado ni se interrumpa bruscamente.",
        "Separación de Responsabilidades: La separación entre el lanzamiento del error (throw en Druida, Arquero, etc.) y su captura/registro (catch y finally en MotorCombate) promueve un código limpio y desacoplado.",
        "Jerarquías Semánticas: Crear clases de excepción propias del dominio (RpgException) otorga una riqueza semántica invaluable frente a excepciones genéricas, facilitando el diagnóstico y mantenimiento del software.",
        "Garantía de Auditoría mediante finally: El uso del bloque finally para la bitácora demostró cómo asegurar que cada evento de combate quede fehacientemente registrado, sentando bases sólidas para sistemas empresariales y de simulación."
    ]
    for c in conclusiones:
        cp = doc.add_paragraph(c, style='List Bullet')
        cp.paragraph_format.space_after = Pt(4)

    output_path = "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/Reporte_Laboratorio_07.docx"
    doc.save(output_path)
    print(f"Documento Word guardado exitosamente en: {output_path}")

    # Guardar también respuestas.docx requerido por la práctica
    resp_doc = Document()
    resp_doc.add_heading("Laboratorio 07 — Preguntas de Reflexión", level=1)
    p_aut = resp_doc.add_paragraph("Estudiante: Santiago | Materia: Programación Orientada a Objetos\n")
    p_aut.paragraph_format.space_after = Pt(12)

    h1 = resp_doc.add_heading("1. ¿Cuál es la diferencia entre una excepción chequeada y una no chequeada? ¿Por qué PersonajeNuloException extiende RuntimeException y no Exception?", level=2)
    resp_doc.add_paragraph(
        "Respuesta: Las excepciones chequeadas (Checked) heredan de java.lang.Exception y el compilador exige obligatoriamente "
        "que sean gestionadas con try-catch o declaradas con throws en la firma del método. Se usan para condiciones externas "
        "o de negocio que un programa bien escrito puede anticipar y recuperar (como recursos insuficientes o acciones no permitidas en combate).\n\n"
        "Las excepciones no chequeadas (Unchecked) heredan de java.lang.RuntimeException y el compilador no impone su captura o declaración. "
        "Representan fallos de programación o errores lógicos internos que deben corregirse en el código. "
        "PersonajeNuloException hereda de RuntimeException porque pasar una referencia nula (null) a ejecutarTurno() o curarAliado() "
        "es una negligencia o error del programador que invoca el método, por lo que no debe forzar a ensuciar todo el código con firmas throws obligatorias."
    )

    h2 = resp_doc.add_heading("2. ¿Para qué sirve el bloque finally? Da un ejemplo real de cuándo es indispensable.", level=2)
    resp_doc.add_paragraph(
        "Respuesta: El bloque finally garantiza que un bloque de código se ejecutará siempre, sin importar si el bloque try concluyó con éxito, "
        "si se capturó una excepción en un bloque catch, o incluso si una excepción no capturada aborta el contexto actual.\n\n"
        "Un ejemplo real indispensable es la liberación de recursos críticos del sistema operativo, tales como streams de archivos (FileInputStream, "
        "FileOutputStream), sockets de red o conexiones a bases de datos (Connection, PreparedStatement). Si ocurre un error leyendo un archivo "
        "o consultando la base de datos, el archivo o la conexión quedarían bloqueados en memoria indefinidamente a menos que se invoque close() "
        "dentro del bloque finally."
    )

    h3 = resp_doc.add_heading("3. ¿Cuál es la diferencia entre throw y throws? Muestra un ejemplo de cada uno tomado de este laboratorio.", level=2)
    resp_doc.add_paragraph(
        "Respuesta:\n"
        "• throws (en plural): Es una palabra clave que se ubica en la firma de un método para notificar a los clientes del método que este "
        "puede llegar a propagar una o más excepciones chequeadas. Ejemplo:\n"
        "   public abstract void atacar() throws RpgException;\n"
        "   public void recibirDanio(int danio) throws AccionInvalidaException;\n\n"
        "• throw (en singular): Es una instrucción ejecutable que se utiliza dentro de un método para instanciar y detonar activamente "
        "una excepción, interrumpiendo el flujo normal de control. Ejemplo:\n"
        "   if (flechasDisponibles <= 0) {\n"
        "       throw new RecursoInsuficienteException(\"flechas\", flechasDisponibles);\n"
        "   }"
    )

    resp_path = "/home/santi/Documents/antigravity/peaceful-chandrasekhar/lab07_excepciones/respuestas.docx"
    resp_doc.save(resp_path)
    print(f"Documento respuestas.docx guardado en: {resp_path}")

create_report()
