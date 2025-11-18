import streamlit as st
from PIL import Image
import io

# Zielgröße
TARGET_WIDTH = 1500
TARGET_HEIGHT = 850

st.title("Logo Resizer (1500 × 850, transparent)")
st.write("Upload ein Logo, es wird proportional skaliert und zentriert, ohne Überlauf.")

uploaded_file = st.file_uploader("Logo hochladen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("Logo wird verarbeitet..."):
        # Logo laden und in RGBA konvertieren
        logo = Image.open(uploaded_file).convert("RGBA")
        orig_width, orig_height = logo.size

        # Skalierung berechnen (zuerst auf Breite)
        scale_factor = TARGET_WIDTH / orig_width
        new_width = TARGET_WIDTH
        new_height = int(orig_height * scale_factor)

        # Wenn Höhe zu groß ist, auf Höhe begrenzen
        if new_height > TARGET_HEIGHT:
            scale_factor = TARGET_HEIGHT / orig_height
            new_height = TARGET_HEIGHT
            new_width = int(orig_width * scale_factor)

        # Logo skalieren
        logo_resized = logo.resize((new_width, new_height), Image.LANCZOS)

        # Neues Canvas mit transparentem Hintergrund
        canvas = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))

        # Zentrierung berechnen
        offset_x = (TARGET_WIDTH - new_width) // 2
        offset_y = (TARGET_HEIGHT - new_height) // 2

        # Logo einfügen (weißer Hintergrund bleibt erhalten)
        canvas.paste(logo_resized, (offset_x, offset_y), logo_resized)

        # Vorschau anzeigen
        st.image(canvas, caption="Verarbeitetes Logo", use_container_width=True)

        # Download-Button
        img_bytes = io.BytesIO()
        canvas.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        st.download_button(
            label="Download PNG",
            data=img_bytes,
            file_name="logo_resized.png",
            mime="image/png"
        )