import os
import sys
import ctypes
import threading
import multiprocessing
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

from gui_client_view import ClientView
from gui_questionnaire_view import QuestionnaireView
from gui_diag_view import DiagView
from gui_tests_view import TestsView
from gui_synthesis_view import SynthesisView
import system_diag
import pdf_report
import asset_utils

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.overrideredirect(True)
        self.configure(fg_color="#0F172A")

        width = 520
        height = 340

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = (screen_w // 2) - (width // 2)
        pos_y = (screen_h // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.attributes("-topmost", True)

        # Card container with cyan border
        container = ctk.CTkFrame(self, fg_color="#0F172A", corner_radius=16, border_width=2, border_color="#0099DA")
        container.pack(fill="both", expand=True, padx=2, pady=2)

        # Logo
        logo_path = asset_utils.get_asset_path("assets/mister_genius_logo.png")
        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                self.logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 100))
                self.lbl_logo = ctk.CTkLabel(container, image=self.logo_img, text="")
                self.lbl_logo.pack(pady=(25, 5))
            except Exception:
                self.lbl_logo = ctk.CTkLabel(
                    container, text="MISTER GENIUS SA", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0099DA"
                )
                self.lbl_logo.pack(pady=(25, 5))
        else:
            self.lbl_logo = ctk.CTkLabel(
                container, text="MISTER GENIUS SA", font=ctk.CTkFont(size=22, weight="bold"), text_color="#0099DA"
            )
            self.lbl_logo.pack(pady=(25, 5))

        self.lbl_title = ctk.CTkLabel(
            container, text="Mister Genius SA - PC Diagnostic", font=ctk.CTkFont(size=16, weight="bold"), text_color="#F8FAFC"
        )
        self.lbl_title.pack(pady=(2, 2))

        self.lbl_tagline = ctk.CTkLabel(
            container, text="« Il y a toujours une solution »", font=ctk.CTkFont(size=12, slant="italic"), text_color="#0099DA"
        )
        self.lbl_tagline.pack(pady=(0, 20))

        # Progress bar & Status
        self.progress_bar = ctk.CTkProgressBar(container, progress_color="#0099DA", width=420, height=10)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10))

        self.lbl_status = ctk.CTkLabel(
            container, text="Chargement des composants du PC...", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94A3B8"
        )
        self.lbl_status.pack(pady=(0, 15))


class PCDiagnosticApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Register Windows AppUserModelID
        if sys.platform == "win32":
            try:
                myappid = 'mistergenius.pcdiagnostic.app.2.4'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception:
                pass

        self.withdraw()  # Hide main window initially during splash loading

        self.title("Mister Genius SA - PC Diagnostic & Rapport Technique")
        self.geometry("1100x760")
        self.minsize(980, 680)

        # Set Window Icon
        ico_path = asset_utils.get_asset_path("assets/mister_genius_logo.ico")
        png_path = asset_utils.get_asset_path("assets/mister_genius_logo.png")
        if os.path.exists(ico_path) and sys.platform == "win32":
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass
        elif os.path.exists(png_path):
            try:
                img = Image.open(png_path)
                self._app_icon = ImageTk.PhotoImage(img)
                self.iconphoto(True, self._app_icon)
            except Exception:
                pass

        # Display Splash Screen
        self.splash = SplashScreen(self)
        self.splash.update()

        # Begin background initialization
        thread = threading.Thread(target=self._init_app_components, daemon=True)
        thread.start()

    def _update_splash_progress(self, message, progress):
        try:
            self.splash.progress_bar.set(progress)
            self.splash.lbl_status.configure(text=message)
            self.splash.update()
        except Exception:
            pass

    def _init_app_components(self):
        # Step 1: Detect PC Hardware Specs (DMI / WMI)
        self.after(0, self._update_splash_progress, "Détection des spécifications matériel (Marque, Modèle, Série)...", 0.25)
        _ = system_diag.get_auto_pc_specs()

        # Step 2: Initialize System Diagnostics Sensors & Metrics
        self.after(0, self._update_splash_progress, "Initialisation des capteurs thermiques et métriques CPU/RAM...", 0.60)
        _ = system_diag.get_system_diagnostics()

        # Step 3: Instantiate UI Layout Components
        self.after(0, self._update_splash_progress, "Construction de l'interface utilisateur Mister Genius SA...", 0.85)
        self.after(0, self._build_main_gui)

    def _build_main_gui(self):
        # Configure root layout grid
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
                self.logo_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(110, 110))
                self.logo_label = ctk.CTkLabel(self.sidebar, image=self.logo_image, text="")
                self.logo_label.grid(row=0, column=0, padx=20, pady=(15, 5))
            except Exception:
                self.logo_label = ctk.CTkLabel(
                    self.sidebar, text="MISTER GENIUS", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0099DA"
                )
                self.logo_label.grid(row=0, column=0, padx=20, pady=(15, 5))
        else:
            self.logo_label = ctk.CTkLabel(
                self.sidebar, text="MISTER GENIUS", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0099DA"
            )
            self.logo_label.grid(row=0, column=0, padx=20, pady=(15, 5))

        self.subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Mister Genius SA\nPC Diagnostic & Rapport",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#0099DA"
        )
        self.subtitle.grid(row=1, column=0, padx=20, pady=(0, 15))

        # Navigation Category Title
        nav_title = ctk.CTkLabel(
            self.sidebar,
            text="INTERVENTION",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#475569"
        )
        nav_title.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="w")

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

        # Complete splash loading and show main window
        self._update_splash_progress("Lancement de l'application...", 1.0)
        self.after(300, self._finish_splash_and_reveal_main)

    def _finish_splash_and_reveal_main(self):
        try:
            self.splash.destroy()
        except Exception:
            pass
        self.deiconify()

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
