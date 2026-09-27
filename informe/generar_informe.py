"""Genera informe/Informe_semana8_diabetes.pdf (máximo 4 páginas).
Requiere haber ejecutado antes: python informe/figuras_semana8.py"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

INK, INK2, BLUE, LINE, SOFT = colors.HexColor("#1f1f1e"), colors.HexColor("#52514e"), colors.HexColor("#2a78d6"), \
    colors.HexColor("#d9d8d3"), colors.HexColor("#eef4fc")
body = ParagraphStyle("b", fontName="DV", fontSize=8.6, leading=11.4, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=3.5)
small = ParagraphStyle("s", parent=body, fontSize=7.6, leading=9.6, alignment=0, spaceAfter=0)
cap = ParagraphStyle("c", parent=body, fontName="DVI", fontSize=7.4, leading=9.4, textColor=INK2, spaceAfter=6)
h1 = ParagraphStyle("h1", fontName="DVB", fontSize=15.5, leading=19, textColor=INK, spaceAfter=2)
sub = ParagraphStyle("sub", fontName="DV", fontSize=8.8, leading=11.5, textColor=INK2, spaceAfter=8)
h2 = ParagraphStyle("h2", fontName="DVB", fontSize=10.6, leading=13.5, textColor=BLUE, spaceBefore=7, spaceAfter=3.5)
bul = ParagraphStyle("bul", parent=body, leftIndent=10, bulletIndent=1, spaceAfter=2)
kpi_n = ParagraphStyle("kn", fontName="DVB", fontSize=15, leading=18, textColor=BLUE)
kpi_t = ParagraphStyle("kt", fontName="DV", fontSize=7.2, leading=9, textColor=INK2)

P = lambda t, s=body: Paragraph(t, s)
B = lambda t: Paragraph(t, bul, bulletText="•")

def table(rows, widths, header=True, fs=7.5):
    st = ParagraphStyle("t", parent=small, fontSize=fs, leading=fs * 1.25)
    sth = ParagraphStyle("th", parent=st, fontName="DVB", textColor=colors.white)
    data = [[Paragraph(str(c), sth if (header and i == 0) else st) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), .4, LINE),
             ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
             ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), BLUE)]
    t.setStyle(TableStyle(style)); return t

def footer(canvas, doc):
    canvas.saveState(); canvas.setFont("DV", 7); canvas.setFillColor(INK2)
    canvas.drawString(1.6 * cm, 1.0 * cm, "Semana 8 · GMM, KDE y DBSCAN aplicados a readmisión de pacientes diabéticos")
    canvas.drawRightString(A4[0] - 1.6 * cm, 1.0 * cm, f"Página {doc.page} de 4"); canvas.restoreState()

W = A4[0] - 3.2 * cm
from reportlab.lib.utils import ImageReader
def img(path, width):
    w, h = ImageReader(path).getSize(); return Image(path, width=width, height=width * h / w)
s = []
# ============================================================ PÁGINA 1
s += [P("Perfiles de pacientes diabéticos para un estudio de seguimiento post-alta", h1),
      P("Laboratorio de semana 8 (GMM, KDE y DBSCAN) adaptado al dataset <i>Diabetes 130-US hospitals, 1999–2008</i> · "
        "Análisis a nivel paciente con todo su historial de ingresos · Notebook: <b>semana08_pacientes_agregados.ipynb</b>", sub)]

s += [P("1. Objetivo de negocio", h2),
      P("Las readmisiones hospitalarias en menos de 30 días son costosas para los hospitales y en EE. UU. se penalizan. La gerencia "
        "quiere <b>focalizar un programa de seguimiento después del alta</b> (llamadas, citas tempranas, revisión de medicación) en los "
        "pacientes que más lo necesitan, sin dispersar recursos limitados. La pregunta analítica, adaptada de la guía de semana 8 "
        "(donde un comité buscaba zonas de un mapa), es: <b>¿qué perfiles de pacientes conviene estudiar primero para ese programa, y "
        "cuál requiere revisión caso a caso?</b> Se usan GMM, KDE y DBSCAN como tres fuentes de evidencia; ningún centroide se interpreta "
        "como un “paciente tipo”, y la densidad de pacientes no se confunde con riesgo ni con demanda de recursos.")]

kpis = [("69 987", "pacientes analizados<br/>(99 340 ingresos, ninguno descartado<br/>por ser repetido)"),
        ("3 segmentos", "recurrentes o en transición:<br/>36 % de los pacientes"),
        ("18.8–25.4 %", "readmisión en esos segmentos<br/>frente a 10.4 % de promedio"),
        ("50 % en 4.3 %", "la mitad de los pacientes cabe en<br/>el 4.3 % del plano (cresta)")]
kt = Table([[[P(n, kpi_n), P(t, kpi_t)] for n, t in kpis]], colWidths=[W / 4] * 4)
kt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SOFT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LINEAFTER", (0, 0), (-2, -1), 2, colors.white), ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 7)]))
s += [Spacer(1, 4), kt, Spacer(1, 4)]

s += [P("2. Hallazgos principales", h2),
      B("<b>La recurrencia es lo que más diferencia a los pacientes.</b> Tres de cada cuatro tuvieron un solo ingreso en la base y forman una "
        "“cresta” muy densa; el resto forma un “abanico” disperso de pacientes que vuelven. Los tres métodos coinciden en esta división."),
      B("<b>El riesgo se concentra en quienes vuelven:</b> los segmentos <i>Recurrentes</i> y <i>Muy recurrentes</i> (14 % de los pacientes) "
        "tienen ~25 % de readmisión en su primer ingreso, 2.4 veces el promedio; <i>En transición</i> (22 %) tiene 18.8 %."),
      B("<b>Carga no es riesgo:</b> el segmento <i>Un solo ingreso, complejo</i> (25 %; 5 días, 18 medicamentos, 75 años) consume muchos recursos "
        "por ingreso pero se readmite menos que el promedio (5.5 %)."),
      B("<b>La división cresta / recurrentes es robusta; las 8 componentes no:</b> al remuestrear los datos, K-means (ARI 0.88) y "
        "DBSCAN (0.79) reproducen casi la misma partición, mientras que el GMM de 8 componentes cambia bastante (0.48)."),
      B("<b>Dos advertencias honestas:</b> la readmisión está en parte construida en los ejes (una readmisión es otro ingreso) y los pacientes "
        "más recientes tienen menos tiempo para volver (censura). Por eso las tasas se leen como descripción, no como prueba.")]

s += [P("3. Datos y contrato experimental", h2),
      table([["Decisión", "Acuerdo"],
             ["Unidad de análisis", "Un paciente = una fila que agrega <b>todos</b> sus ingresos válidos. No se duplica a nadie y no se pierde su evolución."],
             ["Limpieza (no recorte)", "Se quitan 3 ingresos con género inválido y 2 423 con alta por fallecimiento u hospicio (sin seguimiento posible). "
              "No se recortan valores extremos: son pacientes reales."],
             ["Variables (10)", "N.º de ingresos; promedios de estancia, análisis, procedimientos, medicamentos y diagnósticos; máximo de consultas, "
              "urgencias y hospitalizaciones previas; edad. <font name='DV'>log(1+x)</font>, estandarizadas y resumidas en 2 componentes "
              "principales (42 % de la varianza), ambas en desviaciones estándar (d.e.)."],
             ["Ejes del plano", "<b>CP1 · carga clínica total</b> (todo sube) y <b>CP2 · recurrencia</b> (más ingresos y visitas previas) frente a "
              "intensidad del ingreso (estancia, medicamentos)."],
             ["Desarrollo / prueba", "Pacientes ordenados por su primer ingreso: primer 70 % para elegir K, h y eps (muestra de 6 000); último 30 % "
              "(20 997) reservado y abierto una sola vez."]],
            [3.2 * cm, W - 3.2 * cm])]
s.append(PageBreak())

# ============================================================ PÁGINA 2
s += [P("4. Evidencia de los tres métodos", h2),
      img("informe/figuras/f1_mapas.png", W),
      P("Figura 1. Los tres métodos sobre los mismos ejes. <b>GMM</b>: 8 componentes gaussianas y sus contornos del 95 %; cuatro elipses alargadas "
        "cubren la cresta y cuatro el abanico. <b>KDE</b>: la mitad de los pacientes cae dentro del contorno negro, que ocupa solo el 4.3 % del área "
        "y está sobre la cresta. <b>DBSCAN</b>: una masa principal (94.7 %), un grupo pequeño de 15 pacientes muy recurrentes y 5.3 % de ruido.", cap),
      table([["Método", "Qué estima", "Parámetro elegido (con desarrollo)", "Evidencia", "Limitación"],
             ["GMM", "Densidad como mezcla de gaussianas y pertenencia de cada paciente", "K = 8, covarianza completa (menor BIC entre 1 y 10)",
              "Separa la cresta de un solo ingreso (56 %) de la transición (22 %) y los recurrentes (15 %)",
              "Necesita 4 elipses para una sola cresta; poco estable al remuestrear (ARI 0.48)"],
             ["KDE", "Superficie de densidad (pacientes por unidad de área)", "Ancho h = 0.2 d.e. (validación temporal en 3 bloques)",
              "Núcleo muy concentrado en la cresta; el abanico es una meseta de baja densidad",
              "No forma grupos; con h = 0.1 se fragmenta en 8 islas, con h = 1.6 es una loma"],
             ["DBSCAN", "Zonas densas conectadas y puntos aislados (ruido)", "eps = 0.3 d.e., mínimo 15 vecinos (curva del 15.º vecino)",
              "El ruido son pacientes muy recurrentes: 71 % volvió y 44 % tuvo alguna readmisión",
              "Un solo eps no sirve para densidades tan distintas; con eps = 0.15 hay 10 grupos"]],
            [1.5 * cm, 3.4 * cm, 3.6 * cm, 4.6 * cm, W - 13.1 * cm], fs=7.2),
      Spacer(1, 5),
      P("<b>Región que KDE suaviza y DBSCAN separa.</b> El borde entre cresta y abanico (CP1 ≈ −1 a 1.5; CP2 ≈ −1.5 a 1) aparece en la KDE como "
        "una caída continua de densidad. DBSCAN con eps = 0.15 la <i>separa</i> (cresta en un grupo, abanico en otro) y con eps = 0.3 la <i>conecta</i>. "
        "Aquí la separación tiene sentido clínico (pacientes que no vuelven frente a los que sí), pero depende de eps: no es una frontera natural."),
      P("<b>Punto ambiguo y punto raro no son lo mismo.</b> El paciente más ambiguo (48 % de pertenencia a una componente y 21 % a otra) es un "
        "ingreso único muy intenso; el de menor densidad es un paciente con 23 ingresos al que el GMM asigna a una sola componente con total "
        "certeza. La pertenencia compara componentes entre sí; la densidad mide qué tan común es el paciente."),
      P("5. Sensibilidad: qué cambia y qué permanece", h2),
      table([["Se varía", "Resultado", "Conclusión"],
             ["GMM: covarianza completa → diagonal", "K por BIC pasa de 8 a 10 (borde de la rejilla)", "El número de componentes no es un número de perfiles reales"],
             ["KDE: h = 0.1 → 0.2 → 1.6 d.e.", "Región del 50 %: 8 islas → 3 regiones → 1 loma", "La cresta densa permanece en los anchos razonables"],
             ["DBSCAN: eps = 0.15 → 0.3 → 0.6 (m = 15)", "10 grupos (81 % cubierto) → 2 (95 %) → 1 (99 %)", "La masa principal permanece; los grupos pequeños no"],
             ["Remuestreo bootstrap (20 repeticiones)", "Estabilidad (ARI): K-means 0.88; DBSCAN 0.79; GMM 0.48",
              "La división cresta / recurrentes permanece; las 8 componentes del GMM no"]],
            [4.6 * cm, 5.9 * cm, W - 10.5 * cm], fs=7.2),
      P("La silhouette se estima sobre una submuestra fija de 1 000 pacientes; con eps = 0.3 no está definida porque el grupo de 15 pacientes casi no "
        "aparece en esa submuestra. Por eso la configuración no se eligió por silhouette, sino por escala (92 % de los pacientes tiene 15 vecinos a menos "
        "de 0.3 d.e.) y por sensibilidad.", cap)]
s.append(PageBreak())

# ============================================================ PÁGINA 3
s += [P("6. Segmentos de pacientes", h2),
      img("informe/figuras/f2_segmentos.png", W * .9),
      P("Figura 2. Readmisión en menos de 30 días medida en el <b>primer</b> ingreso de cada paciente (la medida menos circular disponible) y tamaño "
        "de cada segmento. Se excluye una componente técnica de 17 pacientes (0.3 %) que el GMM usa para ajustar la punta de la cresta.", cap),
      table([["Segmento", "Pacientes (desarr. / prueba)", "Perfil (medianas)", "Readmisión 1.er ingreso (desarr. / prueba)", "Prioridad"],
             ["<b>Muy recurrentes</b>", "3.4 % / 2.1 %", "5 ingresos; 3 hospitalizaciones, 1 urgencia y 1 consulta previas", "25.4 % / 26.7 %", "Revisión caso a caso"],
             ["<b>Recurrentes</b>", "11.1 % / 9.4 %", "3 ingresos; 2 hospitalizaciones previas; 87 % volvió al menos una vez", "25.3 % / 21.7 %", "Alta: estudiar"],
             ["<b>En transición</b>", "21.9 % / 22.5 %", "La mitad ya tuvo un segundo ingreso; 1 hospitalización previa", "18.8 % / 13.5 %", "Alta: estudiar"],
             ["Frontera cresta–abanico", "7.0 % / 6.2 %", "Un ingreso típico; 24 % volvió", "6.9 % / 3.7 %", "Estándar"],
             ["Un solo ingreso, complejo", "25.2 % / 36.0 %", "5 días, 18 medicamentos, 9 diagnósticos, 75 años", "5.5 % / 2.6 %", "Por carga, no por riesgo"],
             ["Un solo ingreso, moderado", "23.2 % / 18.4 %", "3 días, 12 medicamentos, 5 diagnósticos", "2.8 % / 1.9 %", "Estándar"],
             ["Un solo ingreso, breve", "7.8 % / 5.0 %", "2 días, 6 medicamentos, 4 diagnósticos, 55 años", "0.9 % / 0.8 %", "Estándar"]],
            [3.3 * cm, 2.5 * cm, 5.9 * cm, 2.9 * cm, W - 14.6 * cm], fs=7.2),
      Spacer(1, 5),
      P("<b>Lectura del periodo reservado.</b> El orden de riesgo entre segmentos se mantiene en los pacientes nuevos. Los tamaños cambian en la "
        "dirección que predice la censura: los pacientes recientes tuvieron menos tiempo para volver (1.29 ingresos de media frente a 1.48), así que "
        "crece el segmento de un solo ingreso complejo (25 % → 36 %) y la densidad estimada sube de bloque en bloque. No es una mejora del modelo."),
      P("7. Recomendación del comité", h2),
      P("<b>Observo</b> que, con todo el historial, los pacientes se ordenan en una cresta densa de quienes tuvieron un solo ingreso (75 %) y un "
        "abanico de recurrentes, que los tres métodos reconocen. <b>Interpreto</b> que la recurrencia es el eje que más diferencia el riesgo, aunque su "
        "relación con la readmisión es en parte circular y el periodo reservado está censurado. <b>Recomendaría estudiar</b> (A) los "
        "<i>Recurrentes</i> (CP1 ≈ 0.5 a 2.9; CP2 ≈ 0 a 2.9; 11 %) y (B) los pacientes <i>En transición</i> (CP1 ≈ −1.3 a 2.0; CP2 ≈ −1.1 a 1.8; 22 %), "
        "donde un seguimiento puede actuar antes de que el paciente se vuelva recurrente. <b>Vigilaría</b> el extremo CP1 > 2.7, CP2 > 1.4 "
        "(<i>Muy recurrentes</i> y ruido de DBSCAN, ≈ 3–5 %) con revisión caso a caso. <b>No puedo concluir</b> que la recurrencia cause "
        "readmisiones, ni cuántos recursos se necesitan: faltan fechas, costos, capacidad y desenlaces fuera de la red.",
        ParagraphStyle("box", parent=body, backColor=SOFT, borderPadding=6, spaceBefore=4, spaceAfter=8))]
s.append(PageBreak())

# ============================================================ PÁGINA 4
s += [P("8. Recomendaciones operativas", h2),
      table([["Acción", "Para quién", "Por qué"],
             ["Programa de <b>gestión de caso</b>: llamada a las 48–72 h, cita de control en 7 días, conciliación de medicación, plan ante urgencias",
              "Recurrentes y Muy recurrentes (14 %)", "~25 % de readmisión en su primer ingreso, 2.4 veces el promedio; estable en el periodo reservado"],
             ["<b>Intervención preventiva</b> al alta: educación sobre el tratamiento, cita temprana y seguimiento telefónico",
              "En transición (22 %)", "18.8 % de readmisión; es el punto donde todavía se puede evitar que el paciente se vuelva recurrente"],
             ["<b>Revisión clínica caso a caso</b> antes del alta", "Ruido de DBSCAN y extremo del abanico (≈ 3–5 %)",
              "Combinaciones raras de muchos ingresos y urgencias; no encajan en un protocolo de grupo"],
             ["<b>Coordinación de alta y revisión farmacológica</b> (no seguimiento intensivo)", "Un solo ingreso, complejo (25 %)",
              "Alta carga por ingreso (18 medicamentos, 75 años) pero riesgo de readmisión bajo"],
             ["<b>Calcular el segmento en cada alta</b> con el historial disponible y monitorear mensualmente la tasa por segmento",
              "Todos", "El segmento cambia a medida que el paciente vuelve; la asignación debe actualizarse"],
             ["<b>Mejorar los datos</b>: registrar fechas, readmisiones en otras redes, costos y capacidad del programa", "Gerencia y TI",
              "Sin esto no se puede estimar el retorno de la intervención ni corregir la censura"]],
            [6.2 * cm, 3.6 * cm, W - 9.8 * cm], fs=7.3),
      P("9. Limitaciones", h2),
      B("<b>Circularidad:</b> una readmisión registrada es otro ingreso, y el número de ingresos es un eje del plano. La readmisión en algún ingreso "
        "pasa de 4.3 % (1 ingreso) a 71 % (4 o más). Las tasas por segmento describen, no validan; se reporta la del primer ingreso por ser la menos circular."),
      B("<b>Censura:</b> la base no tiene fechas; los pacientes que aparecen tarde tienen menos tiempo para acumular ingresos. Una evaluación justa "
        "exigiría contar solo los ingresos dentro de una ventana fija después del primero."),
      B("<b>Readmisión incompleta:</b> solo se observan reingresos dentro de la red; el 4.3 % de pacientes con un solo ingreso figura como readmitido en otro lugar."),
      B("<b>Grupos poco separados:</b> los pacientes forman un continuo; el GMM de 8 componentes es inestable (ARI 0.48) y sus componentes son "
        "aproximaciones de la densidad, no perfiles clínicos verdaderos. Los segmentos son convenciones útiles para priorizar."),
      B("<b>Representación resumida:</b> el plano de dos componentes explica el 42 % de la variación de las 10 variables; diagnósticos, "
        "medicamentos específicos y destino al alta no entran en el plano."),
      B("<b>Datos antiguos y sin contexto:</b> 1999–2008, 130 hospitales de EE. UU., sin factores sociales, adherencia ni identificación del hospital "
        "(no se puede evaluar la dependencia entre pacientes del mismo centro)."),
      B("<b>Densidad no es demanda:</b> la concentración de pacientes en una zona no indica cuántos recursos necesita; un paciente recurrente consume varios ingresos."),
      P("10. Reproducibilidad", h2),
      P("Todo el análisis está en <b>semana08_pacientes_agregados.ipynb</b> (ejecutado de principio a fin, semilla 42). Las "
        "figuras y cifras de este informe se regeneran con <font name='DV'>python informe/figuras_semana8.py</font> y el PDF con "
        "<font name='DV'>python informe/generar_informe.py</font>, desde la raíz del repositorio. Fuente del dataset: Strack et al. (2014), "
        "<i>BioMed Research International</i>; guía metodológica: <i>semana-08.html</i> y los cuadernos de la semana 8.")]

doc = SimpleDocTemplate("informe/Informe_semana8_diabetes.pdf", pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                        topMargin=1.4 * cm, bottomMargin=1.6 * cm, title="Perfiles de pacientes diabéticos · Semana 8",
                        author="Equipo de minería de datos")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
print("ok")
