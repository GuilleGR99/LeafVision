# LeafVision

Aplicación de escritorio para la identificación de especies vegetales mediante visión artificial.

## Descripción

LeafVision es un proyecto académico cuyo objetivo es desarrollar una aplicación capaz de identificar especies vegetales a partir de imágenes.

El usuario podrá seleccionar una imagen de su dispositivo o capturarla mediante una cámara. La imagen se enviará a un servidor que ejecutará un modelo de visión artificial y devolverá el resultado de la identificación.

## Funcionalidades principales

- Registro e inicio de sesión de usuarios.
- Selección de imágenes desde el dispositivo.
- Captura de imágenes mediante una cámara.
- Validación de imágenes en formato JPG o PNG, con un tamaño máximo de 10 MB.
- Identificación de plantas mediante un modelo de visión artificial.
- Visualización del nombre común, nombre científico, porcentaje de confianza e imagen de referencia.
- Consulta del historial de identificaciones de cada usuario.

El sistema está limitado a las especies incluidas en el entrenamiento del modelo y está diseñado para procesar una sola planta por imagen.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Aplicación de escritorio | Java |
| Interfaz gráfica | JavaFX y JFoenix |
| Procesamiento e inferencia | Python |
| Dataset de entrenamiento | Kaggle |
| Comunicación cliente-servidor | TCP |
| Base de datos | MySQL |

## Arquitectura general

El sistema se compone de los siguientes elementos:

1. **Aplicación de escritorio:** permite al usuario gestionar su cuenta, seleccionar imágenes y consultar los resultados.
2. **Servidor de procesamiento:** recibe las imágenes y ejecuta el modelo de visión artificial desarrollado en Python.
3. **Base de datos:** almacena la información de los usuarios y su historial de identificaciones.

El despliegue previsto es local.

## Flujo de funcionamiento

1. El usuario se registra o inicia sesión.
2. Selecciona o captura una imagen.
3. La aplicación valida el formato y el tamaño de la imagen.
4. El usuario previsualiza y confirma la imagen.
5. La imagen se envía al servidor mediante TCP.
6. El modelo procesa la imagen y genera una predicción.
7. Si la confianza supera el umbral establecido, se muestra el resultado.
8. El análisis queda asociado al usuario y puede consultarse desde su historial.

Si la imagen no cumple los requisitos o la confianza de la predicción es insuficiente, la aplicación informa al usuario de que no ha sido posible completar la identificación.

## Estado del proyecto

Proyecto en desarrollo.

Los detalles de implementación, configuración del entorno y ejecución se incorporarán conforme avance el desarrollo.

## Equipo

- Alberto Noval
- Cayetano Biehler Pollaci
- Guillermo García Rodríguez
- Juan Pizá

**Proyecto de Informática I**  
Ingeniería Informática
