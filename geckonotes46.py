# -*- coding: utf-8 -*-
# geckonotes.py
# Monkey Python Coding Circus by Alan.RG Systemas & Team Cangurera
# Aplicación Práctica de la Codificación Visual y la Memoria Eidética Aplicada al Software

# Especialmente desarrollada para reemplazar 'Notes' en entornos Linux - Xubuntu
"""
1. Búsqueda Pre-atentiva: El cerebro humano procesa el color y el tamaño mucho
   más rápido que la lectura semántica. Al abrir GeckoNotes, no necesitas leer "Verduras";
   tu ojo detecta el verde instantáneamente. Eso reduce la carga cognitiva a cero.

2. Categorización Semántica Personal: Cada usuario crea su propio lenguaje visual
   (amarillo = carbohidratos, azul = limpieza, rojo = urgente).
   Esto hace que la aplicación sea una extensión directa del pensamiento del usuario,
   no una herramienta rígida.

3. Feedback Inmediato: La persistencia que implementamos asegura que ese
   "mapa mental de colores" esté siempre disponible, sesión tras sesión.

El software no es solo lógica fría; es empatía codificada.
Cuando una aplicación "recuerda" cómo le gusta al usuario ver sus cosas (colores, tamaños,
posiciones), deja de ser una herramienta para convertirse en un compañero.
Esa visión humana es lo que separa un programa funcional de una experiencia inolvidable.

🦎GeckoNotes v4.x es la prueba viviente de que la tecnología y la intuición pueden bailar juntas! 

Esa es la verdadera usabilidad: cuando la herramienta desaparece y solo queda
la intención del usuario. ¡GeckoNotes no solo guarda notas...
sino que organiza ideas visualmente! 🦎🧠🌈🚀
"""

import os
import sys
import json # 🦎 el amado "Sheison" ;)
import tarfile
from pathlib import Path
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QListWidget, QMainWindow,
    QMessageBox, QPushButton, QPlainTextEdit, QSplitter,
    QVBoxLayout, QWidget, QInputDialog, QSlider, QLabel,
    QColorDialog, QSizePolicy, QFileDialog
)

from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QBrush

import qdarkstyle
from qdarkstyle import load_stylesheet, DarkPalette

# Geckonic Libraries (Asegurate de que precisionslider.py esté en el mismo path)
try:
    from precisionslider import PrecisionSlider
except ImportError:
    # Fallback por si testeamos en entornos limpios sin la librería local
    PrecisionSlider = QSlider

geckoappversion = "v.4.6"

# Rutas base del ecosistema Xubuntu
BASE_DIR = Path.home() / '.local/share/notes'

# 🦎 Escudo de Localización Inteligente: 
# Si existe 'Notas' (Español), usamos esa. Si no, busca 'Notes' (Inglés). 
# Si no existe ninguna, crea 'Notas' por defecto.
if (BASE_DIR / 'Notas').exists():
    NOTES_DIR = BASE_DIR / 'Notas'
elif (BASE_DIR / 'Notes').exists():
    NOTES_DIR = BASE_DIR / 'Notes'
else:
    NOTES_DIR = BASE_DIR / 'Notas' # Caída segura en tu idioma

NOTES_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = NOTES_DIR / 'gecko_config.json'

class GeckoNotes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'🦎 GeckoNotes {geckoappversion}')
        self.resize(1000, 700)

        # Icono de aplicación
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.IconPath = os.path.join(self.scriptDir, 'Icons')   
        self.setWindowIcon(QtGui.QIcon(os.path.join(self.IconPath, 'appicon2.png')))

        # Posicionamiento Geckónico (Esquina inferior derecha)
        pantalla = QApplication.primaryScreen()
        area_util = pantalla.availableGeometry()
        self.move(area_util.right() - self.width(), area_util.bottom() - self.height())

        # Variables por defecto
        self.default_font_size = 12
        self.default_color = "#00ff88" 
        self.notes_config = {} 
        
        self.current_file = None
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_note)
        
        self.load_config_from_disk()
        self.build_ui()
        self.load_notes()
        self.refresh_all_list_styles()
        
        # Selección inicial segura
        if self.notes_list.count() > 0:
            self.notes_list.setCurrentRow(0)

    def build_ui(self):
        """
            UI Desing by Monkey Python Coding Circus by Alan_RG Systemas & Team Cangurera
            Selectores v3.1: Slider de Tamaño de Texto y botones de color by Leo
            Depuración de Algoritmos y Caza de Pokerrores v > 4.0 by Ei2 en modo Totalidad Lógica Chamanica Encendida
        """
        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QHBoxLayout(root)

        splitter = QSplitter()
        main_layout.addWidget(splitter)
       
        # ----------------------------------------
        # --- Panel Izquierdo (Lista de notas) ---
        # ----------------------------------------
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 5, 0, 5)

        self.font_list_slider = PrecisionSlider(self, Qt.Vertical)
        self.font_list_slider.setMinimumHeight(350)
        self.font_list_slider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.font_list_slider.setRange(8, 32)
        self.font_list_slider.setValue(self.default_font_size)
        self.font_list_slider.setTickPosition(QSlider.NoTicks)
        self.font_list_slider.setFixedWidth(30)
        self.font_list_slider.valueChanged.connect(lambda val: self.update_geckonic_font_size(val, target='lista'))

        self.lcolor_btn = QPushButton("L:🎨")
        self.lcolor_btn.setFont(QFont("Noto Color Emoji", 12))
        self.lcolor_btn.setFixedSize(40, 27)
        self.lcolor_btn.setToolTip("Cambiar Color de la Etiqueta")
        self.lcolor_btn.clicked.connect(lambda: self.open_geckonic_color_dialog(target='lista'))

        left_controls_layout = QVBoxLayout()
        left_controls_layout.addStretch() 
        left_controls_layout.addWidget(QLabel("32px", alignment=Qt.AlignCenter))
        left_controls_layout.addWidget(self.font_list_slider, alignment=Qt.AlignCenter)
        left_controls_layout.addWidget(QLabel("8px", alignment=Qt.AlignCenter))
        left_controls_layout.addWidget(self.lcolor_btn, alignment=Qt.AlignRight)

        left_list = QVBoxLayout()
        left_list.setContentsMargins(5, 0, 5, 0)
        self.notes_list = QListWidget()
        self.notes_list.currentItemChanged.connect(self.on_note_changed)

        # --- Botón de Seguro / Solo Lectura ---
        self.readonly_btn = QPushButton('🔒 Activar Solo Lectura')
        self.readonly_btn.setFixedHeight(40)
        self.readonly_btn.setCheckable(True)  # Lo convierte en un switch de retención
        self.readonly_btn.setChecked(False)   # Estado inicial: Edición permitida
        self.readonly_btn.setToolTip("Bloquear Edición y Controles para Proteger GeckoNotes")
        self.readonly_btn.clicked.connect(self.toggle_readonly_mode)
        
        left_list.addWidget(self.readonly_btn)    

        # --- Botones de Gestión de Notas ---
        new_btn = QPushButton('📄 Nueva')
        new_btn.clicked.connect(self.new_note)
        new_btn.setToolTip("Crear Una nueva GeckoNote en Blanco")
        rename_btn = QPushButton('✏️ Renombrar')
        rename_btn.clicked.connect(self.rename_note)
        rename_btn.setToolTip("Cambiar el Nombre de la GeckoNote Seleccionada")
        del_btn = QPushButton('🗑️ Eliminar')
        del_btn.clicked.connect(self.delete_note)
        del_btn.setToolTip("Eliminar Permanentemente la GekcoNote Seleccionada")

        # --- 🦎🌈🚀✨ NUEVO: Botones de Portabilidad Geckónica v4.3 [UNDER TESTING 10/06/26] ---
        export_btn = QPushButton('📦 Exportar Backup')
        #export_btn.setDisabled(True)
        export_btn.clicked.connect(self.export_backup)
        export_btn.setToolTip("Comprime GeckoNotes y Configs en un tar.gz")
        import_btn = QPushButton('📥 Importar Backup')
        #import_btn.setDisabled(True)
        import_btn.clicked.connect(self.import_backup)
        import_btn.setToolTip("Restaura GeckoNotes y Configs Desde un tar.gz")

        left_list.addWidget(self.notes_list)
        left_list.addWidget(new_btn)
        left_list.addWidget(rename_btn)
        left_list.addWidget(del_btn)
        left_list.addWidget(export_btn) 
        left_list.addWidget(import_btn)

        left_layout.addLayout(left_controls_layout)
        left_layout.addLayout(left_list)

        # ------------------------------
        # --- Panel Derecho (Editor) ---
        # ------------------------------
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 5, 0, 5)

        self.editor = QPlainTextEdit()
        self.editor.textChanged.connect(self.schedule_save)
        right_layout.addWidget(self.editor, stretch=1) 

        self.font_slider = PrecisionSlider(self, Qt.Vertical)
        self.font_slider.setMinimumHeight(350)
        self.font_slider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.font_slider.setRange(8, 32)
        self.font_slider.setValue(self.default_font_size)
        self.font_slider.setTickPosition(QSlider.NoTicks)
        self.font_slider.setFixedWidth(30)
        self.font_slider.valueChanged.connect(lambda val: self.update_geckonic_font_size(val, target='editor'))
        
        self.tcolor_btn = QPushButton("T:🎨")
        self.tcolor_btn.setFont(QFont("Noto Color Emoji", 12))
        self.tcolor_btn.setFixedSize(40, 27)
        self.tcolor_btn.setToolTip("Cambiar Color del Texto")
        self.tcolor_btn.clicked.connect(lambda: self.open_geckonic_color_dialog(target='editor'))
        
        controls_layout = QVBoxLayout()
        controls_layout.addStretch() 
        controls_layout.addWidget(QLabel("32px", alignment=Qt.AlignCenter))
        controls_layout.addWidget(self.font_slider, alignment=Qt.AlignCenter)
        controls_layout.addWidget(QLabel("8px", alignment=Qt.AlignCenter))
        controls_layout.addWidget(self.tcolor_btn, alignment=Qt.AlignRight)

        right_layout.addLayout(controls_layout) 

        # -----------------------------------------------------------
        # --- Integración Final: Agregar contenedores al splitter ---
        # -----------------------------------------------------------
        splitter.addWidget(left_container)
        splitter.addWidget(right_container)
        splitter.setSizes([250, 750])

    # -------------------------------------
    # --- Seguro de Seguridad Geckónica ---
    # -------------------------------------
    def toggle_readonly_mode(self, checked):
        """
        Activa o desactiva el modo Solo Lectura en GeckoNote.
        Lógica del "🦎✅🚀 Tomahawk Safety" optimizada.
        """
        # Bloquear/Desbloquear el Editor y los Sliders principales
        self.editor.setReadOnly(checked)
        self.font_list_slider.setEnabled(not checked)
        self.font_slider.setEnabled(not checked)
        self.tcolor_btn.setEnabled(not checked)
        self.lcolor_btn.setEnabled(not checked)
        
        # Opcional: ¿Queremos que puedan cambiar de nota en modo Solo Lectura?
        # Si NO queremos que toquen nada de la lista, descomenta la línea de abajo:
        # self.notes_list.setEnabled(not checked)

        if checked:
            self.readonly_btn.setText('🔓 Activar Modo Edición')
            self.readonly_btn.setToolTip("Haz Clic para Permitir Edición de GeckoNotes")
            
            # Apagar todos los botones de acción menos el seguro
            for btn in self.findChildren(QPushButton):
                if btn != self.readonly_btn:
                    btn.setEnabled(False)
        else:
            self.readonly_btn.setText('🔒 Activar Solo Lectura')
            self.readonly_btn.setToolTip("Bloquear Edición y Controles para Proteger GeckoNotes")
            
            # Encender todos los botones del ecosistema
            for btn in self.findChildren(QPushButton):
                btn.setEnabled(True)

    # -------------------------------------------
    # --- 🦎🎨✨ GECKONIC CONFIG & PERSISTENCE ---
    # -------------------------------------------
    def get_current_note_id(self):
        current_item = self.notes_list.currentItem()
        return current_item.text() if current_item else None

    def open_geckonic_color_dialog(self, target='editor'):
        note_id = self.get_current_note_id()
        if not note_id: return
        
        if note_id not in self.notes_config:
            self.notes_config[note_id] = {}
            
        saved_color = self.notes_config[note_id].get(f'{target}_color', self.default_color)
        initial_color = QColor(saved_color)

        dialog = QColorDialog(self)
        dialog.setCurrentColor(initial_color)
        dialog.setOption(QColorDialog.DontUseNativeDialog, True)
        
        def on_color_change(color):
            if target == 'editor':
                cursor = self.editor.textCursor()
                fmt = QTextCharFormat()
                fmt.setForeground(color)
                self.editor.selectAll()
                self.editor.setCurrentCharFormat(fmt)
                self.editor.setTextCursor(cursor)
            elif target == 'lista':
                item = self.notes_list.currentItem()
                if item:
                    item.setForeground(QBrush(color))

        dialog.currentColorChanged.connect(on_color_change)
        
        if dialog.exec_() == QColorDialog.Accepted:
            self.notes_config[note_id][f'{target}_color'] = dialog.currentColor().name()
            self.save_config_to_disk()
        else:
            # Revertir si cancela
            self.apply_saved_style(note_id, target)

    def update_geckonic_font_size(self, size, target='editor'):
        note_id = self.get_current_note_id()
        if not note_id: return
        
        if note_id not in self.notes_config:
            self.notes_config[note_id] = {}
        
        self.notes_config[note_id][f'{target}_font_size'] = size

        if target == 'editor':
            font = self.editor.font()
            font.setPointSize(size)
            self.editor.setFont(font)
        elif target == 'lista':
            item = self.notes_list.currentItem()
            if item:
                """
                hechizo de silenciamiento magnético a Qt:
                « Shh, quedate pillo un segundo que el Team Cangurera está ordenando la casa, ahora te dejo seguir gritando »
                """
                self.notes_list.blockSignals(True) # Evitar Pokerror de re-entrada por cambio de UI
                font = item.font()
                font.setPointSize(size)
                item.setFont(font)
                self.notes_list.blockSignals(False)

    def apply_saved_style(self, note_id, target='editor'):
        config = self.notes_config.get(note_id, {})
        
        if target == 'lista':
            item = self.notes_list.currentItem()
            if not item: return
            
            color = config.get('lista_color', self.default_color)
            size = config.get('lista_font_size', self.default_font_size)
            
            self.notes_list.blockSignals(True)
            item.setForeground(QBrush(QColor(color)))
            font = item.font()
            font.setPointSize(size)
            item.setFont(font)
            self.notes_list.blockSignals(False)
            
            # Sincronizar el slider físico de la lista
            self.font_list_slider.blockSignals(True)
            self.font_list_slider.setValue(size)
            self.font_list_slider.blockSignals(False)
                
        elif target == 'editor':
            color = config.get('editor_color', self.default_color)
            size = config.get('editor_font_size', self.default_font_size)
            
            cursor = self.editor.textCursor()
            self.editor.selectAll()
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            self.editor.setCurrentCharFormat(fmt)
            self.editor.setTextCursor(cursor)
            
            font = self.editor.font()
            font.setPointSize(size)
            self.editor.setFont(font)
            
            # Sincronizar el slider físico del editor
            self.font_slider.blockSignals(True)
            self.font_slider.setValue(size)
            self.font_slider.blockSignals(False)

    def save_config_to_disk(self):
        """Persistencia en Disco (JSON)."""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.notes_config, f, indent=4)
        except Exception as e:
            print(f"Error guardando config: {e}")
    
    def load_config_from_disk(self):
        """Carga de configuraciones Robusta y TT (Todo Terreno)."""
        if not CONFIG_FILE.exists():
            self.notes_config = {}
            return
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notes_config = data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"⚠️ Error al leer la configuración ({e}). Usando valores por defecto.")
            self.notes_config = {}

    def refresh_all_list_styles(self):
        """Aplica Config a toda la lista de GeckoNotes."""
        self.notes_list.blockSignals(True)
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            note_id = item.text()
            config = self.notes_config.get(note_id, {})
            
            color = config.get('lista_color', self.default_color)
            size = config.get('lista_font_size', self.default_font_size)
            
            item.setForeground(QBrush(QColor(color)))
            font = item.font()
            font.setPointSize(size)
            item.setFont(font)
        self.notes_list.blockSignals(False)

    # --- Magia Geckónica del Chaman y el Team Cangurera ---
    def on_note_changed(self, current, previous):
        """Se ejecuta cada vez que cambias de nota en la lista."""
        # Si veníamos de otra nota, guardamos su tamaño modificado en disco
        if previous:
            self.save_config_to_disk()
        
        if current:
            note_id = current.text()
            if note_id not in self.notes_config:
                self.notes_config[note_id] = {
                    'lista_font_size': self.default_font_size, 'lista_color': self.default_color,
                    'editor_font_size': self.default_font_size, 'editor_color': self.default_color
                }   
            # Cargar estilo guardado para ESTA nota
            self.apply_saved_style(note_id, target='lista')
            # Cargar el contenido de la nota en el editor
            self.open_note(note_id)
            # Si el editor también tiene estilo por nota, aplicarlo
            self.apply_saved_style(note_id, target='editor')

    # ----------------------------------------
    # --- 🦎⚡✨ GeckoNotes Logic Management ---
    # ----------------------------------------
    def load_notes(self):
        self.notes_list.blockSignals(True)
        self.notes_list.clear()
        for f in sorted(NOTES_DIR.iterdir()):
            if f.is_file() and f.name != 'gecko_config.json':
                self.notes_list.addItem(f.name)
        self.notes_list.blockSignals(False)
        self.refresh_all_list_styles()

    def open_note(self, name):
        if not name: return
        self.current_file = NOTES_DIR / name
        self.editor.blockSignals(True)
        try:
            self.editor.setPlainText(self.current_file.read_text(encoding='utf-8', errors='ignore'))
        except Exception as e:
            print(f"Error abriendo nota: {e}")
        self.editor.blockSignals(False)

    def schedule_save(self):
        self.save_timer.start(1000)

    def save_note(self):
        # 🚀🦎🔥 Solo guarda si hay un archivo asignado Y el usuario no lo borró en este milisegundo
        if self.current_file and self.current_file.parent.exists():
            try:
                self.current_file.write_text(self.editor.toPlainText(), encoding='utf-8')
            except Exception as e:
                print(f"Error salvando nota: {e}")

    def new_note(self):
        name, ok = QInputDialog.getText(self, 'Nueva nota', 'Nombre:')
        if ok and name:
            path = NOTES_DIR / name
            path.touch(exist_ok=True)
            self.load_notes()
            # Buscar el ítem recién creado y seleccionarlo
            items = self.notes_list.findItems(name, Qt.MatchExactly)
            if items:
                self.notes_list.setCurrentItem(items[0])

    def rename_note(self):
        if not self.current_file: return
        old_name = self.current_file.name
        name, ok = QInputDialog.getText(self, 'Renombrar', 'Nuevo nombre:', text=old_name)
        if ok and name and name != old_name:
            new_path = NOTES_DIR / name
            self.current_file.rename(new_path)
            
            # Migración de metadatos Geckónicos (Persistencia viva)
            if old_name in self.notes_config:
                self.notes_config[name] = self.notes_config.pop(old_name)
                self.save_config_to_disk()
                
            self.load_notes()
            items = self.notes_list.findItems(name, Qt.MatchExactly)
            if items:
                self.notes_list.setCurrentItem(items[0])

    def delete_note(self):
        if not self.current_file: return
        name = self.current_file.name
        if QMessageBox.question(self, 'Eliminar', f'¿Eliminar nota "{name}"?') == QMessageBox.Yes:
            """
            freno de mano que acuta junto al hechizo de silenciamiento magnético a Qt
            « tranquilo que el Team Cangurera sigue ordenando el caos »
            """
            self.save_timer.stop() # Frena el timer antes de tocar el editor para evitar que agende un guardado fantasma
            self.current_file.unlink() # Borrar el archivo real del disco
            self.current_file = None # Romper la brújula en memoria: ya no hay archivo actual

            # Limpieza de metadatos zombies
            if name in self.notes_config:
                self.notes_config.pop(name)
                self.save_config_to_disk()

            self.load_notes()
            self.editor.clear()

    # --------------------------------------------------------
    # --- 🦎📦 La Lógica del Backup: Los Métodos Chamánicos ---
    # --------------------------------------------------------
    # Regla de oro del Team Cangurera:
    # "Si no lo probaste en desarrollo y no tienes un backup, no lo toques en producción."
    def export_backup(self):
        """Comprime toda la carpeta de notas y la config en un archivo .tar.gz elegido por el usuario."""
        # Aseguramos que los últimos cambios visuales estén impactados en disco antes del viaje
        self.save_config_to_disk()
        if self.current_file:
            self.save_note()

        options = QFileDialog.Options()
        # Nombre por defecto hermosamente Geckónico 
        default_name = os.path.join(Path.home(), "GeckoNotes.bckp.tar.gz")
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "GeckoNotes Backup - Guardar Archivo", default_name,
            "Archivos Comprimidos (*.tar.gz)", options=options
        )
        
        if filepath:
            try:
                # Magia de compresión nativa Linux
                with tarfile.open(filepath, "w:gz") as tar:
                    # Agregamos toda la carpeta de notas completa, guardando los nombres relativos
                    tar.add(NOTES_DIR, arcname=NOTES_DIR.name)
                
                QMessageBox.information(self, "Backup Exitoso", f"¡Totalidad empaquetada!\nGuardado en: {os.path.basename(filepath)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear el backup:\n{e}")

    def import_backup(self):
        """Lee un archivo .tar.gz y extrae las notas y la config, fusionando o reemplazando con cuidado."""
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(
            self, "GeckoNotes Backup - Seleccionar Archivo", str(Path.home()),
            "Archivos Comprimidos (*.tar.gz)", options=options
        )
        # Confirmación "Esto combinará las notas actuales y sobreescribirá las configuraciones visuales."
        if filepath:
            confirm = QMessageBox.question(
                self, "Confirmar Restauración", 
                "¿Deseas importar este backup?\n\n" 
                "⚠️ Ten en cuenta:\n"
                "• Las notas con el mismo nombre se SOBRESCRIBIRÁN (se perderán los cambios recientes).\n"
                "• Las notas del backup que no tienes se AGREGARÁN.\n"
                "• Tus notas actuales que NO están en el backup se CONSERVARÁN.\n"
                "• Se restaurarán los colores y tamaños guardados.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                try:
                    # Frenamos señales y timers para evitar que Qt tire eventos fantasmas durante la inyección de archivos
                    self.save_timer.stop()
                    self.notes_list.blockSignals(True)
                    self.editor.blockSignals(True)
                    
                    with tarfile.open(filepath, "r:gz") as tar:
                        # Extraemos el contenido. Como se guardó con arcname=NOTES_DIR.name, 
                        # el tar contiene una carpeta interna llamada 'Notes'. Extraemos en el directorio padre.
                        tar.extractall(path=NOTES_DIR.parent)
                    
                    # Volvemos a levantar la config inyectada y las notas del plano físico
                    self.load_config_from_disk()
                    self.load_notes()
                    self.refresh_all_list_styles()
                    
                    # Reset del estado del editor por seguridad
                    self.current_file = None
                    self.editor.clear()
                    
                    # Seleccionar la primera nota si hay para dejar la UI armada
                    if self.notes_list.count() > 0:
                        self.notes_list.setCurrentRow(0)
                        
                    QMessageBox.information(self, "Restauración Exitosa", "¡Notas y configuraciones sincronizadas con el multiverso!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Fallo en la restauración cuántica:\n{e}")
                finally:
                    # Devolvemos el habla a los widgets
                    self.notes_list.blockSignals(False)
                    self.editor.blockSignals(False)

    # ------------------------
    # --- Salida Geckónica ---
    # ------------------------ 
    def closeEvent(self, event):
        """ 🚀🦎 Asegura que el Team Cangurera salve el mapa mental antes de apagar las luces."""
        self.save_config_to_disk()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    win = GeckoNotes()
    win.show()
    sys.exit(app.exec_())