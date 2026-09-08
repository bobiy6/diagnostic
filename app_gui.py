import os
import sys
import multiprocessing
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

from gui_client_view import ClientView
from gui_questionnaire_view import QuestionnaireView
from gui_diag_view import DiagView
from gui_tests_view import TestsView
from gui_synthesis_view import SynthesisView
import pdf_report
import asset_utils

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PCDiagnosticApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mister Genius SA - PC Diagnostic & Rapport Technique")
        self.geometry("1100x760")
        self.minsize(980, 680)

        # Configure root layout grid: Left Sidebar (col 0), Right Content Area (col 1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT SIDEBAR NAVIGATION PANEL (#0F172A)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#0F172A")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)  # Spacer row

        # Mister Genius Logo / Header
        logo_path = asset_utils.get_asset_path("assets/mister_genius_logo.png")
        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                self.logo_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(170, 50))
                self.logo_label = ctk.CTkLabel(self.sidebar, image=self.logo_image, text="")
                self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
            except Exception:
                self.logo_label = ctk.CTkLabel(
                    self.sidebar, text="MISTER GENIUS", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0099DA"
                )
                self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        else:
            self.logo_label = ctk.CTkLabel(
                self.sidebar, text="MISTER GENIUS", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0099DA"
            )
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))

        self.subtitle = ctk.CTkLabel(
            self.sidebar,
            text="PC Diagnostic & Rapport",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#64748B"
        )
        self.subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Navigation Category Title
        nav_title = ctk.CTkLabel(
            self.sidebar,
            text="INTERVENTION",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#475569"
        )
        nav_title.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")

        # Sidebar Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("client", "👤  Fiche Client"),
            ("quest", "📋  Questionnaire"),
            ("diag", "🔍  Diagnostic Auto"),
            ("tests", "⚡  Tests Machine"),
            ("synth", "📊  Synthèse & Score")
        ]

        for idx, (key, label) in enumerate(nav_items, start=3):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color="#94A3B8",
                hover_color="#1E293B",
                font=ctk.CTkFont(size=13, weight="bold"),
                command=lambda k=key: self.select_view(k)
            )
            btn.grid(row=idx, column=0, padx=12, pady=3, sticky="ew")
            self.nav_buttons[key] = btn

        # Bottom Sidebar Status Card
        self.sidebar_card = ctk.CTkFrame(self.sidebar, fg_color="#1E293B", corner_radius=10)
        self.sidebar_card.grid(row=8, column=0, padx=12, pady=15, sticky="ew")

        card_title = ctk.CTkLabel(
            self.sidebar_card, text="Mister Genius SA", font=ctk.CTkFont(size=11, weight="bold"), text_color="#0099DA"
        )
        card_title.pack(anchor="w", padx=12, pady=(10, 2))

        card_desc = ctk.CTkLabel(
            self.sidebar_card,
            text="« Il y a toujours une solution »\nVersion Portable USB v2.4",
            font=ctk.CTkFont(size=10),
            text_color="#64748B",
            justify="left"
        )
        card_desc.pack(anchor="w", padx=12, pady=(0, 10))

        # ==========================================
        # RIGHT MAIN CONTENT AREA
        # ==========================================
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color="#0B0F17")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        # Top Header Bar
        self.header_bar = ctk.CTkFrame(self.main_area, height=60, corner_radius=0, fg_color="#161E2E")
        self.header_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        self.current_title = ctk.CTkLabel(
            self.header_bar,
            text="Fiche Client & Machine",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#F8FAFC"
        )
        self.current_title.pack(side="left", padx=20, pady=15)

        # Header Action Buttons
        self.btn_pdf = ctk.CTkButton(
            self.header_bar,
            text="📄  Générer Rapport PDF",
            fg_color="#0099DA",
            hover_color="#0072CE",
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.export_pdf
        )
        self.btn_pdf.pack(side="right", padx=15, pady=12)

        self.btn_new = ctk.CTkButton(
            self.header_bar,
            text="🔄  Nouveau Diagnostic",
            fg_color="#334155",
            hover_color="#475569",
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            command=self.reset_all
        )
        self.btn_new.pack(side="right", padx=5, pady=12)

        # View Containers Frame
        self.container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Instantiate Sub-views
        self.views = {}
        self.views["client"] = ClientView(self.container)
        self.views["quest"] = QuestionnaireView(self.container)
        self.views["diag"] = DiagView(self.container)
        self.views["tests"] = TestsView(self.container)
        self.views["synth"] = SynthesisView(self.container)
        self.views["synth"].parent_app = self

        # Client view as default
        self.client_view = self.views["client"]
        self.quest_view = self.views["quest"]
        self.diag_view = self.views["diag"]
        self.tests_view = self.views["tests"]
        self.synth_view = self.views["synth"]

        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

        self.select_view("client")

    def select_view(self, key):
        titles = {
            "client": "👤  Fiche Client & Machine",
            "quest": "📋  Questionnaire & Interventions Matérielles",
            "diag": "🔍  Diagnostic Automatique du Système",
            "tests": "⚡  Benchmarks & Test de Piétinement 25 Min",
            "synth": "📊  Synthèse globale & Calcul du Score"
        }

        self.current_title.configure(text=titles.get(key, ""))

        # Highlight sidebar active button
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color="#0099DA", text_color="#FFFFFF", hover_color="#0072CE")
            else:
                btn.configure(fg_color="transparent", text_color="#94A3B8", hover_color="#1E293B")

        # Raise selected view frame
        frame = self.views[key]
        frame.tkraise()

        # Auto-refresh synthesis score if synthesis tab clicked
        if key == "synth" and hasattr(frame, "refresh_synthesis"):
            frame.refresh_synthesis()

    def reset_all(self):
        if messagebox.askyesno("Nouveau Diagnostic", "Voulez-vous réinitialiser tous les champs pour un nouveau PC ?"):
            self.client_view.reset_data()
            self.quest_view.reset_data()
            self.diag_view.refresh_diag()
            messagebox.showinfo("Réinitialisation", "Le diagnostic Mister Genius SA a été réinitialisé.")

    def export_pdf(self):
        client_data = self.client_view.get_data()
        questionnaire = self.quest_view.get_data()
        auto_data = self.diag_view.get_data()
        test_results = self.tests_view.get_data()

        default_filename = f"Mister_Genius_Rapport_{client_data.get('clientName', 'PC').replace(' ', '_')}.pdf"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf")],
            initialfile=default_filename,
            title="Enregistrer le Rapport PDF Mister Genius SA"
        )

        if filepath:
            try:
                pdf_report.generate_pdf_report(filepath, client_data, questionnaire, auto_data, test_results)
                messagebox.showinfo("Rapport Généré", f"Le rapport PDF Mister Genius SA a été généré avec succès :\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur PDF", f"Impossible de générer le rapport PDF :\n{str(e)}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = PCDiagnosticApp()
    app.mainloop()
