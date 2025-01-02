import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para mostrar los detalles del servicio
def show_service_details(service_name):
    # Crear una ventana nueva para mostrar los detalles
    details_window = tk.Toplevel(root)
    details_window.title(f"Detalles del Servicio: {service_name}")
    
    # Mostrar imagen del servicio
    img_path = ""
    if service_name == "INSTALACION SERVIDOR INFORMATICO":
        img_path = "servidor_detalle.png"  # Imagen más grande del servicio
        description = "Este servicio incluye la instalación y configuración de un servidor informático robusto para su empresa o hogar."
    elif service_name == "INSTALACION CAMARAS DE SEGURIDAD":
        img_path = "camara_detalle.png"
        description = "Instalamos cámaras de seguridad de alta calidad para proteger su hogar o negocio."
    
    img = Image.open(img_path)
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)
    
    tk.Label(details_window, text=service_name, font=("Helvetica", 16), fg="blue").pack(pady=10)
    tk.Label(details_window, image=img).pack(pady=10)
    
    # Mostrar la descripción
    tk.Label(details_window, text=description, font=("Helvetica", 12)).pack(pady=10)
    
    # Crear un gráfico adicional si el servicio lo requiere (Ejemplo con Matplotlib)
    if service_name == "INSTALACION SERVIDOR INFORMATICO":
        # Crear una figura con matplotlib
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot([0, 1, 2], [0, 1, 4], label="Rendimiento Servidor")
        ax.set_title("Gráfica de Rendimiento")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Rendimiento")
        ax.legend()
        
        # Convertir la figura en un canvas de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=details_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
    
    # Botón de cierre
    tk.Button(details_window, text="Cerrar", command=details_window.destroy).pack(pady=10)

# Marco de menú
root = tk.Tk()

menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

# Título de la sección
tk.Label(menu_frame, text="SELECCIONA SERVICIO TECNICO QUE REQUIERAS", font=("Helvetica", 15), fg="red").pack(pady=10)

root.iconbitmap('cybermas.ico')

# Cargar las imágenes de los servicios
img_service_1 = Image.open("servidor.png")
img_service_1 = img_service_1.resize((50, 50))
img_service_1 = ImageTk.PhotoImage(img_service_1)

img_service_2 = Image.open("camara.png")
img_service_2 = img_service_2.resize((50, 50))
img_service_2 = ImageTk.PhotoImage(img_service_2)

# Función para asignar el clic a las imágenes
def on_click_service(service_name):
    show_service_details(service_name)

# Inserta los servicios con imágenes y eventos de clic
label_1 = tk.Label(menu_frame, text="1. INSTALACION SERVIDOR INFORMATICO")
label_1.pack(anchor='w')
label_1.bind("<Button-1>", lambda e: on_click_service("INSTALACION SERVIDOR INFORMATICO"))
tk.Label(menu_frame, image=img_service_1).pack()

label_2 = tk.Label(menu_frame, text="2. INSTALACION CAMARAS DE SEGURIDAD")
label_2.pack(anchor='w')
label_2.bind("<Button-1>", lambda e: on_click_service("INSTALACION CAMARAS DE SEGURIDAD"))
tk.Label(menu_frame, image=img_service_2).pack()

root.mainloop()
