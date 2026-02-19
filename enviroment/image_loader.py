"""
Utilidades de carga de imágenes para representación de laberintos
"""
import numpy as np
from PIL import Image


class ImageLoader:
    """Maneja la carga y procesamiento de imágenes de laberintos"""
    
    @staticmethod
    def load_image(image_path):
        """
        Cargar una imagen desde ruta de archivo
        
        Args:
            image_path: Ruta al archivo de imagen (.png o .bmp)
            
        Returns:
            array numpy de forma (altura, ancho, 3) con valores RGB
        """
        try:
            image = Image.open(image_path)
            # Convertir a modo RGB si no lo está
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # Convertir a array numpy
            img_array = np.array(image)
            return img_array
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")
    
    @staticmethod
    def save_image(img_array, output_path):
        """
        Guardar un array numpy como imagen
        
        Args:
            img_array: array numpy de forma (altura, ancho, 3)
            output_path: Ruta para guardar la imagen
        """
        try:
            image = Image.fromarray(img_array.astype('uint8'))
            image.save(output_path)
        except Exception as e:
            raise ValueError(f"Error saving image: {e}")
    
    @staticmethod
    def get_dimensions(img_array):
        """
        Obtener dimensiones de la imagen
        
        Args:
            img_array: array numpy representando la imagen
            
        Returns:
            tupla (altura, ancho)
        """
        return img_array.shape[0], img_array.shape[1]
