import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Importa PhotoImage
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    sender_email = "tu_correo@gmail.com"  # Cambia esto por tu correo de envío
    sender_password = "tu_contraseña"     # Cambia esto por tu contraseña o contraseña de aplicación
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

# Función para regresar a la ventana de registro
def return_to_register():
    menu_frame.pack_forget()  # Ocultar el marco del menú
    register_frame.pack(pady=20)  # Mostrar el marco de registro

# Crear la ventana principal
root = tk.Tk()
root.title("SOLUCIONES TECNOLOGICAS Cyber-MAS")
root.geometry("800x800")

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

# Marco de menú
menu_frame = tk.Frame(root)
tk.Label(menu_frame, text="OPCIONES DE SERVICIOS TECNOLOGICOS").pack(pady=10)

# Botón para regresar a la ventana de registro
tk.Button(menu_frame, text="Regresar a Registro", command=return_to_register, bg="#FF5722", fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)

# Ejecuta la aplicación
root.mainloop()
