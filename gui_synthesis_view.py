import customtkinter as ctk
import pdf_report

class SynthesisView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        # TOP BAR
        header_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1F2937")
        header_frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            header_frame,
            text="📊  SYNTHÈSE GÉNÉRALE & SCORE DE SANTÉ MATÉRIEL",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0099DA"
        )
        title.pack(side="left", padx=20, pady=12)

        btn_calc = ctk.CTkButton(
            header_frame,
            text="🔄  Recalculer la Synthèse",
            fg_color="#0099DA",
            hover_color="#0072CE",
            height=34,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.update_synthesis
        )
        btn_calc.pack(side="right", padx=15, pady=12)

        # HERO SCORE CARDS FRAME
        score_cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        score_cards_frame.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")
        score_cards_frame.grid_columnconfigure(0, weight=1)
        score_cards_frame.grid_columnconfigure(1, weight=2)

        # HERO SCORE BADGE
        self.card_score = ctk.CTkFrame(score_cards_frame, fg_color="#0F172A", corner_radius=12, border_width=2, border_color="#0099DA")
        self.card_score.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        lbl_score_title = ctk.CTkLabel(self.card_score, text="NOTE GLOBAL DE SANTÉ", font=ctk.CTkFont(size=11, weight="bold"), text_color="#0099DA")
        lbl_score_title.pack(anchor="center", pady=(12, 2))

        self.lbl_score_value = ctk.CTkLabel(self.card_score, text="-- / 100", font=ctk.CTkFont(size=32, weight="bold"), text_color="#10B981")
        self.lbl_score_value.pack(anchor="center", pady=(0, 2))

        self.lbl_urgency = ctk.CTkLabel(self.card_score, text="Niveau d'urgence : Faible", font=ctk.CTkFont(size=11, weight="bold"), text_color="#F8FAFC")
        self.lbl_urgency.pack(anchor="center", pady=(0, 12))

        # MAINTENANCE INTERVAL BADGE CARD
        self.card_maint = ctk.CTkFrame(score_cards_frame, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1F2937")
        self.card_maint.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        lbl_maint_t = ctk.CTkLabel(self.card_maint, text="📅 RECOMMANDATION DE MAINTENANCE MISTER GENIUS SA", font=ctk.CTkFont(size=12, weight="bold"), text_color="#0099DA")
        lbl_maint_t.pack(anchor="w", padx=15, pady=(12, 4))

        self.lbl_maint_date = ctk.CTkLabel(self.card_maint, text="Prochaine date conseillée : --", font=ctk.CTkFont(size=13, weight="bold"), text_color="#F8FAFC")
        self.lbl_maint_date.pack(anchor="w", padx=15, pady=2)

        self.lbl_maint_interval = ctk.CTkLabel(self.card_maint, text="Intervalle : Maintenance annuelle (Particulier)", font=ctk.CTkFont(size=11), text_color="#94A3B8")
        self.lbl_maint_interval.pack(anchor="w", padx=15, pady=(0, 12))

        # DETAILED SYNTHESIS OUTPUT
        self.textbox_synth = ctk.CTkTextbox(
            self,
            height=340,
            font=ctk.CTkFont(family="Courier", size=11),
            fg_color="#0B0F17",
            border_width=1,
            border_color="#1F2937"
        )
        self.textbox_synth.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

    def refresh_synthesis(self):
        self.update_synthesis()

    def update_synthesis(self):
        if not hasattr(self, "parent_app") or not self.parent_app:
            return

        client_data = self.parent_app.client_view.get_data()
        questionnaire = self.parent_app.quest_view.get_data()
        auto_data = self.parent_app.diag_view.get_data()
        test_results = self.parent_app.tests_view.get_data()

        synth = pdf_report.calculate_synthesis(client_data, questionnaire, auto_data, test_results)

        score = synth.get('score', 85)
        self.lbl_score_value.configure(text=f"{score} / 100")

        if score >= 80:
            self.lbl_score_value.configure(text_color="#10B981")
            self.card_score.configure(border_color="#10B981")
        elif score >= 50:
            self.lbl_score_value.configure(text_color="#F59E0B")
            self.card_score.configure(border_color="#F59E0B")
        else:
            self.lbl_score_value.configure(text_color="#EF4444")
            self.card_score.configure(border_color="#EF4444")

        self.lbl_urgency.configure(text=f"Urgence : {synth.get('urgency', 'Faible')}")
        self.lbl_maint_date.configure(text=f"Prochaine date conseillée : {synth.get('nextMaintenanceDate', 'N/A')}")
        self.lbl_maint_interval.configure(text=f"Intervalle : {synth.get('maintenanceInterval', 'N/A')}")

        out = f"=== BILAN DE SANTÉ & ÉTAT DE VIE DU MATÉRIEL (MISTER GENIUS SA) ===\n\n"
        out += f"NOTE DE SANTÉ GLOBALE : {synth['score']} / 100\n"
        out += f"NIVEAU D'URGENCE : {synth['urgency']}\n"
        out += f"INTERVALLE MAINTENANCE : {synth['maintenanceInterval']}\n"
        out += f"PROCHAINE MAINTENANCE CONSEILLÉE : {synth['nextMaintenanceDate']}\n\n"

        out += "[ÉTAT DE VIE DE CHAQUE COMPOSANT]\n"
        out += f" • PROCESSEUR (CPU) : {synth.get('cpu_health', 'Bon')}\n"
        out += f" • MÉMOIRE (RAM)    : {synth.get('ram_health', 'Bon')}\n"
        out += f" • STOCKAGE DISQUE  : {synth.get('disk_health', 'Bon')}\n"
        out += f" • CARTE GRAPHIQUE  : {synth.get('gpu_health', 'Bon')}\n"
        out += f" • BATTERIE         : {synth.get('battery_health', 'Non disponible')}\n\n"

        out += "[PROBLÈMES & ANOMALIES IDENTIFIÉS]\n"
        if synth['problems']:
            for p in synth['problems']:
                out += f" • {p}\n"
        else:
            out += " • Aucun dysfonctionnement ou anomalie détectée.\n"
        out += "\n"

        out += "[ACTIONS DE MAINTENANCE RÉALISÉES / CONSEILLÉES]\n"
        if synth['actions']:
            for a in synth['actions']:
                out += f" • {a}\n"
        else:
            out += " • Aucune action corrective immédiate requise.\n"
        out += "\n"

        out += "[RECOMMANDATIONS TECHNICIEN]\n"
        for r in synth['recommendations']:
            out += f" • {r}\n"

        self.textbox_synth.delete("1.0", "end")
        self.textbox_synth.insert("1.0", out)
