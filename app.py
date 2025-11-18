import streamlit as st
from PIL import Image
import io

TARGET_WIDTH = 1500
TARGET_HEIGHT = 850

st.title("Logo Resizer (1500 × 850, transparent)")
st.write("Upload ein Logo, es wird auf volle Breite skaliert und vertikal zentriert.")

uploaded_file = st.file_uploader("Logo hochladen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Logo laden
    logo = Image.open(uploaded_file).convert("RGBA")
    orig_width, orig_height = logo.size

    # Skalierung auf volle Breite
    new_width = TARGET_WIDTH
    new_height = int(orig_height * (TARGET_WIDTH / orig_width))
    logo_resized = logo.resize((new_width, new_height), Image.LANCZOS)

    # Neues Canvas mit transparentem Hintergrund
    canvas = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))

    # Vertikale Einmittung
    offset_y = (TARGET_HEIGHT - new_height) // 2
    canvas.paste(logo_resized, (0, offset_y), logo_resized)

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