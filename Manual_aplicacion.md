
MANUAL DE APLICACIÓN
TraductorData LaunchBox v1
===============================================

1. DESCRIPCIÓN GENERAL
------------------------------------------------

TraductorData LaunchBox es una aplicación de escritorio desarrollada en Python
cuya finalidad es traducir automáticamente al español los nodos <Notes> dentro
de archivos XML utilizados por LaunchBox.

El programa utiliza Inteligencia Artificial local (offline) basada en el modelo:

    facebook/m2m100_418M

La traducción se realiza completamente en la computadora del usuario y no depende
de servicios en línea como Google Translate, DeepL o APIs externas.

La aplicación está diseñada especialmente para colecciones grandes de metadata
de videojuegos de LaunchBox, permitiendo automatizar la traducción masiva de
descripciones y notas.



2. FUNCIONAMIENTO INTERNO
------------------------------------------------

La aplicación trabaja siguiendo el siguiente flujo:

1. El usuario selecciona una carpeta de entrada (input).
2. El programa busca todos los archivos XML dentro de esa carpeta.
3. Cada archivo XML es analizado.
4. Se localizan los nodos:

       <Notes>

5. El texto encontrado es limpiado y normalizado.
6. Se detecta automáticamente el idioma.
7. Solo se traducen textos detectados como inglés.
8. El sistema divide el contenido en oraciones.
9. Cada oración se traduce usando IA local.
10. El texto traducido pasa por una etapa de corrección.
11. Se aplican reglas especiales orientadas a terminología gamer.
12. El resultado se guarda en un nuevo XML dentro de la carpeta output.



3. SISTEMA DE IA UTILIZADO
------------------------------------------------

La aplicación utiliza varias tecnologías internas:

- Transformers (HuggingFace)
- M2M100
- CTranslate2
- SentencePiece
- LangDetect

El modelo original es convertido automáticamente a formato optimizado CT2
(CTranslate2) para reducir consumo de recursos y mejorar velocidad.

El sistema puede funcionar completamente offline una vez descargados
los modelos.



4. SISTEMA DE CACHE
------------------------------------------------

La aplicación incluye una base de datos SQLite local ubicada en:

    cache/translation_cache.db

Su función es almacenar traducciones ya realizadas.

Ventajas:

- Evita traducir el mismo texto varias veces.
- Acelera enormemente futuras ejecuciones.
- Reduce consumo de CPU.
- Mantiene consistencia entre traducciones.

Cada texto se almacena usando un hash SHA1 como identificador único.



5. DICCIONARIO GAMER
------------------------------------------------

La aplicación utiliza un archivo:

    gamer_dictionary.json

Este archivo contiene reemplazos personalizados relacionados con términos
de videojuegos.

Ejemplo:

- handheld console -> consola portátil
- backward compatible -> retrocompatible

El diccionario se aplica antes de traducir.

Esto permite mejorar precisión y contexto para metadata de videojuegos.
Este diccionario puede ser ampliado o modificado para personalizar aun mas las traducciones.


6. SISTEMA DE CORRECCIÓN AUTOMÁTICA
------------------------------------------------

Después de traducir, el programa ejecuta una fase de corrección donde
reemplaza errores comunes generados por IA.

Ejemplos:

- "liberación occidental"
  se corrige a:
  "lanzamiento occidental"

- "modo standby"
  se corrige a:
  "modo de espera"

- "portable system"
  se corrige a:
  "consola portátil"

Esto ayuda a producir traducciones más naturales y coherentes.



7. INTERFAZ PRINCIPAL
------------------------------------------------

La interfaz está dividida en varias zonas:


------------------------------------------------
CARPETA INPUT
------------------------------------------------

Aquí se selecciona la carpeta que contiene los XML originales.

------------------------------------------------
CARPETA OUTPUT
------------------------------------------------

Aquí se define la carpeta donde se guardarán
los XML traducidos.

------------------------------------------------
PERFIL
------------------------------------------------

La aplicación incluye 3 perfiles de rendimiento:

LOW
BALANCED
HIGH

Cada perfil modifica:

- batch size
- workers
- inter threads
- velocidad
- consumo de RAM y CPU

------------------------------------------------
BARRA DE PROGRESO
------------------------------------------------

Muestra:

- progreso total
- cantidad de nodos procesados
* la cantidad de nodos procesados es la cantidad de bloques de texto que se enviaran a la IA para traducir

Ejemplo:

    150 / 200

------------------------------------------------
ESTADÍSTICAS DEL SISTEMA
------------------------------------------------

La aplicación monitorea en tiempo real:

- RAM actual
- CPU actual
- RAM promedio
- CPU promedio
- RAM máxima
- CPU máximo

Esto permite evaluar el rendimiento del sistema.

------------------------------------------------
BOTÓN INICIAR TRADUCCIÓN
------------------------------------------------

Inicia el procesamiento completo.

------------------------------------------------
BOTÓN ABORTAR
------------------------------------------------

Detiene inmediatamente el proceso de traducción.

------------------------------------------------
CONSOLA INTERNA
------------------------------------------------

Muestra mensajes del sistema en tiempo real.

Ejemplos:

- archivos procesados
- errores
- carga de IA
- estadísticas
- tiempos
- finalización



8. PERFILES DE RENDIMIENTO
------------------------------------------------

LOW
----

Configuración ligera.

Usa pocos recursos.

Ideal para:
- PCs antiguas
- laptops modestas
- servidores limitados

BALANCED
--------

Configuración equilibrada.

Es el perfil recomendado.

HIGH
----

Máximo rendimiento.

Mayor consumo de RAM y CPU.

Ideal para:
- procesadores modernos
- muchas traducciones
- sistemas potentes



9. ESTRUCTURA DE CARPETAS
------------------------------------------------

La aplicación utiliza la siguiente estructura:

backups/
cache/
input/
logs/
models/
output/

Archivos importantes:

main.py
settings.json
gamer_dictionary.json

------------------------------------------------
CARPETA MODELS
------------------------------------------------

Contiene los modelos de IA.

Subcarpetas:

models/m2m100_original
models/m2m100_ct2

------------------------------------------------
CARPETA CACHE
------------------------------------------------

Contiene la base de datos SQLite.

------------------------------------------------
CARPETA LOGS
------------------------------------------------

Contiene:

    app.log

Aquí se registran eventos y errores.

------------------------------------------------
CARPETA INPUT
------------------------------------------------

XML originales.

------------------------------------------------
CARPETA OUTPUT
------------------------------------------------

XML traducidos.



10. PROCESO DE USO
------------------------------------------------

PASO 1
------

Abrir la aplicación.

PASO 2
------

Seleccionar carpeta INPUT.

PASO 3
------

Seleccionar carpeta OUTPUT.

PASO 4
------

Elegir perfil de rendimiento.

PASO 5
------

Presionar:

    INICIAR TRADUCCIÓN

PASO 6
------

Esperar a que termine el procesamiento.

PASO 7
------

Los XML traducidos aparecerán en la carpeta OUTPUT.



11. REQUISITOS
------------------------------------------------

Para funcionamiento correcto:

- Windows 10/11
- Visual C++ Redistributable
- Permisos de escritura
- Espacio suficiente en disco

En algunos servidores Windows puede ser necesario:

    Ejecutar como administrador



12. FUNCIONAMIENTO PORTABLE
------------------------------------------------

La aplicación fue compilada como versión portable.

En este modo:

- no requiere instalación
- puede moverse entre PCs
- usa rutas relativas
- mantiene modelos localmente

Sin embargo:

- los modelos pesan mas de un GB
- algunas PCs requieren permisos elevados



13. LIMITACIONES
------------------------------------------------

La aplicación solo traduce:

    nodos <Notes>

No modifica:

- títulos
- nombres
- géneros
- desarrolladores
- otras etiquetas XML

La precisión depende de:

- calidad del modelo
- contexto del texto
- terminología original



14. OBJETIVO DEL PROYECTO
------------------------------------------------

El objetivo principal del proyecto es automatizar la traducción masiva
de metadata de videojuegos de LaunchBox usando IA local de alta calidad,
manteniendo:

- velocidad
- coherencia
- funcionamiento offline
- reutilización de cache
- terminología gamer adecuada



===============================================
FIN DEL MANUAL
===============================================
