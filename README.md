# TraductorData LaunchBox — Traducción MASIVA de Notas en el Metadata XML usando IA Offline 🚀

Después de muchísimo tiempo buscando una solución real para traducir metadata de LaunchBox… terminé cansándome 😅

Probé diferentes plugins de la comunidad pero honestamente no logre hacer funcionar ninguno. Supongo que el tema de cambio de versiones afecta bastante.

Así que terminé desarrollando mi propia aplicación pensada para funcionar con cualquier version de LaunchBox

El resultado es:

## 🎮 TraductorData LaunchBox

Una herramienta de escritorio que traduce automáticamente los nodos `<Notes>` de los XML de LaunchBox usando IA local.

No usa Google Translate.
No usa servicios online.
No requiere API Keys.
Todo corre directamente en tu PC.

# ✅ ¿Qué traduce exactamente?

La aplicación traduce el nodo:

<Notes>

De los XML de metadata de LaunchBox y los entrega respetando el resto de datos y estructura del XML.

Ideal para:

* Descripciones
* Historia de juegos
* Información técnica
* Metadata importada en inglés

---

# 🧠 ¿Qué usa internamente?

La app utiliza:

* HuggingFace Transformers
* M2M100
* CTranslate2
* Traducción IA offline
* Cache SQLite
* Correcciones gamer automáticas

Todo optimizado para grandes bibliotecas.

---

# ⚡ Características

✅ Traducción masiva
✅ Funciona completamente offline
✅ Usa IA real local
✅ Mantiene formato XML
✅ Cache inteligente muy rapido
✅ Perfiles LOW / BALANCED / HIGH
✅ Diseñada específicamente para LaunchBox

---

🚨☢️ AVISOS IMPORTANTES!!!

** La primera vez que ejecutes la aplicación, tardara un poco en arrancar. Es normal ya que debe generar directorios y validaciones.

** Se recomienda ejecutar como Administrador

** Se recomienda realizar siempre un backup de los archivos originales antes de reemplazarlos. 

** La primera vez realiza una prueba con un solo archivo para hacerte una idea de cuanto tardara en tu pc

*********************************************************************************************************** 
El tiempo total de traducción depende del rendimiento de tu PC y de la cantidad de textos a traducir, si un texto no se ha traducido nunca entonces tardara un poco mas en realizar el proceso pero la siguiente vez que detecte ese texto la traducción será casi instantánea.

Aproximadamente le toma poco menos de media hora por cada mil juegos de la colección durante LA PRIMERA TRADUCCION
Traducciones posteriores se hacen desde cache y se procesan en segundos.

************************************************************************************************************

---


# 📦 CÓMO USARLO (PASO A PASO)

## 1. LOCALIZAR LOS XML DE LAUNCHBOX

Ve a tu carpeta de LaunchBox.

Normalmente está en algo como:

\LaunchBox\Data\Platforms

Ahí encontrarás muchos archivos XML.

Ejemplo:


Nintendo Entertainment System.xml
Super Nintendo Entertainment System.xml
Sega Genesis.xml


** Si quieres traducir tambien las notas de las plataformas, incluye el archivo 

\LaunchBox\Data\Platforms.XML


---

# ⚠️ 2. HACER RESPALDO

MUY IMPORTANTE.

Antes de usar la herramienta:

Haz una copia de seguridad de tus XML originales.

Simplemente copia los XML a otra carpeta por seguridad.

---

# 📁 3. COPIAR XML A LA CARPETA INPUT

Dentro de la aplicación existe una carpeta llamada:

\input

Copia ahí los XML que deseas traducir.

---

# ▶️ 4. EJECUTAR LA APLICACIÓN

Abre:

TraductorData_LaunchBox.exe

👉 Ejecutar como administrador

---

# ⚙️ 5. CONFIGURAR CARPETAS INPUT Y OUTPUT

*********************************** NOTA IMPORTANTE*******************************

Se recomienda usar las carpetas Input y Output que se generan automáticamente en la misma ruta de la aplicación, deja estos campos como aparecen por default.

**********************************************************************************


# 🚀 6. ELEGIR PERFIL

La aplicación incluye perfiles:

* LOW
* BALANCED
* HIGH

Recomendación general:

✅ BALANCED

---

# 🧠 7. INICIAR TRADUCCIÓN

Presiona:

INICIAR TRADUCCIÓN

La aplicación:

* analizará los XML
* detectará idioma
* traducirá únicamente texto necesario
* conservará estructura XML
* guardará resultados automáticamente

---

# 📂 8. TOMAR LOS XML TRADUCIDOS

Cuando termine:

Los archivos traducidos aparecerán en:

\output


---

# 🔄 9. REEMPLAZAR EN LAUNCHBOX

Ahora simplemente:

1. Copia los XML traducidos
2. Pégalos nuevamente en:

```
\LaunchBox\Data\Platforms
y
\LaunchBox\Data\Platforms.XML
```

3. Reemplaza los originales

---

# 🎉 LISTO

Ahora LaunchBox mostrará las Notes traducidas al español.

---

# 📌 IMPORTANTE

La herramienta:

✅ SOLO traduce `<Notes>`
❌ NO modifica nombres de juegos
❌ NO altera imágenes
❌ NO cambia rutas
❌ NO rompe compatibilidad con LaunchBox

---

# 💾 TODO ES OFFLINE

✅ No necesita internet
✅ No consume APIs
✅ No tiene límites
✅ No manda datos a servidores

---

# ❤️ Proyecto hecho por necesidad real

Hice esta herramienta porque literalmente no encontré nada que resolviera este problema de forma seria y automatizada para LaunchBox.

Espero que le sirva a más gente de la comunidad tanto como me sirvió a mí.

Si alguien la prueba, agradecería muchísimo feedback 🙌
