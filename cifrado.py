# Cargar las librerias
import tkinter as tk
from tkinter import messagebox

# Función para cifrar el número
def cifrar(numero):
    if not numero.isdigit() or len(numero) != 6:
        return None, 'Ingrese un número de 6 dígitos.'
    cifras = [(int(d) + 7) % 10 for d in numero]
    cifras[0], cifras[2] = cifras[2], cifras[0]
    cifras[1], cifras[3] = cifras[3], cifras[1]
    cifras[4], cifras[5] = cifras[5], cifras[4]
    return ''.join(map(str, cifras)), None

# Función para descifrar el número
def descifrar(numero):
    if not numero.isdigit() or len(numero) != 6:
        return None, 'Ingrese un número cifrado de 6 dígitos.'
    cifras = [int(d) for d in numero]
    cifras[0], cifras[2] = cifras[2], cifras[0]
    cifras[1], cifras[3] = cifras[3], cifras[1]
    cifras[4], cifras[5] = cifras[5], cifras[4]
    descifrado = [(d - 7 + 10) % 10 for d in cifras]
    return ''.join(map(str, descifrado)), None

# Validar mientras el usuario escribe (permite borrar)
def solo_seis_digitos(valor):
    return valor == '' or (valor.isdigit() and len(valor) <= 6)

# Clase principal de la app
class App:
    def __init__(self, root):
        self.root = root
        root.title('🔐 Aplicación de Cifrado de Datos')
        root.geometry('400x200')
        root.resizable(False, False)

        tk.Label(
            root,
            text='Desarrollado por: Mario Esteban Vargas Pisco',
            font=('Arial', 10)
        ).pack(pady=10)

        tk.Button(
            root, text='🔏 Cifrar número',
            command=self.ventana_cifrado,
            width=20
        ).pack(pady=5)

        tk.Button(
            root, text='🔓 Descifrar número',
            command=self.ventana_descifrado,
            width=20
        ).pack(pady=5)

        tk.Label(
            root, text='Versión V.1',
            font=('Arial', 8, 'italic')
        ).pack(pady=10)
   # Ventana de cifrado
    def ventana_cifrado(self):
        v = tk.Toplevel()
        v.title('🔏 Cifrado')
        v.geometry('300x180')
    # Entrada de número
        tk.Label(
            v, text='Ingresa un número de 6 dígitos:',
            font=('Arial', 10)
        ).pack(pady=10)
     # Validación en tiempo real
        vcmd = v.register(solo_seis_digitos)
        entrada = tk.Entry(
            v, justify='center', font=('Arial', 12),
            validate='key', validatecommand=(vcmd, '%P')
        )
        entrada.pack()
     # Resultado visual
        resultado = tk.Label(
            v, text='', font=('Arial', 12, 'bold'), fg='blue'
        )
        resultado.pack(pady=10)
    # Botón de acción
        def cifrar_y_mostrar():
            salida, error = cifrar(entrada.get())
            if error:
                messagebox.showerror('Error', error)
            else:
                resultado.config(text=f'Cifrado: {salida}')

        tk.Button(v, text='Cifrar', command=cifrar_y_mostrar).pack()
     # Ventana de descifrado
    def ventana_descifrado(self):
        v = tk.Toplevel()
        v.title('🔓 Descifrado')
        v.geometry('300x180')
    # Entrada
        tk.Label(
            v, text='Ingresa número cifrado (6 dígitos):',
            font=('Arial', 10)
        ).pack(pady=10)
     # Validación en tiempo real
        vcmd = v.register(solo_seis_digitos)
        entrada = tk.Entry(
            v, justify='center', font=('Arial', 12),
            validate='key', validatecommand=(vcmd, '%P')
        )
        entrada.pack()

        resultado = tk.Label(
            v, text='', font=('Arial', 12, 'bold'), fg='green'
        )
        resultado.pack(pady=10)
    # Acción de descifrar
        def descifrar_y_mostrar():
            salida, error = descifrar(entrada.get())
            if error:
                messagebox.showerror('Error', error)
            else:
                resultado.config(text=f'Original: {salida}')

        tk.Button(v, text='Descifrar', command=descifrar_y_mostrar).pack()

# Ejecutar aplicación
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()