from server.generators.image_generator import ImageGenerator

def generate_image_file(prompt: str, output_path: str = "output.png"):
    gen = ImageGenerator()
    img_data = gen.generate_image(prompt)
    if img_data:
        with open(output_path, "wb") as f:
            f.write(img_data)
        print(f"Imagen guardada en: {output_path}")
    else:
        print("No se generó imagen")
