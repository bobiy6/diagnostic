import customtkinter as ctk
import pdf_report

class SynthesisView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(header_frame, text="Synthèse Générale & Bilan de Santé Matériel", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(side="left")

        btn_calc = ctk.CTkButton(header_frame, text="Calculer Bilan & Santé", width=160, command=self.update_synthesis)
        btn_calc.pack(side="right")

        self.textbox_synth = ctk.CTkTextbox(self, height=420, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox_synth.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.parent_app = parent

    def update_synthesis(self):
        client_data = self.parent_app.client_view.get_data()
        questionnaire = self.parent_app.quest_view.get_data()
        auto_data = self.parent_app.diag_view.get_data()
        test_results = self.parent_app.tests_view.get_data()

        synth = pdf_report.calculate_synthesis(client_data, questionnaire, auto_data, test_results)

        out = f"=== BILAN DE SANTÉ & ÉTAT DE VIE DU MATÉRIEL ===\n\n"
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
