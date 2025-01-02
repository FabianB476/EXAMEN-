import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Importa PhotoImage
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image,ImageTk
from tkinter import font


# Crear la base de datos si no existe
def create_db():
    conn = sqlite3.connect('users.db')  # Conectar a la base de datos (la crea si no existe)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    address TEXT,
                    password TEXT,
                    email TEXT)''')
    conn.commit()
    conn.close()

# Función para enviar el código de recuperación al correo del usuario
def send_recovery_email(user_email, recovery_code):
    sender_email = "fabian19800610@gmail.com"  # Cambia esto por tu correo de envío
    sender_password = "dsxx rzkk sddj lnoo"     # Cambia esto por tu contraseña o contraseña de aplicación generada en la API
    subject = "Código de Recuperación de Contraseña"
    body = f"Tu código de recuperación es: {recovery_code}"

    # Configuración del servidor SMTP (en este caso, Gmail)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Correo Enviado", f"Se ha enviado un código de recuperación a {user_email}.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al enviar el correo: {e}")

# Función para generar un código de recuperación aleatorio
def generate_recovery_code():
    return random.randint(100000, 999999)

# Función para la recuperación de contraseña
def recover_password():
    email = entry_email.get()  # Usamos el correo electrónico para la recuperación

    if email:
        # Verificar si el correo electrónico existe en la base de datos
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''SELECT password FROM users WHERE email = ?''', (email,))
        result = c.fetchone()
        conn.close()

        if result:
            # Generar un código de recuperación
            recovery_code = generate_recovery_code()

            # Enviar el correo con el código de recuperación
            send_recovery_email(email, recovery_code)
            messagebox.showinfo("Recuperación de Contraseña", f"Se ha enviado un código de recuperación a {email}.")
        else:
            messagebox.showerror("Error", "El correo electrónico no está registrado.")
    else:
        messagebox.showerror("Error", "Por favor, ingresa tu correo electrónico.")

# Función para registrar usuario
def register_user():
    user_id = entry_id.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    address = entry_address.get()
    password = entry_password.get()
    email = entry_email.get()  # Obtener el correo electrónico

    if not user_id or not first_name or not last_name or not address or not password or not email:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
    else:
        # Insertar datos en la base de datos
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (user_id, first_name, last_name, address, password, email)
                     VALUES (?, ?, ?, ?, ?, ?)''', (user_id, first_name, last_name, address, password, email))
        conn.commit()
        conn.close()

        messagebox.showinfo("Registro exitoso", "Registro completado correctamente.")
        show_menu()

# Función para mostrar el menú después del registro
def show_menu():
    register_frame.pack_forget()  # Oculta el marco de registro
    menu_frame.pack(pady=20)      # Muestra el marco del menú

# Función para borrar los campos de entrada
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Función para ingresar (autenticación)
def authenticate_user():
    # Crear una nueva ventana para que el usuario ingrese su ID y contraseña
    auth_window = tk.Toplevel(root)
    auth_window.title("Ingreso de Usuario")
    auth_window.iconbitmap('cybermas.ico')
    auth_window.geometry("500x500")

    # Etiquetas y campos de entrada para ID y contraseña
    tk.Label(auth_window, text="Número de ID:").pack(pady=10)
    entry_auth_id = tk.Entry(auth_window)
    entry_auth_id.pack(pady=5)

    tk.Label(auth_window, text="Contraseña:").pack(pady=10)
    entry_auth_password = tk.Entry(auth_window, show='*')
    entry_auth_password.pack(pady=5)

    # Función para verificar la autenticación
    def check_authentication():
        user_id = entry_auth_id.get()
        password = entry_auth_password.get()

        if user_id and password:
            # Verificar si los datos de usuario coinciden con la base de datos
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM users WHERE user_id = ? AND password = ?''', (user_id, password))
            result = c.fetchone()
            conn.close()

            if result:
                messagebox.showinfo("Ingreso Exitoso", "Has ingresado correctamente.")
                auth_window.destroy()  # Cierra la ventana de autenticación
                show_menu()  # Muestra el marco de menú
            else:
                messagebox.showerror("Error", "ID o contraseña incorrectos.")
        else:
            messagebox.showerror("Error", "Por favor, ingresa tu ID y contraseña.")

    # Botón para verificar la autenticación
    tk.Button(auth_window, text="Ingresar", command=check_authentication, bg="#4CAF50", fg="white").pack(pady=20)

# Crear la ventana principal
root = tk.Tk()
root.title("Bienvenidos  a Cyber-MAS")
root.iconbitmap('cybermas.ico')
root.geometry("800x800")
# Establecer una fuente personalizada
custom_font = ("Helvetica", 50, "bold")  # Tipo de letra Arial, tamaño 20, negrita


# Etiqueta de título con fuente personalizada


# Cargar la imagen de fondo
bg_image = Image.open("cybermas.jpg")  # Reemplaza con la ruta de tu imagen
bg_image = bg_image.resize((800, 800))  # Redimensiona la imagen al tamaño de la ventana
bg_image = ImageTk.PhotoImage(bg_image)

# Crear un label con la imagen de fondo
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Hace que la imagen ocupe toda la ventana

# Aquí puedes agregar otros widgets sobre la imagen de fondo
# Ejemplo: campos de texto y botones para el registro

# Frame para el formulario de registro
register_frame = tk.Frame(root, bg="white", padx=20, pady=20)  # Fondo blanco y margen
register_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrado en la ventana



# Crear la base de datos al iniciar la aplicación
create_db()

# Marco de registro
register_frame = tk.Frame(root)
register_frame.pack(pady=20)

# Etiquetas y entradas para el registro
tk.Label(register_frame, text="Número de ID:").grid(row=0, column=0, padx=10, pady=5)
entry_id = tk.Entry(register_frame)
entry_id.grid(row=0, column=1)

tk.Label(register_frame, text="Nombres:").grid(row=1, column=0, padx=10, pady=5)
entry_first_name = tk.Entry(register_frame)
entry_first_name.grid(row=1, column=1)

tk.Label(register_frame, text="Apellidos:").grid(row=2, column=0, padx=10, pady=5)
entry_last_name = tk.Entry(register_frame)
entry_last_name.grid(row=2, column=1)

tk.Label(register_frame, text="Dirección:").grid(row=3, column=0, padx=10, pady=5)
entry_address = tk.Entry(register_frame)
entry_address.grid(row=3, column=1)

tk.Label(register_frame, text="Contraseña:").grid(row=4, column=0, padx=10, pady=5)
entry_password = tk.Entry(register_frame, show='*')
entry_password.grid(row=4, column=1)

tk.Label(register_frame, text="Correo Electrónico:").grid(row=5, column=0, padx=10, pady=5)
entry_email = tk.Entry(register_frame)  # Nueva entrada para correo
entry_email.grid(row=5, column=1)

# Botones para registrar, borrar y recuperar contraseña
tk.Button(register_frame, text="Registrarse", command=register_user, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold")).grid(row=6, column=0, padx=10, pady=10)
tk.Button(register_frame, text="Borrar", command=clear_fields, bg="#F44336", fg="white", font=("Helvetica", 12, "bold")).grid(row=6, column=1, padx=10, pady=10)
tk.Button(register_frame, text="Recuperar Contraseña", command=recover_password, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold")).grid(row=6, column=2, padx=10, pady=10)

# Botón para ingresar en la parte superior derecha de la ventana principal
login_button = tk.Button(root, text="Ingresar.....", command=authenticate_user, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))

login_button.place(x=680, y=10)  # Colocamos el botón en la parte superior derecha

#################
# Función para regresar al formulario de registro
def show_register_window():
    menu_frame.pack_forget()  # Oculta el marco de menú
    register_frame.pack(pady=20)  # Muestra el marco de registro

###### Marco de menú

import tkinter as tk
from PIL import Image, ImageTk

# Crear una ventana con detalles del servicio
def show_service_details(service_name):
    # Crear una nueva ventana para mostrar los detalles
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Detalles del Servicio: {service_name}")
    root.iconbitmap('cybermas.ico')
    detail_window.geometry("500x500")

    # Aquí agregarás la descripción del servicio
    if service_name == "INSTALACION SERVIDOR INFORMATICO":
        description = "Un servidor Informatico es un sistema que le proporciona recursos,datos, servicios o programas a otros ordenadores, conocidos como clientes, a través de una red." "En teoría, se consideran servidores aquellos ordenadores que comparten recursos con máquinas cliente."
    elif service_name == "INSTALACION CAMARAS DE SEGURIDAD":
        description = " !  SIENTASE SEGURO SU TRANQUILIDAD NO TIENE PRECIO   ! ."
    elif service_name == "INSTALACION ALARMAS DE SEGURIDAD":
        description = " Proteja y monitoree su hogar  o negocio desde su celular instale sitema de seguridad electrónica con CyberMAS ."
    elif service_name == "INSTALACIONES ELECTRICAS":
        description = "Proporcionar energía eléctrica a edificios, oficinas, infraestructuras, lugares públicos, entre otros."
    elif service_name == " HERRAMIENTAS":
        description = " Suministro de   herramientas tecnológicas  para tu proyecto estructural fisico "
    elif service_name == "PROYECTOS DESARROLLO DE SOFTWARE":
        description = "Implementacion software  DE  acuerdo a tus  nesecidades para tu  emprendimiento o negocio ."
    else:
        description = "Información no disponible."

    # Mostrar la descripción en la ventana de detalles
    label = tk.Label(detail_window, text=description, font=("Helvetica", 12), wraplength=350)
    label.pack(pady=20)

# ## Marco de menú
menu_frame = tk.Frame(root)
#menu_frame.pack(pady=20)

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

# Mostrar las imágenes en el menú
tk.Label(menu_frame, image=img_service_1).pack()
tk.Label(menu_frame, image=img_service_2).pack()


# Detalles de los otros servicios con imágenes y eventos de clic
img_service_3 = Image.open("alarma.png")
img_service_3 = img_service_3.resize((50, 50))
img_service_3 = ImageTk.PhotoImage(img_service_3)

img_service_4 = Image.open("electri.png")
img_service_4 = img_service_4.resize((50, 50))
img_service_4 = ImageTk.PhotoImage(img_service_4)

# Inserta las imágenes y eventos de clic
label_3 = tk.Label(menu_frame, text="3.- INSTALACION ALARMAS DE SEGURIDAD")
label_3.pack(anchor='w')
label_3.bind("<Button-1>", lambda e: on_click_service("INSTALACION ALARMAS DE SEGURIDAD"))
tk.Label(menu_frame, image=img_service_3).pack()

label_4 = tk.Label(menu_frame, text="4.- INSTALACIONES ELECTRICAS")
label_4.pack(anchor='w')
label_4.bind("<Button-1>", lambda e: on_click_service("INSTALACIONES ELECTRICAS"))
tk.Label(menu_frame, image=img_service_4).pack()


# Continuar con los demás servicios como en el ejemplo anterior...

img_service_5 = Image.open("herramientas.png")
img_service_5 = img_service_5.resize((50, 50))
img_service_5 = ImageTk.PhotoImage(img_service_5)

img_service_6 = Image.open("software.png")
img_service_6 = img_service_6.resize((50, 50))
img_service_6 = ImageTk.PhotoImage(img_service_6)

label_5 = tk.Label(menu_frame, text="5.- HERRAMIENTAS")
label_5.pack(anchor='w')
label_5.bind("<Button-1>", lambda e: on_click_service("  HERRAMIENTAS"))
tk.Label(menu_frame, image=img_service_5).pack()

label_6 = tk.Label(menu_frame, text="6.- PROYECTOS DESARROLLO DE SOFTWARE")
label_6.pack(anchor='w')
label_6.bind("<Button-1>", lambda e: on_click_service("PROYECTOS DESARROLLO DE SOFTWARE"))
tk.Label(menu_frame, image=img_service_6).pack()

# Agregar el botón para regresar a la ventana de registro
tk.Button(menu_frame, text="Regresar al Registro", command=show_register_window, bg="#FF5722", fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)

# Botón de salir
exit_button = tk.Button(register_frame, text="Salir", command=root.quit, bg="#F44336", fg="white", font=("Helvetica", 12, "bold"))
exit_button.grid(row=6, column=3, padx=10, pady=10)

# Ejecuta la aplicación
root.mainloop()