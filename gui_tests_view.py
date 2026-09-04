import customtkinter as ctk
import threading
import system_hardware_benchmarks

class TestsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Mister Genius SA - Benchmarks & Test de Piétinement 25 Min",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#0099DA"
        )
        title.grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Tests séquentiels composant par composant (CPU -> RAM -> Disque -> GPU -> Batterie)",
            font=ctk.CTkFont(size=12),
            text_color="#64748B"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # Action Buttons bar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.btn_run_fast = ctk.CTkButton(
            btn_frame,
            text="Test Séquentiel Rapide (30s)",
            fg_color="#334155",
            hover_color="#475569",
            command=lambda: self.start_benchmark_thread(quick=True)
        )
        self.btn_run_fast.pack(side="left", padx=(0, 10))

        self.btn_run_deep = ctk.CTkButton(
            btn_frame,
            text="TEST SÉQUENTIEL DE PIÉTINEMENT 25 MIN (5 x 5 min)",
            fg_color="#0099DA",
            hover_color="#0072CE",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.start_benchmark_thread(quick=False)
        )
        self.btn_run_deep.pack(side="left")

        # Component Progress & Error Display
        prog_frame = ctk.CTkFrame(self, fg_color="#0F172A", corner_radius=10)
        prog_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        prog_frame.grid_columnconfigure(0, weight=1)

        self.lbl_stage = ctk.CTkLabel(
            prog_frame,
            text="SÉLECTIONNEZ UN TEST POUR DÉMARRER",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#0099DA"
        )
        self.lbl_stage.grid(row=0, column=0, padx=15, pady=(10, 2), sticky="w")

        self.progress_bar = ctk.CTkProgressBar(prog_frame, progress_color="#0099DA", height=14)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        self.lbl_errors_count = ctk.CTkLabel(
            prog_frame,
            text="Erreurs Détectées : 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#10B981"
        )
        self.lbl_errors_count.grid(row=2, column=0, padx=15, pady=(2, 10), sticky="w")

        # Terminal Log Output
        self.textbox_log = ctk.CTkTextbox(self, height=290, font=ctk.CTkFont(family="Courier", size=11))
        self.textbox_log.insert("1.0", "Exécution séquentielle : chaque composant est testé individuellement de 0% à 100%.\n")
        self.textbox_log.grid(row=4, column=0, padx=20, pady=5, sticky="nsew")

        self.test_results = {}
        self.last_log_message = ""

    def update_single_progress(self, message, pct):
        self.progress_bar.set(pct)
        self.lbl_stage.configure(text=f"[{int(pct*100)}%] {message}")
        if pct >= 1.0 or self.last_log_message != message:
            self.last_log_message = message
            self.textbox_log.insert("end", f"[{int(pct*100)}%] {message}\n")
            self.textbox_log.see("end")

    def update_stage_progress(self, stage_name, stage_pct, global_pct, errors_count):
        self.progress_bar.set(global_pct)
        self.lbl_stage.configure(text=f"[{int(global_pct*100)}%] {stage_name} ({int(stage_pct*100)}%)")
        if errors_count > 0:
            self.lbl_errors_count.configure(text=f"Erreurs Détectées : {errors_count} (ANOMALIE)", text_color="#EF4444")
        else:
            self.lbl_errors_count.configure(text="Erreurs Détectées : 0 (STABLE)", text_color="#10B981")

        if self.last_log_message != stage_name or global_pct >= 1.0:
            self.last_log_message = stage_name
            self.textbox_log.insert("end", f"[{int(global_pct*100)}%] {stage_name}\n")
            self.textbox_log.see("end")

    def start_benchmark_thread(self, quick=True):
        self.btn_run_fast.configure(state="disabled")
        self.btn_run_deep.configure(state="disabled")
        self.progress_bar.set(0)
        self.textbox_log.delete("1.0", "end")
        self.lbl_errors_count.configure(text="Erreurs Détectées : 0", text_color="#10B981")
        self.last_log_message = ""

        mode_str = "RAPIDE SÉQUENTIEL" if quick else "TEST SÉQUENTIEL 25 MINUTES (5 X 5 MIN)"
        self.textbox_log.insert("end", f"=== DÉMARRAGE DES TESTS COMPOSANT PAR COMPOSANT ({mode_str}) ===\n\n")

        thread = threading.Thread(target=self.run_benchmarks, args=(quick,), daemon=True)
        thread.start()

    def run_benchmarks(self, quick):
        try:
            if quick:
                def cb(msg, pct):
                    self.after(0, self.update_single_progress, msg, pct)
                res = system_hardware_benchmarks.run_all_hardware_benchmarks(quick=True, callback=cb)
            else:
                def stage_cb(stage_name, st_pct, glob_pct, errs):
                    self.after(0, self.update_stage_progress, stage_name, st_pct, glob_pct, errs)
                res = system_hardware_benchmarks.run_all_hardware_benchmarks(quick=False, stage_callback=stage_cb)

            self.test_results = res
        except Exception as err:
            self.after(0, lambda: self.textbox_log.insert("end", f"\nANOMALIE EN COURS DE TEST : {str(err)}\n"))
        finally:
            def finish_ui():
                self.progress_bar.set(1.0)
                self.lbl_stage.configure(text="TESTS SÉQUENTIELS TERMINÉS AVEC SUCCÈS !")
                self.textbox_log.insert("end", "\n=== TOUS LES TESTS MATÉRIELS ONT ÉTÉ EXÉCUTÉS AVEC SUCCÈS ===")
                self.btn_run_fast.configure(state="normal")
                self.btn_run_deep.configure(state="normal")

            self.after(0, finish_ui)

    def get_data(self):
        return self.test_results
