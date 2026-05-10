import os
import sys

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def resource_path(relative_path):

    if getattr(sys, "frozen", False):

        base_path = Path(sys.executable).parent

    else:

        base_path = Path(__file__).resolve().parent

    return base_path / relative_path


from pathlib import Path

BASE_DIR = (
    Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)

os.chdir(BASE_DIR)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import sqlite3
import hashlib
import re
import logging
import json
import psutil

from langdetect import detect
from lxml import etree

from transformers import (
    M2M100ForConditionalGeneration,
    M2M100Tokenizer
)

from ctranslate2 import Translator
from ctranslate2.converters import TransformersConverter


(BASE_DIR / "logs").mkdir(exist_ok=True)
(BASE_DIR / "cache").mkdir(exist_ok=True)
(BASE_DIR / "input").mkdir(exist_ok=True)
(BASE_DIR / "output").mkdir(exist_ok=True)
(BASE_DIR / "models").mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(BASE_DIR / "logs" / "app.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)


class CacheDB:

    def __init__(self):

        self.conn = sqlite3.connect(
            "cache/translation_cache.db"
        )

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS translations (
                text_hash TEXT PRIMARY KEY,
                translated TEXT
            )
            """
        )

    def _hash(self, text):

        return hashlib.sha1(
            text.encode("utf-8")
        ).hexdigest()

    def get(self, text):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT translated FROM translations WHERE text_hash=?",
            (self._hash(text),)
        )

        row = cursor.fetchone()

        return row[0] if row else None

    def save(self, text, translated):

        self.conn.execute(
            """
            INSERT OR REPLACE INTO translations
            VALUES (?, ?)
            """,
            (
                self._hash(text),
                translated
            )
        )

        self.conn.commit()


class TranslationEngine:

    def __init__(self):

        self.model_name = (
            "facebook/m2m100_418M"
        )

        self.models_dir = Path("models")

        self.original_dir = (
            self.models_dir / "m2m100_original"
        )

        self.ct2_dir = (
            self.models_dir / "m2m100_ct2"
        )

        self.models_dir.mkdir(exist_ok=True)

        self.tokenizer = (
            M2M100Tokenizer.from_pretrained(
                self.model_name
            )
        )

        self.tokenizer.src_lang = "en"

        if not self.original_dir.exists():

            model = (
                M2M100ForConditionalGeneration
                .from_pretrained(self.model_name)
            )

            model.save_pretrained(
                self.original_dir
            )

            self.tokenizer.save_pretrained(
                self.original_dir
            )

        if not self.ct2_dir.exists():

            converter = TransformersConverter(
                str(self.original_dir)
            )

            converter.convert(
                str(self.ct2_dir),
                quantization="int8"
            )

        self.translator = Translator(
            str(self.ct2_dir),
            device="cpu"
        )

    def translate(self, text):

        ids = self.tokenizer.encode(text)

        tokens = (
            self.tokenizer
            .convert_ids_to_tokens(ids)
        )

        result = (
            self.translator.translate_batch(
                [tokens],
                target_prefix=[["__es__"]]
            )[0]
        )

        translated = self.tokenizer.decode(
            self.tokenizer.convert_tokens_to_ids(
                result.hypotheses[0]
            ),
            skip_special_tokens=True
        )

        return translated


class App:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "TraductorData LaunchBox v1.0"
        )

        self.root.geometry("1000x760")

        self.root.configure(bg="#050505")

        self.input_var = tk.StringVar(
            value="input"
        )

        self.output_var = tk.StringVar(
            value="output"
        )

        self.profile_var = tk.StringVar(
            value="BALANCED"
        )

        self.cpu_values = []
        self.ram_values = []

        self.max_cpu = 0
        self.max_ram = 0

        self.abort_requested = False
        

        # cargar diccionario gamer
        try:
            with open("gamer_dictionary.json", "r", encoding="utf-8") as f:
                self.gamer_dictionary = json.load(f)
        except:
            self.gamer_dictionary = {}


        self.build_ui()

    def build_ui(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "TFrame",
            background="#050505"
        )

        style.configure(
            "TLabel",
            background="#050505",
            foreground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Title.TLabel",
            background="#050505",
            foreground="#00ff99",
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Green.Horizontal.TProgressbar",
            troughcolor="#111111",
            background="#00ff99",
            bordercolor="#222222",
            lightcolor="#00ff99",
            darkcolor="#00cc77"
        )

        top = ttk.Frame(self.root)
        top.pack(fill="x", padx=15, pady=15)

        ttk.Label(
            top,
            text="TraductorData LaunchBox",
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,15))

        ttk.Label(
            top,
            text="Carpeta Input:"
        ).grid(row=1, column=0, sticky="w")

        ttk.Entry(
            top,
            textvariable=self.input_var,
            width=70
        ).grid(row=1, column=1)

        ttk.Button(
            top,
            text="Seleccionar",
            command=self.select_input
        ).grid(row=1, column=2, padx=5)

        ttk.Label(
            top,
            text="Carpeta Output:"
        ).grid(row=2, column=0, sticky="w", pady=(10,0))

        ttk.Entry(
            top,
            textvariable=self.output_var,
            width=70
        ).grid(row=2, column=1, pady=(10,0))

        ttk.Button(
            top,
            text="Seleccionar",
            command=self.select_output
        ).grid(row=2, column=2, padx=5, pady=(10,0))

        ttk.Label(
            top,
            text="Perfil:"
        ).grid(row=3, column=0, sticky="w", pady=(10,0))

        ttk.Combobox(
            top,
            textvariable=self.profile_var,
            values=["LOW","BALANCED","HIGH"],
            state="readonly",
            width=20
        ).grid(row=3, column=1, sticky="w", pady=(10,0))

        self.progress = ttk.Progressbar(
            self.root,
            mode="determinate",
            style="Green.Horizontal.TProgressbar"
        )

        self.progress.pack(
            fill="x",
            padx=15,
            pady=(15,5)
        )

        self.progress_label = tk.Label(
            self.root,
            text="0 / 0",
            bg="#050505",
            fg="white",
            font=("Segoe UI", 9)
        )

        self.progress_label.pack()

        self.stats_label = tk.Label(
            self.root,
            text="RAM actual: 0 GB | CPU actual: 0%",
            bg="#050505",
            fg="white",
            font=("Segoe UI", 10)
        )

        self.stats_label.pack(anchor="w", padx=15, pady=(10,0))

        self.avg_label = tk.Label(
            self.root,
            text="RAM promedio: 0 GB | CPU promedio: 0%",
            bg="#050505",
            fg="white",
            font=("Segoe UI", 10)
        )

        self.avg_label.pack(anchor="w", padx=15)

        self.max_label = tk.Label(
            self.root,
            text="RAM máxima: 0 GB | CPU máximo: 0%",
            bg="#050505",
            fg="white",
            font=("Segoe UI", 10)
        )

        self.max_label.pack(anchor="w", padx=15)

        self.start_button = tk.Button(
            self.root,
            text="INICIAR TRADUCCIÓN",
            bg="#00aa66",
            fg="white",
            activebackground="#00cc77",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=8,
            borderwidth=0,
            command=self.start
        )

        self.start_button.pack(pady=15)

        self.abort_button = tk.Button(
            self.root,
            text="ABORTAR",
            bg="#aa2222",
            fg="white",
            activebackground="#cc3333",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            borderwidth=0,
            command=self.abort_process
        )

        self.abort_button.pack(pady=(0,15))


        self.console = tk.Text(
            self.root,
            bg="#000000",
            fg="#00ff99",
            insertbackground="white",
            font=("Consolas", 10),
            height=24,
            borderwidth=1
        )

        self.console.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.update_stats()

    def update_stats(self):

        process = psutil.Process()
        ram = process.memory_info().rss / (1024**3)

        cpu = psutil.Process().cpu_percent(interval=0.1)

        self.cpu_values.append(cpu)
        self.ram_values.append(ram)

        avg_cpu = sum(self.cpu_values) / len(self.cpu_values)
        avg_ram = sum(self.ram_values) / len(self.ram_values)

        self.max_cpu = max(self.max_cpu, cpu)
        self.max_ram = max(self.max_ram, ram)

        self.stats_label.config(
            text=f"RAM actual: {ram:.2f} GB | CPU actual: {cpu:.1f}%"
        )

        self.avg_label.config(
            text=f"RAM promedio: {avg_ram:.2f} GB | CPU promedio: {avg_cpu:.1f}%"
        )

        self.max_label.config(
            text=f"RAM máxima: {self.max_ram:.2f} GB | CPU máximo: {self.max_cpu:.1f}%"
        )

        self.root.after(1000, self.update_stats)

    def log(self, text):

        self.console.insert(
            "end",
            text + "\n"
        )

        self.console.see("end")

        logging.info(text)

        self.root.update_idletasks()

    def select_input(self):

        path = filedialog.askdirectory()

        if path:
            self.input_var.set(path)

    def select_output(self):

        path = filedialog.askdirectory()

        if path:
            self.output_var.set(path)

    
    def abort_process(self):

        self.abort_requested = True

        self.progress.stop()

        self.progress["value"] = 0
        self.progress["maximum"] = 1

        self.progress_label.config(
            text="0 / 0"
        )

        self.root.update_idletasks()

        self.progress["value"] = 0
        self.progress["maximum"] = 1
        self.progress_label.config(text="0 / 0")

        self.log("")
        self.log("===== ABORTADO POR USUARIO =====")

    def start(self):

        # Reset visual COMPLETO antes de iniciar
        self.abort_requested = False

        self.progress.stop()

        self.progress["value"] = 0
        self.progress["maximum"] = 1

        self.progress_label.config(
            text="0 / 0"
        )

        self.root.update_idletasks()

        thread = threading.Thread(
            target=self.run_translation
        )

        thread.start()

    
    def apply_gamer_dictionary(self, text):

        for original, replacement in self.gamer_dictionary.items():

            text = re.sub(
                re.escape(original),
                replacement,
                text,
                flags=re.IGNORECASE
            )

        return text


    def split_sentences(self, text):

        return re.split(
            r'(?<=[.!?])\s+',
            text
        )

    def fix_translation(self, text):

        fixes = {
            "tabletop": "de sobremesa",
            "modo standby": "modo de espera",
            "fue inmediatamente sucediendo por":
                "fue sucedido inmediatamente por",
            "handheld console": "consola portátil",
            "home console": "consola doméstica",
            "backward compatible": "retrocompatible",
            "optical disc": "disco óptico",
            "cartridges": "cartuchos",
            "portable system": "consola portátil",
            "maintenance system": "consola portátil",
            "dominación de Nintendo": "dominio de Nintendo",
            "liberación occidental": "lanzamiento occidental",
            "curta vida": "vida corta",
            "la manzana fue anunciada": "la consola fue anunciada",
            "fue logrado por": "fue sucedido por",
            "sistema de mantenimiento": "consola portátil",
            "liberación": "lanzamiento",
            "en el camino": "en modo portátil",
            "fue lanzado": "fue lanzada",
            "fue sucedido": "fue sucedida",
            "disco ópticos": "discos ópticos",
            "portable de consola": "consola portátil",
            "dominación portátil": "dominio portátil",
            "fue inmediatamente conseguido por": "fue reemplazada inmediatamente por",
            "fue exitosa por": "fue sucedida por",
            "pantallas trabajando en tandem": "pantallas funcionando en conjunto",
            "modo dock": "modo acoplado",
            "microphone": "micrófono",
            "tandem": "conjunto",
            "la consola fue lanzado": "la consola fue lanzada",
            "el sistema fue lanzado": "el sistema fue lanzado",
            "pantalla de visualización": "pantalla",
            "vida corta": "corto ciclo de vida",
            "logró el modelo": "reemplazó el modelo",
            "fue suspendida": "fue descontinuada",
            "fue suspendido": "fue descontinuado",
            "mercados mundiales": "mercados internacionales",
            "la sucesora": "su sucesora",
            "console portátil": "consola portátil"
        }

        for wrong, correct in fixes.items():
            text = text.replace(
                wrong,
                correct
            )

        text = re.sub(
            r'(?<!US)\$\s?([0-9]+(?:\.[0-9]+)?)',
            r'US$\1',
            text
        )

        return text

    def run_translation(self):

        # Reset estadísticas por ejecución
        self.cpu_values = []
        self.ram_values = []
        self.max_cpu = 0
        self.max_ram = 0


        
        profile = self.profile_var.get()

        if profile == "LOW":
            self.batch_size = 1
            self.worker_threads = 1
            self.inter_threads = 1
            self.sleep_delay = 0.02

        elif profile == "HIGH":
            self.batch_size = 16
            self.worker_threads = 8
            self.inter_threads = 6
            self.sleep_delay = 0

        else:
            self.batch_size = 4
            self.worker_threads = 2
            self.inter_threads = 2
            self.sleep_delay = 0.005

        self.log(f"Perfil activo: {profile}")
        self.log(f"Batch size: {self.batch_size}")
        self.log(f"Workers: {self.worker_threads}")
        self.log(f"Inter threads: {self.inter_threads}")

        self.abort_requested = False

        self.progress["value"] = 0
        self.progress["maximum"] = 1
        self.progress_label.config(text="0 / 0")

        self.cpu_values = []
        self.ram_values = []
        self.max_cpu = 0
        self.max_ram = 0

        start_time = time.time()

        self.log("Inicializando motor IA...")

        try:

            translator = TranslationEngine()

        except Exception as e:

            self.log(f"ERROR cargando IA: {e}")

            return

        db = CacheDB()

        input_folder = Path(
            self.input_var.get()
        )

        output_folder = Path(
            self.output_var.get()
        )

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        xml_files = list(
            input_folder.glob("*.xml")
        )

        if not xml_files:

            self.log("No se encontraron XML")

            return

        total_notes = 0

        for xml in xml_files:

            tree = etree.parse(str(xml))

            notes = tree.xpath("//Notes")

            total_notes += len(notes)

        self.progress["maximum"] = max(total_notes,1)

        processed = 0
        translated_count = 0
        cache_hits = 0

        self.progress["value"] = 0
        self.progress_label.config(text="0 / 0")

        for xml in xml_files:

            self.log(
                f"Procesando: {xml.name}"
            )

            try:

                tree = etree.parse(str(xml))

                notes = tree.xpath("//Notes")

                for note in notes:

                    if self.abort_requested:
                        self.log("Proceso detenido.")
                        return

                    processed += 1

                    self.progress["value"] = processed

                    self.progress_label.config(
                        text=f"{processed} / {total_notes}"
                    )

                    original = note.text

                    if not original:
                        continue

                    original = re.sub(
                        r'\s+',
                        ' ',
                        original
                    ).strip()

                    original = self.apply_gamer_dictionary(
                        original
                    )

                    try:

                        language = detect(original)

                    except:

                        continue

                    if language != "en":
                        continue

                    cached = db.get(original)

                    if cached:

                        note.text = cached

                        cache_hits += 1

                        continue

                    translated_parts = []

                    sentences = self.split_sentences(
                        original
                    )

                    for sentence in sentences:

                        if self.sleep_delay:
                            time.sleep(self.sleep_delay)

                        sentence = sentence.strip()

                        if not sentence:
                            continue

                        translated = (
                            translator.translate(
                                sentence
                            )
                        )

                        translated_parts.append(
                            translated
                        )

                    final = " ".join(
                        translated_parts
                    )

                    final = self.fix_translation(
                        final
                    )

                    note.text = final

                    db.save(
                        original,
                        final
                    )

                    translated_count += 1

                output_file = (
                    output_folder / xml.name
                )

                tree.write(
                    str(output_file),
                    pretty_print=True,
                    xml_declaration=True,
                    encoding="utf-8"
                )

                self.log(
                    f"Guardado: {output_file}"
                )

            except Exception as e:

                self.log(
                    f"ERROR en {xml.name}: {e}"
                )

        elapsed = round(
            time.time() - start_time,
            2
        )

        self.log("")
        self.log("===== COMPLETADO =====")
        self.log(
            f"Traducidos: {translated_count}"
        )
        self.log(
            f"Cache hits: {cache_hits}"
        )
        self.log(
            f"Tiempo total: {elapsed} segundos"
        )

        messagebox.showinfo(
            "Completado",
            "Proceso terminado."
        )


root = tk.Tk()

app = App(root)

root.mainloop()
