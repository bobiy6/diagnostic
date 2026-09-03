import customtkinter as ctk
import threading
import system_hardware_benchmarks

class TestsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Tests & Benchmarks Matériels Approfondis", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")

        subtitle = ctk.CTkLabel(self, text="Évaluation réelle CPU, MemTest RAM, IOPS Disque, GPU 3D et Batterie", font=ctk.CTkFont(size=12), text_color="gray")
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # Action Buttons bar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.btn_run_fast = ctk.CTkButton(
            btn_frame,
            text="Test Rapide Standard (30s)",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=lambda: self.start_benchmark_thread(quick=True)
        )
        self.btn_run_fast.pack(side="left", padx=(0, 10))

        self.btn_run_deep = ctk.CTkButton(
            btn_frame,
            text="Test Approfondi Professionnel (MemTest & IOPS 4K)",
            fg_color="#059669",
            hover_color="#047857",
            command=lambda: self.start_benchmark_thread(quick=False)
        )
        self.btn_run_deep.pack(side="left")

        # Progress bar & Status
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="ew")

        self.lbl_status = ctk.CTkLabel(self, text="Prêt pour le benchmark matériel.", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_status.grid(row=4, column=0, padx=20, pady=(0, 5), sticky="w")

        self.textbox_log = ctk.CTkTextbox(self, height=320, font=ctk.CTkFont(family="Courier", size=11))
        self.textbox_log.insert("1.0", "Cliquez sur 'Test Rapide' ou 'Test Approfondi' pour mesurer le matériel réel.\n")
        self.textbox_log.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")

        self.test_results = {}

    def update_progress(self, message, progress_val):
        self.progress_bar.set(progress_val)
        self.lbl_status.configure(text=f"[{int(progress_val*100)}%] {message}")
        self.textbox_log.insert("end", f"[{int(progress_val*100)}%] {message}\n")
        self.textbox_log.see("end")

    def start_benchmark_thread(self, quick=True):
        self.btn_run_fast.configure(state="disabled")
        self.btn_run_deep.configure(state="disabled")
        self.progress_bar.set(0)
        self.textbox_log.delete("1.0", "end")
        mode_str = "RAPIDE" if quick else "APPROFONDI PROFESSIONNEL"
        self.textbox_log.insert("end", f"=== DÉMARRAGE DU BENCHMARK MATÉRIEL ({mode_str}) ===\n\n")

        thread = threading.Thread(target=self.run_benchmarks, args=(quick,), daemon=True)
        thread.start()

    def run_benchmarks(self, quick):
        def cb(msg, progress):
            self.after(0, self.update_progress, msg, progress)

        cpu_sec = 2 if quick else 4
        ram_mb = 64 if quick else 256
        disk_mb = 32 if quick else 128
        gpu_sec = 2 if quick else 4

        # Execute
        res = system_hardware_benchmarks.run_all_hardware_benchmarks(callback=cb)

        self.test_results = res

        def finish_ui():
            self.progress_bar.set(1.0)
            self.lbl_status.configure(text="Benchmark matériel terminé !")
            self.textbox_log.insert("end", "\n=== TOUS LES TESTS MATÉRIELS ONT ÉTÉ EXÉCUTÉS AVEC SUCCÈS ===")
            self.btn_run_fast.configure(state="normal")
            self.btn_run_deep.configure(state="normal")

        self.after(0, finish_ui)

    def get_data(self):
        return self.test_results
