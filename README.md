# Prueba Técnica Software Engineer MID
Este repositorio contiene el desarrollo de la prueba técnica para el **cargo Software Engineer MID** el cual incluye los siguientes ejercicios:
1. Esquema de base de datos para una plataforma de blogs sencilla. La plataforma debe admitir usuarios, publicaciones de blog, comentarios y etiquetas. (EjercicioUno.png)
2. Función en lenguaje python que toma una lista de enteros y un entero de destino, y devuelva los índices de los dos números que sumados dan el resultado del entero destino. (EjercicioDos.py)
3. sistema de gestión de bibliotecas sencillo con clases para libros, bibliotecas y miembros, el cual se explica a continuacion. 


## API Biblioteca 

API REST para la **gestión de bibliotecas**, desarrollada con **Django REST Framework**, siguiendo una arquitectura en capas y principios SOLID.

---

## Descripción

Esta API permite administrar **bibliotecas, libros, miembros y préstamos**. 
Se implementa:

- CRUD para todas las entidades principales.
- Validaciones necesarias para el correcto funcionamiento.
- Documentación interactiva con **Swagger / drf-spectacular**.
- Autenticación por **Token**.
- Arquitectura en capas: **Models → Repositories → services → ViewSets → Serializers**.
---

## Proceso de instalación 
1. **Instalar Docker**  
   - Para Windows: [Guía de instalación](https://docs.docker.com/desktop/setup/install/windows-install/)  
   - Para Linux: instalar según tu distribución (Ubuntu, Debian, Fedora, etc.)

2. **Clonar el repositorio**  

```bash
git clone https://github.com/jesusrincon09/TestSoftwareEngineerMID.git
````

3. Abrir terminal en la raíz del proyecto y ejecutar:
```bash
docker compose up --build
````
4. Acceder a la documentación de la API en el navegador:
```bash
http://localhost:8000/api/docs/swagger/
````
5. *Nota:* El contenedor de Docker incluye todo lo necesario para ejecutar el proyecto, incluyendo entorno virtual y base de datos.
6. Usuario de prueba para generar token de acceso
```bash
{
  "username": "admin",
  "password": "admin123"
}

````

## Endpoints principales

| Entidad   | Endpoint                     | Métodos                      |
|-----------|----------------------------- |------------------------------|
| Libraries | /api/libraries/              | GET, POST, PUT, DELETE |
| Books     | /api/books/                  | GET, POST, PUT, DELETE |
| Members   | /api/members/                | GET, POST, PUT, DELETE |
| Loans     | /api/loans/                  | GET, POST |
| Loans     | /api/loans/{id}/return/      | POST |
| token     | /api/token/                  | POST |



