import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

from gui_client_view import ClientView
from gui_questionnaire_view import QuestionnaireView
from gui_diag_view import DiagView
from gui_tests_view import TestsView
from gui_synthesis_view import SynthesisView
import pdf_report

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PCDiagnosticApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PC Diagnostic & Rapport - Application Portable Technicien")
        self.geometry("950 x 680")
        self.minsize(800, 600)

        # Top Header Bar
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.pack(fill="x", side="top", padx=0, pady=0)

        self.app_title = ctk.CTkLabel(
            self.header_frame,
            text="PC Diagnostic & Rapport",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.app_title.pack(side="left", padx=20, pady=12)

        self.btn_pdf = ctk.CTkButton(
            self.header_frame,
            text="Générer Rapport PDF",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.export_pdf
        )
        self.btn_pdf.pack(side="right", padx=15, pady=12)

        self.btn_new = ctk.CTkButton(
            self.header_frame,
            text="Nouveau Diagnostic",
            fg_color="#334155",
            hover_color="#475569",
            command=self.reset_all
        )
        self.btn_new.pack(side="right", padx=5, pady=12)

        # Tab View
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_client = self.tabview.add("Fiche Client")
        self.tab_quest = self.tabview.add("Questionnaire")
        self.tab_diag = self.tabview.add("Diagnostic Auto")
        self.tab_tests = self.tabview.add("Tests Machine")
        self.tab_synth = self.tabview.add("Synthèse")

        # Instantiate View Frames
        self.client_view = ClientView(self.tab_client)
        self.client_view.pack(fill="both", expand=True)

        self.quest_view = QuestionnaireView(self.tab_quest)
        self.quest_view.pack(fill="both", expand=True)

        self.diag_view = DiagView(self.tab_diag)
        self.diag_view.pack(fill="both", expand=True)

        self.tests_view = TestsView(self.tab_tests)
        self.tests_view.pack(fill="both", expand=True)

        self.synth_view = SynthesisView(self.tab_synth)
        self.synth_view.parent_app = self
        self.synth_view.pack(fill="both", expand=True)

    def reset_all(self):
        if messagebox.askyesno("Nouveau Diagnostic", "Voulez-vous réinitialiser tous les champs pour un nouveau PC ?"):
            self.client_view.reset_data()
            self.quest_view.reset_data()
            self.diag_view.refresh_diag()
            messagebox.showinfo("Réinitialisation", "Le diagnostic a été réinitialisé.")

    def export_pdf(self):
        client_data = self.client_view.get_data()
        questionnaire = self.quest_view.get_data()
        auto_data = self.diag_view.get_data()
        test_results = self.tests_view.get_data()

        default_filename = f"Rapport_Diagnostic_{client_data.get('clientName', 'PC').replace(' ', '_')}.pdf"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf")],
            initialfile=default_filename,
            title="Enregistrer le Rapport PDF Client"
        )

        if filepath:
            try:
                pdf_report.generate_pdf_report(filepath, client_data, questionnaire, auto_data, test_results)
                messagebox.showinfo("Rapport Généré", f"Le rapport PDF a été généré avec succès :\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur PDF", f"Impossible de générer le rapport PDF :\n{str(e)}")

if __name__ == "__main__":
    app = PCDiagnosticApp()
    app.mainloop()
