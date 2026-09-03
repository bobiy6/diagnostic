import customtkinter as ctk
import threading
import system_hardware_benchmarks

class TestsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Tests & Benchmarks Matériels Réels", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        subtitle = ctk.CTkLabel(self, text="Mesure réelle de la vitesse CPU, bande passante RAM, I/O Disque et usure Batterie", font=ctk.CTkFont(size=12), text_color="gray")
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.btn_run = ctk.CTkButton(self, text="Lancer les Vrais Tests Matériels", fg_color="#2563EB", hover_color="#1D4ED8", command=self.start_benchmark_thread)
        self.btn_run.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.textbox_log = ctk.CTkTextbox(self, height=360, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox_log.insert("1.0", "Cliquez sur 'Lancer les Vrais Tests Matériels' pour exécuter les benchmarks en temps réel.\n")
        self.textbox_log.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.test_results = {}

    def start_benchmark_thread(self):
        self.btn_run.configure(state="disabled", text="Benchmark en cours...")
        self.textbox_log.delete("1.0", "end")
        self.textbox_log.insert("end", "=== DÉMARRAGE DES TESTS BENCHMARK MATÉRIELS RÉELS ===\n\n")

        thread = threading.Thread(target=self.run_benchmarks, daemon=True)
        thread.start()

    def run_benchmarks(self):
        # 1. CPU
        self.textbox_log.insert("end", "[1/4] Test de charge CPU multi-threaded en cours...\n")
        cpu_res = system_hardware_benchmarks.run_cpu_benchmark(duration_sec=2)
        self.textbox_log.insert("end", f"     -> Débit calculs: {cpu_res['ops_per_sec']} ({cpu_res['threads_used']} threads)\n")
        self.textbox_log.insert("end", f"     -> Évaluation CPU: {cpu_res['rating']}\n\n")

        # 2. RAM
        self.textbox_log.insert("end", "[2/4] Test d'allocation & bande passante RAM en cours...\n")
        ram_res = system_hardware_benchmarks.run_ram_benchmark(block_mb=64)
        self.textbox_log.insert("end", f"     -> Vitesse Écriture: {ram_res['write_speed']} | Lecture: {ram_res['read_speed']}\n")
        self.textbox_log.insert("end", f"     -> Évaluation RAM: {ram_res['rating']}\n\n")

        # 3. DISK
        self.textbox_log.insert("end", "[3/4] Test réel E/S Disque (Écriture & Lecture 32 Mo) en cours...\n")
        disk_res = system_hardware_benchmarks.run_disk_benchmark(test_mb=32)
        self.textbox_log.insert("end", f"     -> Type détecté: {disk_res['disk_type']}\n")
        self.textbox_log.insert("end", f"     -> Débit Écriture: {disk_res['write_speed']} | Lecture: {disk_res['read_speed']}\n")
        self.textbox_log.insert("end", f"     -> État Santé Disque: {disk_res['health']} ({disk_res['rating']})\n\n")

        # 4. BATTERY
        self.textbox_log.insert("end", "[4/4] Analyse d'usure et rétention Batterie en cours...\n")
        batt_res = system_hardware_benchmarks.run_battery_benchmark()
        self.textbox_log.insert("end", f"     -> Niveau: {batt_res['percent']} | Rétention/Usure: {batt_res['estimated_wear']}\n")
        self.textbox_log.insert("end", f"     -> État de Santé Batterie: {batt_res['health']} ({batt_res['lifespan_state']})\n\n")

        self.textbox_log.insert("end", "=== TOUS LES TESTS MATÉRIELS SONT TERMINÉS ===")

        self.test_results = {
            "cpu": cpu_res,
            "ram": ram_res,
            "disk": disk_res,
            "battery": batt_res
        }

        self.btn_run.configure(state="normal", text="Lancer les Vrais Tests Matériels")

    def get_data(self):
        return self.test_results
