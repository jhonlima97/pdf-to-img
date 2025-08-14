import json

def extract_lambayeque_ubigeos(input_file, output_file):
    """
    This function reads a JSON file containing Peruvian ubigeo data,
    filters for entries belonging to the Lambayeque department, and
    saves the results to a new JSON file.

    Parameters:
    input_file (str): The name of the input JSON file.
    output_file (str): The name of the output JSON file.
    """
    # El prefijo ubigeo para el departamento de Lambayeque es '14'
    lambayeque_ubigeo_prefix = '14'
    
    lambayeque_data = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Aseguramos que la data esté en la clave 'igt_distrital'
            if "igt_distrital" in data:
                all_ubigeos = data["igt_distrital"]
                
                # Iteramos sobre cada entrada y verificamos el campo 'iddist'
                for entry in all_ubigeos:
                    # Obtenemos el valor de 'iddist' de manera segura
                    iddist = str(entry.get("iddist", ""))
                    
                    # Filtramos las entradas cuyo 'iddist' comience con el prefijo de Lambayeque
                    if iddist.startswith(lambayeque_ubigeo_prefix):
                        lambayeque_data.append(entry)
            else:
                print(f"Error: No se encontró la clave 'igt_distrital' en {input_file}.")
                return

        if not lambayeque_data:
            print("No se encontraron ubigeos de Lambayeque en el archivo de entrada.")
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            output_json = {"igt_lambayeque_distrital": lambayeque_data}
            json.dump(output_json, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Extracción exitosa: Se encontraron {len(lambayeque_data)} distritos de Lambayeque")

    except FileNotFoundError:
        print(f"❌ Error: El archivo '{input_file}' no fue encontrado.")
    except json.JSONDecodeError:
        print(f"❌ Error: No se pudo decodificar el JSON de '{input_file}'. Por favor, revise el formato del archivo.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

# --- Ejecución del script ---
input_json_file = "public/archivos/igt_distrital_nacional.json"
output_json_file = "public/archivos/igt_lambayeque_distrital.json"

extract_lambayeque_ubigeos(input_json_file, output_json_file)