from pdf2image import convert_from_path
import os

# --- CONFIGURACIÓN ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_SOURCE_DIR = os.path.join(SCRIPT_DIR, 'public', 'archivos', 'docs_normatividad')
THUMBNAIL_OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'public', 'img', 'normatividadmin')

IMAGE_FORMAT = 'jpeg'  # 'png' o 'jpeg'
IMAGE_QUALITY = 80    # Quality img(0-100), solo para JPEG
IMAGE_DPI = 100
# ---------------------------------------------------------------------------------------

POPPLER_PATH = r'C:\tools\poppler-24.08.0\Library\bin'

def generate_miniatura():
    print("Iniciando generación de miniaturas con pdf2image...")

    if not os.path.exists(THUMBNAIL_OUTPUT_DIR):
        os.makedirs(THUMBNAIL_OUTPUT_DIR)

    pdf_files = [f for f in os.listdir(PDF_SOURCE_DIR) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"No se encontraron archivos PDF en la ruta especificada: {PDF_SOURCE_DIR}")
        return

    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(PDF_SOURCE_DIR, pdf_file)
        base_name = os.path.splitext(pdf_file)[0] # Nombre del archivo sin extensión
        thumbnail_output_path = os.path.join(THUMBNAIL_OUTPUT_DIR, base_name) # pdf2image añade la extensión

        try:
            # Convertir solo la primera página (first_page=1, last_page=1)
            images = convert_from_path(
                pdf_file_path,
                first_page=1,
                last_page=1,
                dpi=IMAGE_DPI, 
                fmt=IMAGE_FORMAT,
                jpegopt={"quality": IMAGE_QUALITY} if IMAGE_FORMAT == 'jpeg' else {},
                poppler_path=POPPLER_PATH
            )

            if images:
                # Guardar la primera (y única) imagen generada
                image_path = f"{thumbnail_output_path}.{IMAGE_FORMAT}"
                images[0].save(image_path)
                print(f"Miniatura generada para: {pdf_file} -> {image_path}")
            else:
                print(f"No se pudo generar miniatura para: {pdf_file}")

        except Exception as e:
            print(f"Error al generar miniatura para {pdf_file}: {e}")
            print("Asegúrate de que Poppler esté correctamente instalado y en el PATH.")

if __name__ == "__main__":
    generate_miniatura()