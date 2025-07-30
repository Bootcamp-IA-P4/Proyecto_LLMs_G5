
from PIL import Image
import os

def resize_image_to_width(input_path: str, output_path: str, target_width: int):
    """
    Redimensiona una imagen a un ancho específico manteniendo la proporción.

    Args:
        input_path (str): Ruta de la imagen original.
        output_path (str): Ruta donde se guardará la imagen redimensionada.
        target_width (int): El ancho deseado en píxeles.
    """
    try:
        image = Image.open(input_path)
        original_width, original_height = image.size

        # Si la imagen ya tiene el ancho deseado, no hacemos nada (o la copiamos)
        if original_width == target_width:
            # image.save(output_path) # Descomentar si quieres una copia exacta
            return input_path

        # Calcular el nuevo alto para mantener la proporción
        aspect_ratio = original_height / original_width
        target_height = int(target_width * aspect_ratio)

        # Redimensionar con un filtro de alta calidad (LANCZOS)
        resized_image = image.resize((target_width, target_height), Image.LANCZOS)

        # Guardar la nueva imagen
        resized_image.save(output_path)
        
        print(f"Imagen redimensionada y guardada en: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error al redimensionar la imagen {input_path}: {e}")
        return None
