# 🦎 GeckoNotes — v4.6 (Demo Testing)

[![Python v3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/UI-PyQt5-green.svg)](https://pypi.org/project/PyQt5/)
[![Ecosistema](https://img.shields.io/badge/Environment-Xubuntu%20%2F%20XFCE-orange.svg)](https://xubuntu.org/)

> **"El software no es solo lógica fría; es empatía codificada. Cuando una aplicación 'recuerda' cómo le gusta al usuario ver sus cosas, deja de ser una herramienta para convertirse en un compañero."**

---

## 🧠 El Manifiesto Visual (Memoria Eidética Aplicada)

GeckoNotes v4.6 no es un bloque de texto plano rígido; es la aplicación práctica de la **Búsqueda Pre-atentiva** y la cognición humana aplicadas al desarrollo de software. Diseñado específicamente para reemplazar las herramientas de notas por defecto en entornos **Xubuntu (XFCE)**, este entorno se basa en tres pilares neuro-estéticos:

1. **Carga Cognitiva Cero:** El cerebro humano procesa el color y la geometría fractal mucho antes que la lectura semántica. No necesitas leer tus categorías; tu ojo detecta el color asignado de forma instantánea.
2. **Categorización Semántica Personalizada:** Un lenguaje visual libre donde el usuario define sus prioridades (ej. Amarillo = Mercado/Finanzas, Verde = Desarrollo, Rojo = Crítico). La app se adapta al pensamiento del usuario, no al revés.
3. **Persistencia Dinámica Absoluta:** Un mapa mental persistente que recuerda tamaños, fuentes y colores nota por nota, sesión tras sesión.

---

## 🚀 Características y Componentes del Sistema

| Módulo / Control | Tipo de Componente | Funcionalidad Geckónica |
| :--- | :--- | :--- |
| **🔒 Tomahawk Safety** | `QPushButton` (Switch) | Seguro de retención que congela el editor, sliders y selectores para blindar las notas contra modificaciones accidentales en producción. |
| **🎨 Selectores L:🎨 y T:🎨** | `QColorDialog` (Custom) | Diálogos de color no nativos modificados para inyectar hojas de estilo dinámicas en tiempo real sobre la lista y el editor. |
| **🎚️ Sliders de Precisión** | `PrecisionSlider` / `QSlider` | Control vertical simétrico para calibrar el tamaño de la fuente de la lista (8px a 32px) y del texto en tiempo real. |
| **🛡️ Escudo de Localización** | Lógica de Pathing Automático | Detecta de forma inteligente el idioma del sistema operativo (`Notes` / `Notas`) en `~/.local/share/notes` para una caída segura. |
| **📦 Portabilidad Cuántica** | `tarfile` (Compresión Nativa) | **[Módulo v4.6]** Exportación e importación de Backups completos en formato `.tar.gz`, resolviendo la fusión de archivos y metadatos sin scripts externos. |

---

## 🛠️ Arquitectura e Inmunidad a los "Pokerrorres"

* **El Hechizo de Silenciamiento Magnético (`blockSignals`):** Para evitar bucles recursivos y desbordes de memoria cuando el usuario navega de forma veloz por la lista, el sistema duerme temporalmente las señales de Qt (`blockSignals(True)`) mientras ordena los estilos en el plano físico.
* **Auto-Guardado Desacoplado (`QTimer`):** Implementa un temporizador de disparo único (`setSingleShot`) que agenda el guardado en disco 1000 ms después del último cambio en el teclado. Esto elimina la fricción de botones de "Guardar" y optimiza las escrituras en disco.
* **Persistencia Estructurada (El amado "Sheison"):** Las configuraciones visuales se empaquetan en un archivo `gecko_config.json` independiente, mapeando los metadatos de estilo directamente al identificador de la nota. Si renombras una nota, la persistencia viva migra los metadatos al instante.
* **Posicionamiento Inteligente:** Al inicializarse, el script consulta la geometría de la pantalla activa y se posiciona de forma exacta en la esquina inferior derecha del área útil de Xubuntu, manteniéndose accesible pero fuera de la línea de fuego de tu espacio de trabajo.

---

## 📦 Dependencias Estructurales

Para correr la demo testing en un entorno limpio, solo necesitas el motor de Python y las siguientes librerías del ecosistema:

```bash
pip install PyQt5 qdarkstyle
