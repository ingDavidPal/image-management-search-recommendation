# image-management-search-recommendation
Python system for image management, metadata processing, search, galleries and image recommendation.
# Sistema de gestión, búsqueda y recomendación de imágenes

Proyecto académico desarrollado en Python para la gestión de una colección de imágenes, sus metadatos y galerías, incorporando funcionalidades de búsqueda y recomendación.

El proyecto utiliza diferentes estructuras de datos y componentes para identificar, almacenar, visualizar, buscar y gestionar imágenes.

## Descripción

El sistema trabaja con una colección de imágenes generadas y permite asociar a cada imagen un identificador único (UUID), su archivo correspondiente y diferentes metadatos.

Entre la información gestionada se encuentran datos como:

- Prompt utilizado para generar la imagen.
- Modelo utilizado.
- Seed.
- CFG Scale.
- Número de pasos.
- Sampler.
- Fecha de generación.
- Fecha de creación.

El proyecto también incorpora galerías de imágenes, lectura de metadatos directamente desde archivos PNG, búsqueda de imágenes y un sistema de recomendación.

## Funcionalidades principales

### Gestión de imágenes

El proyecto dispone de diferentes componentes para gestionar las imágenes y su información asociada.

Las imágenes se identifican mediante UUID y se relacionan con sus respectivos archivos.

Entre las operaciones implementadas se encuentran:

- Añadir imágenes.
- Eliminar imágenes.
- Asociar imágenes con sus archivos.
- Obtener información de una imagen mediante su UUID.
- Gestionar los metadatos asociados.
- Localizar archivos de imagen mediante diferentes rutas.

### Gestión de galerías

La clase `Gallery` permite organizar imágenes en galerías.

Una galería contiene:

- Nombre.
- Descripción.
- Fecha de creación.
- Lista de imágenes.

Permite realizar operaciones como:

- Cargar una galería desde un archivo JSON.
- Añadir imágenes.
- Eliminar la primera imagen.
- Eliminar la última imagen.
- Evitar imágenes duplicadas.
- Mostrar la información de la galería.
- Visualizar las imágenes que contiene.

Las imágenes de una galería se almacenan mediante sus UUIDs.

### Identificación mediante UUID

Las imágenes se identifican mediante UUID para poder trabajar con ellas independientemente de la ruta física del archivo.

El proyecto utiliza UUIDs deterministas generados a partir de la información del archivo, permitiendo asociar de forma consistente un identificador con cada imagen.

### Lectura de metadatos PNG

El proyecto implementa un lector de metadatos PNG sin utilizar librerías de procesamiento de imágenes como Pillow.

La función `read_png_metadata()` analiza directamente la estructura del archivo PNG.

Se procesan diferentes tipos de chunks de texto:

- `tEXt`
- `zTXt`
- `iTXt`

Para ello se utilizan las librerías estándar:

- `struct`
- `zlib`

`zlib` permite descomprimir información almacenada en determinados chunks del archivo PNG.

### Búsqueda de metadatos

El proyecto incluye un componente específico para trabajar con la información asociada a las imágenes y realizar operaciones de búsqueda relacionadas con sus metadatos.

El sistema puede trabajar con información como:

- Prompt.
- Modelo.
- Seed.
- CFG Scale.
- Steps.
- Sampler.
- Fecha de generación.
- Fecha de creación.

### Sistema de recomendación

El proyecto incluye un componente `RecommenderSystem.py` destinado a la recomendación de imágenes.

También se incluye el archivo `clip_vectors.json`, que contiene vectores asociados a las imágenes y forma parte de los datos utilizados por el sistema.

El proyecto dispone además de información de referencia mediante:

- `ground_truth_sample.json`

Estos archivos permiten trabajar con información necesaria para las funcionalidades de búsqueda/recomendación y para la evaluación del sistema.

### Visualización de imágenes

El componente `ImageViewer.py` se encarga de la visualización de las imágenes gestionadas por el sistema.

Las galerías pueden recorrer sus imágenes y solicitar al visualizador que muestre cada una de ellas.

### Gestión de archivos

`ImageFiles.py` se encarga de las operaciones relacionadas con los archivos de imagen.

El proyecto contempla diferentes representaciones de las rutas y realiza procesos de normalización para poder localizar correctamente los archivos.

Se contemplan:

- Rutas relativas.
- Rutas absolutas.
- Separadores `/` y `\`.
- Diferentes directorios de imágenes.
- Búsqueda por nombre de archivo como último recurso.

## Estructura del proyecto

```text
.
├── autograder.py
├── cfg.py
├── clip_vectors.json
├── Gallery.py
├── ground_truth_sample.json
├── ImageData.py
├── ImageFiles.py
├── ImageID.py
├── ImageViewer.py
├── RecommenderSystem.py
├── SearchMetadata.py
└── test_manual.py
