# Fase4-Practicas-Simuladas-213023_329-GJP

# 🏢 Software FJ - Reservation Engine 🚀

![Python](https://img.shields.io/badge/Python-3.12-57CC99?style=for-the-badge&logo=python&logoColor=white)
![POO](https://img.shields.io/badge/Architecture-POO-1A1A1A?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-100%25_Functional-success?style=for-the-badge)

Este repositorio contiene la solución técnica para el **Sistema Integral de Gestión de Clientes, Servicios y Reservas** (Fase 4 - Componente Práctico). Desarrollado bajo un enfoque estricto de Programación Orientada a Objetos (POO) y tolerancia a fallos.

## 🎯 Características Principales (Core Features)

* **Arquitectura Sin BD:** Gestión de datos 100% en memoria mediante listas y objetos instanciados.
* **Excepciones Avanzadas:** Sistema blindado contra caídas mediante bloques `try/except/else/finally` y *Exception Chaining*.
* **Polimorfismo & Sobrecarga:** Cálculo dinámico de tarifas (Salas, Equipos, Asesorías) con parámetros opcionales.
* **Telemetría Automática:** Registro de eventos (Info, Warning, Critical) directamente a un archivo `sistema_fj.log`.
* **UI de Diagnóstico:** Interfaz gráfica minimalista en Tkinter para simular operaciones en lote (Batch).

## 🛠️ Estructura de Clases

1.  `EntidadBase` (Clase Abstracta Maestra).
2.  `Cliente` (Implementa encapsulamiento estricto de datos).
3.  `Servicio` (Clase Abstracta para jerarquía de servicios).
    * ↳ `SalaReunion`
    * ↳ `EquipoComputo`
    * ↳ `AsesoriaEspecializada`
4.  `Reserva` (Controlador de lógica de negocio y manejo de errores).

## 🚀 ¿Cómo ejecutar la suite de pruebas?

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/Fase4-Practicas-Simuladas-213023_329-GJP.git](https://github.com/tu-usuario/Fase4-Practicas-Simuladas-213023_329-GJP.git)
