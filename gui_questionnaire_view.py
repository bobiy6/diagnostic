import customtkinter as ctk

class QuestionnaireView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Questionnaire Technicien - Mister Genius SA",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#0099DA"
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")

        subtitle = ctk.CTkLabel(self, text="Contrôles de maintenance (Oui / Non / Inconnu), pièces et observations", font=ctk.CTkFont(size=12), text_color="#64748B")
        subtitle.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        self.checklist_items = [
            ("dustCleaned", "Dépoussiérage physique effectué"),
            ("thermalPasteReplaced", "Remplacement pâte thermique"),
            ("diskScanOk", "Analyse intégrité disque SMART"),
            ("malwareCheck", "Scan Antivirus / Anti-Malware"),
            ("updatesDone", "Mises à jour OS & Pilotes")
        ]

        self.checklist_vars = {}
        row_idx = 2
        for key, label in self.checklist_items:
            ctk.CTkLabel(self, text=label + " :").grid(row=row_idx, column=0, padx=20, pady=6, sticky="w")
            seg = ctk.CTkSegmentedButton(
                self,
                values=["oui", "non", "inconnu"],
                selected_color="#0099DA",
                selected_hover_color="#0072CE"
            )
            seg.set("oui")
            seg.grid(row=row_idx, column=1, padx=20, pady=6, sticky="w")
            self.checklist_vars[key] = seg
            row_idx += 1

        ctk.CTkLabel(self, text="Nature des problèmes :").grid(row=row_idx, column=0, padx=20, pady=10, sticky="nw")
        self.textbox_issues = ctk.CTkTextbox(self, height=60, border_color="#0099DA", border_width=1)
        self.textbox_issues.insert("1.0", "Ventilateur encrassé et pilote de carte graphique obsolète.")
        self.textbox_issues.grid(row=row_idx, column=1, padx=20, pady=10, sticky="ew")
        row_idx += 1

        ctk.CTkLabel(self, text="Composants changés :").grid(row=row_idx, column=0, padx=20, pady=10, sticky="w")
        self.entry_comp_name = ctk.CTkEntry(self, placeholder_text="Pièce (ex. SSD NVMe 1 To)", border_color="#0099DA")
        self.entry_comp_name.insert(0, "SSD NVMe 1 To")
        self.entry_comp_name.grid(row=row_idx, column=1, padx=20, pady=10, sticky="ew")
        row_idx += 1

        ctk.CTkLabel(self, text="Raison du changement :").grid(row=row_idx, column=0, padx=20, pady=10, sticky="w")
        self.entry_comp_reason = ctk.CTkEntry(self, placeholder_text="Raison (ex. Amélioration vitesse)", border_color="#0099DA")
        self.entry_comp_reason.insert(0, "Amélioration de la vitesse de démarrage")
        self.entry_comp_reason.grid(row=row_idx, column=1, padx=20, pady=10, sticky="ew")
        row_idx += 1

        ctk.CTkLabel(self, text="Observations technicien :").grid(row=row_idx, column=0, padx=20, pady=10, sticky="nw")
        self.textbox_obs = ctk.CTkTextbox(self, height=80, border_color="#0099DA", border_width=1)
        self.textbox_obs.insert("1.0", "Nettoyage complet effectué, dépoussiérage des ouïes d'aération. Remise à niveau des pilotes par Mister Genius SA.")
        self.textbox_obs.grid(row=row_idx, column=1, padx=20, pady=10, sticky="ew")

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
