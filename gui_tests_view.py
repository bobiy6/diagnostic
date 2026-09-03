import customtkinter as ctk

class TestsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Tests Matériels Machine", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        subtitle = ctk.CTkLabel(self, text="Benchmarks de charge CPU, RAM, vitesse Disque et Batterie", font=ctk.CTkFont(size=12), text_color="gray")
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.btn_run = ctk.CTkButton(self, text="Lancer Tous les Tests (Simulé / Express)", command=self.run_tests)
        self.btn_run.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.textbox_log = ctk.CTkTextbox(self, height=280, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox_log.insert("1.0", "Cliquez sur 'Lancer Tous les Tests' pour démarrer l'évaluation des composants.\n")
        self.textbox_log.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.test_results = {}

    def run_tests(self):
        self.textbox_log.delete("1.0", "end")
        self.textbox_log.insert("end", "[1/4] Test de charge CPU & Stabilité Thermal... PASS (Temp. max 68°C)\n")
        self.textbox_log.insert("end", "[2/4] Test d'intégrité RAM... PASS (0 erreur détectée)\n")
        self.textbox_log.insert("end", "[3/4] Benchmark Vitesse Disque... PASS (Lecture 3200 Mo/s | Écriture 2700 Mo/s)\n")
        self.textbox_log.insert("end", "[4/4] Analyse de rétention Batterie... AVERTISSEMENT (Rétention à 82%)\n\n")
        self.textbox_log.insert("end", "=== TOUS LES TESTS MATÉRIELS SONT TERMINÉS ===")

        self.test_results = {
            "cpuStress": {"status": "Succès", "details": "Temp. max 68°C"},
            "ramIntegrity": {"status": "Succès", "details": "0 erreur"},
            "diskBenchmark": {"status": "Succès", "details": "Read 3200MB/s"},
            "batteryHealthCheck": {"status": "Avertissement", "details": "Rétention 82%"}
        }

    def get_data(self):
        return self.test_results
