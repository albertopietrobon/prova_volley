import streamlit as st
from streamlit_drawable_canvas import st_drawable_canvas
import numpy as np
from PIL import Image, ImageDraw

# --- Configurazione Iniziale ---
st.title("Campo da Pallavolo Interattivo")

# Dimensioni del campo da pallavolo (proporzioni standard)
FIELD_WIDTH = 900
FIELD_HEIGHT = 1800

# Colori
FIELD_COLOR = "#8FBC8F"  # Verde scuro (DarkSeaGreen)
LINE_COLOR = "white"
SECTOR_LINE_COLOR = "lightgray"
POINT_COLOR = "red"

# Spessore delle linee
LINE_THICKNESS = 5
SECTOR_LINE_THICKNESS = 2

# Numero di settori per lato (es. 3x3 per metà campo)
NUM_ATTACK_SECTORS_X = 3
NUM_ATTACK_SECTORS_Y = 3
NUM_DEFENSE_SECTORS_X = 3
NUM_DEFENSE_SECTORS_Y = 6  # Più settori nella zona di difesa

# Calcolo delle dimensioni dei settori
attack_sector_width = FIELD_WIDTH / NUM_ATTACK_SECTORS_X
attack_sector_height = (FIELD_HEIGHT / 2) / NUM_ATTACK_SECTORS_Y
defense_sector_width = FIELD_WIDTH / NUM_DEFENSE_SECTORS_X
defense_sector_height = (FIELD_HEIGHT / 2) / NUM_DEFENSE_SECTORS_Y

# --- Funzioni Utili ---
def draw_field(width, height):
    """Disegna il campo da pallavolo."""
    image = Image.new("RGB", (width, height), FIELD_COLOR)
    draw = ImageDraw.Draw(image)

    # Linea centrale
    draw.line([(0, height / 2), (width, height / 2)], fill=LINE_COLOR, width=LINE_THICKNESS)

    # Linee laterali e di fondo
    draw.rectangle([(0, 0), (width, height)], outline=LINE_COLOR, width=LINE_THICKNESS)

    # Linea dei 3 metri (zona d'attacco)
    draw.line([(0, height / 2 - 300), (width, height / 2 - 300)], fill=LINE_COLOR, width=LINE_THICKNESS)
    draw.line([(0, height / 2 + 300), (width, height / 2 + 300)], fill=LINE_COLOR, width=LINE_THICKNESS)

    return image, draw

def draw_attack_sectors(draw, num_x, num_y, sector_width, sector_height):
    """Disegna le linee dei settori nella metà campo d'attacco."""
    start_y = 0
    for i in range(1, num_y):
        y = int(start_y + i * sector_height)
        draw.line([(0, y), (FIELD_WIDTH, y)], fill=SECTOR_LINE_COLOR, width=SECTOR_LINE_THICKNESS)
    for i in range(1, num_x):
        x = int(i * sector_width)
        draw.line([(x, start_y), (x, FIELD_HEIGHT / 2)], fill=SECTOR_LINE_COLOR, width=SECTOR_LINE_THICKNESS)

def draw_defense_sectors(draw, num_x, num_y, sector_width, sector_height):
    """Disegna le linee dei settori nella metà campo di difesa."""
    start_y = FIELD_HEIGHT / 2
    for i in range(1, num_y):
        y = int(start_y + i * sector_height)
        draw.line([(0, y), (FIELD_WIDTH, y)], fill=SECTOR_LINE_COLOR, width=SECTOR_LINE_THICKNESS)
    for i in range(1, num_x):
        x = int(i * sector_width)
        draw.line([(x, start_y), (x, FIELD_HEIGHT)], fill=SECTOR_LINE_COLOR, width=SECTOR_LINE_THICKNESS)

# --- Interfaccia Utente ---
st.sidebar.header("Selezione Attacco e Difesa")

# Seleziona la zona di attacco
attack_zone_col1, attack_zone_col2 = st.sidebar.columns(2)
attack_x = attack_zone_col1.selectbox("Attacco X", list(range(1, NUM_ATTACK_SECTORS_X + 1)))
attack_y = attack_zone_col2.selectbox("Attacco Y", list(range(1, NUM_ATTACK_SECTORS_Y + 1)))
attack_label = f"({attack_x}, {attack_y})"

# Seleziona la zona di caduta
defense_zone_col1, defense_zone_col2 = st.sidebar.columns(2)
defense_x = defense_zone_col1.selectbox("Difesa X", list(range(1, NUM_DEFENSE_SECTORS_X + 1)))
defense_y = defense_zone_col2.selectbox("Difesa Y", list(range(1, NUM_DEFENSE_SECTORS_Y + 1)))
defense_label = f"({defense_x}, {defense_y})"

# Bottone per registrare il punto
if st.sidebar.button("Registra Punto"):
    st.sidebar.success(f"Attacco da: Zona {attack_label}, Caduta in: Zona {defense_label}")

# --- Visualizzazione del Campo ---
st.subheader("Visualizzazione del Campo")

# Disegna il campo base
field_image, draw = draw_field(FIELD_WIDTH, FIELD_HEIGHT)

# Disegna le griglie dei settori
draw_attack_sectors(draw, NUM_ATTACK_SECTORS_X, NUM_ATTACK_SECTORS_Y, attack_sector_width, attack_sector_height)
draw_defense_sectors(draw, NUM_DEFENSE_SECTORS_X, NUM_DEFENSE_SECTORS_Y, defense_sector_width, defense_sector_height)

st.image(field_image, caption="Campo da Pallavolo con Settori", use_column_width=True)

# --- Possibilità di Disegno (Opzionale) ---
st.subheader("Disegno sul Campo (Opzionale)")
canvas_result = st_drawable_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Arancione semitrasparente
    stroke_width=5,
    stroke_color="red",
    background_color=FIELD_COLOR,
    background_image=field_image,
    height=FIELD_HEIGHT // 3,  # Riduci l'altezza per non occupare troppo spazio
    width=FIELD_WIDTH // 3,
    drawing_mode="freedraw",
    key="drawable_canvas"
)

if canvas_result.json_data is not None:
    st.subheader("Dati del Disegno (JSON)")
    st.json(canvas_result.json_data)
