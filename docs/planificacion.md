# LEAFVISION — Documento de planificación del desarrollo

## 1. Introducción

Este documento establece la planificación inicial del desarrollo. 

El desarrollo se organizará en cuatro flujos de trabajo independientes. Cada flujo tendrá un conjunto definido de objetivos. Los módulos se desarrollarán en paralelo siempre que sus dependencias lo permitan y se integrarán progresivamente hasta obtener el sistema completo.

La planificación se basa en las necesidades y requisitos definidos para el proyecto.

## 2. Arquitectura de referencia

El sistema estará compuesto por los siguientes elementos:

- **Aplicación de escritorio:** desarrollada en Java, con JavaFX y JFoenix.
- **Persistencia:** MySQL, gestionado desde la aplicación Java.
- **Servidor de identificación:** desarrollado en Python, encargado de ejecutar el modelo de visión artificial.
- **Comunicación:** protocolo TCP entre la aplicación Java y el servidor Python.
- **Despliegue:** entorno local.

La aplicación Java gestionará la interfaz gráfica, los usuarios y la persistencia. El servidor Python se encargará exclusivamente del procesamiento de las imágenes y la identificación de las plantas.

## 3. Organización del desarrollo

El proyecto se dividirá en los siguientes flujos:

| Identificador | Flujo de trabajo | Rama Git |
|---|---|---|
| F1 | Interfaz gráfica y experiencia de usuario | `feature/ui` |
| F2 | Gestión de usuarios y persistencia | `feature/persistence` |
| F3 | Modelo de visión artificial y servidor Python | `feature/plant-classifier` |
| F4 | Comunicación TCP e integración del sistema | `feature/tcp-integration` |

Cada flujo desarrollará y probará su módulo de forma independiente. Las interfaces entre módulos se definirán antes de comenzar su integración.

## 4. F1 — Interfaz gráfica y experiencia de usuario

### Objetivo

Desarrollar la interfaz de escritorio que permita al usuario interactuar con LEAFVISION, desde el acceso a la aplicación hasta la consulta de los resultados y del historial.

### Tareas

**F1.1 — Preparación de la interfaz**
1. Crear la estructura inicial de la aplicación JavaFX.
2. Incorporar JFoenix y configurar los elementos gráficos comunes.
3. Definir la navegación entre las distintas vistas.

**F1.2 — Acceso de usuarios**
4. Implementar la vista de registro.
5. Implementar la vista de inicio de sesión.
6. Integrar las vistas con los servicios de usuario mediante una interfaz provisional.

**F1.3 — Entrada de imágenes**
7. Implementar la selección de imágenes desde el dispositivo.
8. Implementar la captura de imágenes mediante cámara.
9. Validar los formatos JPG y PNG.
10. Validar el tamaño máximo de 10 MB.
11. Implementar la previsualización de la imagen.
12. Permitir seleccionar o capturar otra imagen antes del análisis.

**F1.4 — Presentación de resultados**
13. Implementar el indicador de carga.
14. Implementar la vista de identificación válida.
15. Mostrar nombre común, nombre científico, porcentaje de confianza e imagen de referencia.
16. Implementar la vista de identificación fallida.
17. Implementar la presentación de errores.

**F1.5 — Historial**
18. Implementar la vista del historial de identificaciones.
19. Mostrar los análisis asociados al usuario autenticado.

### Pruebas

- Navegación entre vistas.
- Validación de formato y tamaño.
- Previsualización y sustitución de imágenes.
- Presentación de resultados simulados.
- Presentación de errores y predicciones fallidas.
- Visualización del historial mediante datos de prueba.

### Entregable

Módulo de interfaz gráfica funcional.

## 5. F2 — Gestión de usuarios y persistencia

### Objetivo

Implementar la gestión de usuarios y el almacenamiento de los resultados e historial de identificaciones mediante MySQL.

### Tareas

**F2.1 — Diseño de persistencia**
1. Diseñar el esquema de la base de datos.
2. Definir las entidades de usuario e identificación.
3. Definir la relación entre usuarios y análisis.
~~4. Definir la estrategia de almacenamiento de imágenes.~~
5. Crear el esquema inicial de MySQL.

**F2.2 — Acceso a datos**
6. Configurar la conexión a MySQL desde Java.
7. Implementar las operaciones de acceso a datos.
8. Implementar el manejo de errores de persistencia.

**F2.3 — Gestión de usuarios**
9. Implementar el registro de usuarios.
10. Implementar el inicio de sesión.
11. Implementar la validación de credenciales.

**F2.4 — Persistencia de identificaciones**
12. Implementar el almacenamiento de imágenes.
13. Implementar el almacenamiento de resultados.
14. Asociar cada análisis con el usuario autenticado.
15. Implementar la consulta del historial.
16. Garantizar que cada usuario solo pueda consultar sus propios análisis.

### Pruebas

- Registro e inicio de sesión.
- Persistencia y recuperación de usuarios.
- Almacenamiento y recuperación de imágenes y resultados.
- Consulta del historial.
- Verificación del aislamiento entre usuarios.
- Manejo de errores de conexión y persistencia.

### Entregable

Módulo Java de persistencia y gestión de usuarios y esquema SQL.

## 6. F3 — Modelo de visión artificial y servidor Python

### Objetivo

Desarrollar el modelo de clasificación de plantas y el servidor local encargado de recibir imágenes, ejecutar la inferencia y devolver el resultado.

### Tareas

**F3.1 — Preparación del dataset**
1. Seleccionar un dataset de plantas de Kaggle.
2. Identificar las clases y especies disponibles.
3. Preparar las imágenes para el entrenamiento.
4. Dividir el dataset en conjuntos de entrenamiento, validación y prueba.

**F3.2 — Entrenamiento y evaluación**
5. Seleccionar la arquitectura del modelo.
6. Entrenar el modelo de clasificación.
7. Evaluar el rendimiento del modelo.
8. Seleccionar un umbral de confianza a partir de la evaluación.
9. Asociar las clases con sus nombres comunes y científicos.
10. Asociar las clases con sus imágenes de referencia.

**F3.3 — Inferencia**
11. Implementar la carga del modelo entrenado.
12. Implementar la inferencia sobre una imagen.
13. Implementar la validación del umbral de confianza.
14. Implementar la respuesta de identificación fallida.
15. Implementar el manejo de errores de inferencia.

**F3.4 — Servidor**
16. Implementar el servidor Python local.
17. Implementar la recepción de imágenes.
18. Implementar la respuesta con los resultados.
19. Implementar el manejo de conexiones y errores.

### Pruebas

- Inferencia sobre imágenes de prueba.
- Evaluación del modelo con métricas de clasificación.
- Validación del umbral de confianza.
- Pruebas de identificación fallida.
- Pruebas del servidor con imágenes válidas e inválidas.
- Verificación de la estructura de las respuestas.

### Entregable

Modelo entrenado, código de inferencia, servidor Python ejecutable y resultados de evaluación.

## 7. F4 — Comunicación TCP e integración

### Objetivo

Implementar la comunicación entre la aplicación Java y el servidor Python y coordinar la integración progresiva de los módulos.

### Tareas

**F4.1 — Definición del protocolo**
1. Definir el protocolo de comunicación TCP.
2. Definir el formato de las solicitudes.
3. Definir el mecanismo de transferencia de imágenes.
4. Definir el formato de las respuestas.
5. Definir los códigos y mensajes de error.
6. Definir el mecanismo de delimitación de mensajes.

**F4.2 — Implementación de la comunicación**
7. Implementar el cliente TCP en Java.
8. Implementar la recepción de solicitudes en Python.
9. Implementar el envío y recepción de respuestas.
10. Implementar el manejo de desconexiones y tiempos de espera.

**F4.3 — Pruebas de comunicación**
11. Probar el envío de imágenes desde Java.
12. Probar la recepción de resultados.
13. Probar respuestas fallidas y errores de conexión.

**F4.4 — Integración**
14. Integrar el cliente TCP con la interfaz Java.
15. Integrar el servidor Python real.
16. Integrar los resultados con el módulo de persistencia.
17. Verificar el flujo completo de identificación.
18. Preparar la configuración de ejecución local.
19. Documentar el procedimiento de ejecución.

### Pruebas

- Comunicación Java-Python.
- Transferencia de imágenes.
- Respuestas válidas y fallidas.
- Servidor no disponible.
- Tiempo de espera agotado.
- Persistencia del resultado recibido.
- Ejecución del flujo completo.

### Entregable

Módulo de comunicación TCP, pruebas de integración y configuración para ejecutar LEAFVISION localmente.

## 8. Secuencia de desarrollo e integración

El desarrollo se organizará mediante los siguientes hitos:

### Hito 1 — Contratos comunes

Antes de implementar las dependencias entre módulos, se deberán acordar:

- Estructura de los datos de usuario.
- Estructura de los datos de identificación.
- Esquema inicial de la base de datos.
- Protocolo TCP.
- Formato de respuestas y errores.
- Estrategia de almacenamiento de imágenes.

**Resultado:** contratos técnicos definidos para permitir el desarrollo paralelo.

### Hito 2 — Desarrollo independiente

Cada flujo desarrolla su módulo y realiza pruebas unitarias.

**Resultado:** módulos ejecutables y pruebas unitarias satisfactorias.

### Hito 3 — Comunicación Java-Python

Se integra el cliente TCP Java con el servidor Python real.

**Resultado:** una imagen enviada desde Java puede ser procesada por Python y devolver una respuesta.

### Hito 4 — Integración de persistencia

Se conecta el resultado recibido con el módulo de MySQL. Los análisis se almacenan asociados al usuario correspondiente.

**Resultado:** el sistema persiste y recupera los resultados de identificación.

### Hito 5 — Integración de interfaz

Se conecta la interfaz con la comunicación TCP y los servicios de persistencia.

**Resultado:** el usuario puede realizar una identificación y consultar posteriormente su historial.

### Hito 6 — Validación del sistema

Se ejecutan las pruebas de extremo a extremo y se verifica el cumplimiento de los requisitos.

**Resultado:** versión integrada de LEAFVISION preparada para la demostración local.

## 9. Estrategia de Git

Cada flujo trabajará en su rama independiente:

- `feature/ui`
- `feature/persistence`
- `feature/plant-classifier`
- `feature/tcp-integration`

Las integraciones se realizarán mediante pull requests a la rama develop para la integración de modulos. 

## 10. Criterios generales de finalización

El proyecto se considerará integrado cuando:

- La aplicación permita registrar e iniciar sesión.
- El usuario pueda seleccionar o capturar una imagen válida.
- La imagen se envíe al servidor Python mediante TCP.
- El servidor devuelva una identificación o una respuesta de fallo.
- La interfaz muestre el resultado de forma comprensible.
- El análisis quede almacenado en MySQL.
- El usuario pueda consultar su historial.
- Se verifique que los usuarios no acceden a análisis ajenos.
- Se hayan probado los principales errores de comunicación, procesamiento y persistencia.
- El sistema pueda ejecutarse en el entorno local previsto.
