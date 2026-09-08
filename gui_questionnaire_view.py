import customtkinter as ctk

class QuestionnaireView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # LEFT CARD: CHECKLIST CONTRÔLES
        card_checklist = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1F2937")
        card_checklist.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        card_checklist.grid_columnconfigure(1, weight=1)

        header_chk = ctk.CTkLabel(
            card_checklist,
            text="📋  CONTRÔLES DE MAINTENANCE",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0099DA"
        )
        header_chk.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="w")

        self.checklist_items = [
            ("dustCleaned", "Dépoussiérage physique effectué"),
            ("thermalPasteReplaced", "Remplacement pâte thermique"),
            ("diskScanOk", "Analyse intégrité disque SMART"),
            ("malwareCheck", "Scan Antivirus / Anti-Malware"),
            ("updatesDone", "Mises à jour OS & Pilotes")
        ]

        self.checklist_vars = {}
        for idx, (key, label) in enumerate(self.checklist_items, start=1):
            ctk.CTkLabel(card_checklist, text=label + " :", font=ctk.CTkFont(size=11, weight="bold")).grid(row=idx, column=0, padx=20, pady=8, sticky="w")
            seg = ctk.CTkSegmentedButton(
                card_checklist,
                values=["oui", "non", "inconnu"],
                selected_color="#0099DA",
                selected_hover_color="#0072CE",
                height=30
            )
            seg.set("oui")
            seg.grid(row=idx, column=1, padx=20, pady=8, sticky="e")
            self.checklist_vars[key] = seg

        # RIGHT CARD: INTERVENTIONS & OBSERVATIONS
        card_interventions = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1F2937")
        card_interventions.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        card_interventions.grid_columnconfigure(1, weight=1)

        header_obs = ctk.CTkLabel(
            card_interventions,
            text="📝  INTERVENTIONS & OBSERVATIONS",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0099DA"
        )
        header_obs.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="w")

        # Nature des problèmes
        ctk.CTkLabel(card_interventions, text="Nature des problèmes :", font=ctk.CTkFont(size=11, weight="bold")).grid(row=1, column=0, padx=20, pady=6, sticky="nw")
        self.textbox_issues = ctk.CTkTextbox(card_interventions, height=55, border_color="#0099DA", border_width=1)
        self.textbox_issues.insert("1.0", "Ventilateur encrassé et pilote de carte graphique obsolète.")
        self.textbox_issues.grid(row=1, column=1, padx=20, pady=6, sticky="ew")

        # Composants changés
        ctk.CTkLabel(card_interventions, text="Pièce remplacée :", font=ctk.CTkFont(size=11, weight="bold")).grid(row=2, column=0, padx=20, pady=6, sticky="w")
        self.entry_comp_name = ctk.CTkEntry(card_interventions, placeholder_text="Pièce (ex. SSD NVMe 1 To)", border_color="#0099DA", height=34)
        self.entry_comp_name.insert(0, "SSD NVMe 1 To")
        self.entry_comp_name.grid(row=2, column=1, padx=20, pady=6, sticky="ew")

        # Raison du changement
        ctk.CTkLabel(card_interventions, text="Motif du changement :", font=ctk.CTkFont(size=11, weight="bold")).grid(row=3, column=0, padx=20, pady=6, sticky="w")
        self.entry_comp_reason = ctk.CTkEntry(card_interventions, placeholder_text="Raison (ex. Amélioration vitesse)", border_color="#0099DA", height=34)
        self.entry_comp_reason.insert(0, "Amélioration de la vitesse de démarrage")
        self.entry_comp_reason.grid(row=3, column=1, padx=20, pady=6, sticky="ew")

        # Observations
        ctk.CTkLabel(card_interventions, text="Observations :", font=ctk.CTkFont(size=11, weight="bold")).grid(row=4, column=0, padx=20, pady=6, sticky="nw")
        self.textbox_obs = ctk.CTkTextbox(card_interventions, height=65, border_color="#0099DA", border_width=1)
        self.textbox_obs.insert("1.0", "Nettoyage complet effectué, dépoussiérage des ouïes d'aération. Remise à niveau des pilotes par Mister Genius SA.")
        self.textbox_obs.grid(row=4, column=1, padx=20, pady=6, sticky="ew")

    def get_data(self):
        checklist = {key: seg.get() for key, seg in self.checklist_vars.items()}
        comp_name = self.entry_comp_name.get()
        comp_reason = self.entry_comp_reason.get()
        replaced = [{"name": comp_name, "reason": comp_reason}] if comp_name else []

        return {
            "checklist": checklist,
            "issuesNature": self.textbox_issues.get("1.0", "end-1c"),
            "replacedComponents": replaced,
            "observations": self.textbox_obs.get("1.0", "end-1c")
        }

    def reset_data(self):
        for seg in self.checklist_vars.values():
            seg.set("inconnu")
        self.textbox_issues.delete("1.0", "end")
        self.entry_comp_name.delete(0, "end")
        self.entry_comp_reason.delete(0, "end")
        self.textbox_obs.delete("1.0", "end")
