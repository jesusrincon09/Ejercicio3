# Prueba Técnica Software Engineer MID
Este repositorio contiene el desarrollo de la prueba técnica para el **cargo Software Engineer MID** el cual incluye los siguientes ejercicios:
1. Esquema de base de datos para una plataforma de blogs sencilla. La plataforma debe admitir usuarios, publicaciones de blog, comentarios y etiquetas. (EjercicioUno.png)
2. Función en lenguaje python que toma una lista de enteros y un entero de destino, y devuelva los índices de los dos números que sumados dan el resultado del entero destino. (EjercicioDos.py)
3. sistema de gestión de bibliotecas sencillo con clases para libros, bibliotecas y miembros, el cual se explica a continuacion. 


# API Biblioteca 

API REST para la **gestión de bibliotecas**, desarrollada con **Django REST Framework**, siguiendo una arquitectura en capas y principios SOLID.

---

## Descripción

Esta API permite administrar **bibliotecas, libros, miembros y préstamos**. 
Se mplementa:

- CRUD para todas las entidades principales.
- Validaciones necesarias para el correcto funcionamiento.
- Documentación interactiva con **Swagger / drf-spectacular**.
- Autenticación por **Token**.
- Arquitectura en capas: **Models → Repositories → services → ViewSets → Serializers**.
---
