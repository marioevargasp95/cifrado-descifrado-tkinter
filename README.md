# 🔐 Aplicación de Cifrado y Descifrado de Números

**Nombre del estudiante:** Mario Esteban Vargas Pisco  
**Asignatura:** Aplicaciones I  
**Fecha:** Mayo 10, 2025  

---

## 📘 Introducción

Esta aplicación fue desarrollada como parte del curso de Aplicaciones I con el propósito de implementar una interfaz gráfica en Python que permita al usuario cifrar y descifrar números de seis dígitos aplicando una lógica algorítmica.  
El objetivo principal es familiarizarse con el desarrollo de interfaces usando `Tkinter`, aplicar lógica de programación y generar un entregable funcional empaquetado como ejecutable.

---

## ⚙️ Desarrollo

El programa consta de una ventana principal desde la cual el usuario puede:
- **Cifrar un número**: se abre una ventana para ingresar un número de 6 dígitos y aplicar el algoritmo de cifrado.
- **Descifrar un número**: se abre una ventana para revertir el cifrado y obtener el número original.

### Algoritmo de cifrado:
1. Se suma 7 a cada dígito y se aplica módulo 10.
2. Se intercambian las posiciones:
   - 1º ↔ 3º
   - 2º ↔ 4º
   - 5º ↔ 6º

### Ventanas de la aplicación:

| Ventana principal                      | Ventana de cifrado                    | Ventana de descifrado                 |
|----------------------------------------|---------------------------------------|---------------------------------------|
| ![Main](screenshots/main.PNG) | ![Cifrado](screenshots/cifrado.PNG) | ![Descifrado](screenshots/descifrado.PNG) |

---

## 🧪 Pruebas de funcionalidad

| Entrada original | Número cifrado | Descifrado (resultado) |
|------------------|----------------|-------------------------|
| 123456           | 098723         | 123456                  |
| 987654           | 432109         | 987654                  |
| 222222           | 999999         | 222222                  |

---

## 🧠 Conclusión

A través de esta actividad se logró comprender la estructura básica de una interfaz gráfica usando Python y Tkinter. Se aplicaron principios de lógica y diseño modular, además de integrarse con herramientas como PyInstaller y GitHub. Este proyecto fortaleció la autonomía técnica en el desarrollo de soluciones sencillas, prácticas y presentables.