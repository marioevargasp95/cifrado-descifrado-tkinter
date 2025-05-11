# 🔐 Aplicación de Cifrado y Descifrado de Datos

Esta aplicación de escritorio fue desarrollada en Python utilizando Tkinter. Permite cifrar y descifrar números de 6 dígitos usando una transformación básica con operaciones matemáticas y reordenamiento de dígitos.

---

## 📌 Objetivo

Crear una interfaz gráfica amigable que:
- Permita ingresar un número de 6 dígitos.
- Cifre el número sumando 7 a cada dígito y aplicando módulo 10.
- Reordene los dígitos según una lógica específica.
- Permita revertir el proceso para obtener el número original.

---

## 🛠️ Tecnologías utilizadas

- Python 3.12
- Tkinter (para la GUI)
- PyInstaller (opcional, para convertir en .exe)

---

## 📷 Capturas de Pantalla

Las capturas están disponibles en la carpeta `screenshots/`.

---

## 🚀 Instrucciones de uso

### Requisitos

- Tener Python instalado (versión 3.7 o superior).

### Ejecución

```bash
python cifrado_comentado.py
```

También puedes compilarlo a .exe con:

```bash
pyinstaller --onefile --windowed cifrado_comentado.py
```

---

## 🧪 Ejemplo de funcionamiento

### Entrada:
```
123456
```

### Cifrado:
```
890123 → 089123 → 019823 → 018932
```

### Descifrado:
```
018932 → original: 123456
```

---

## 👨‍💻 Autor

Desarrollado por **Mario Esteban Vargas Pisco**

---

## 📄 Licencia

Este proyecto se distribuye bajo la Licencia MIT.
