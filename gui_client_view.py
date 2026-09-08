import customtkinter as ctk
import datetime
import system_diag

class ClientView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Auto-detect PC specs (Brand, Model, Serial Number)
        auto_specs = system_diag.get_auto_pc_specs()

        # CARD 1: INFORMATIONS INTERVENTION
        card_intervention = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1F2937")
        card_intervention.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        card_intervention.grid_columnconfigure(1, weight=1)

        header_inter = ctk.CTkLabel(
            card_intervention,
            text="👤  INFORMATIONS INTERVENTION",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0099DA"
        )
        header_inter.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="w")

        # Nom Client
        ctk.CTkLabel(card_intervention, text="Nom Client / Raison Sociale :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, padx=20, pady=8, sticky="w")
        self.entry_client_name = ctk.CTkEntry(card_intervention, placeholder_text="ex. Dupont Jean / SARL Tech", border_color="#0099DA", height=36)
        self.entry_client_name.insert(0, "Dupont Informatique")
        self.entry_client_name.grid(row=1, column=1, padx=20, pady=8, sticky="ew")

        # Date d'intervention (Auto)
        ctk.CTkLabel(card_intervention, text="Date d'intervention (Auto) :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, padx=20, pady=8, sticky="w")
        self.entry_date = ctk.CTkEntry(card_intervention, border_color="#0099DA", height=36)
        self.entry_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=2, column=1, padx=20, pady=8, sticky="ew")

        # Technicien
        ctk.CTkLabel(card_intervention, text="Technicien Mister Genius :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=3, column=0, padx=20, pady=8, sticky="w")
        self.entry_technician = ctk.CTkEntry(card_intervention, placeholder_text="ex. Alexandre Martin", border_color="#0099DA", height=36)
        self.entry_technician.insert(0, "Alexandre Martin")
        self.entry_technician.grid(row=3, column=1, padx=20, pady=8, sticky="ew")

        # Type Client
        ctk.CTkLabel(card_intervention, text="Type de Client :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=4, column=0, padx=20, pady=8, sticky="w")
        self.option_client_type = ctk.CTkOptionMenu(
            card_intervention,
            values=["Particulier", "Professionnel"],
            fg_color="#0099DA",
            button_color="#0072CE",
            button_hover_color="#0056B3",
            height=36
        )
        self.option_client_type.grid(row=4, column=1, padx=20, pady=8, sticky="ew")

        # CARD 2: SPÉCIFICATIONS MATÉRIEL & MOTIF
        card_hardware = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1F2937")
        card_hardware.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        card_hardware.grid_columnconfigure(1, weight=1)

        header_hw = ctk.CTkLabel(
            card_hardware,
            text="💻  SPÉCIFICATIONS PC CLIENT (DÉTECTÉES AUTO)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0099DA"
        )
        header_hw.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="w")

        # Marque PC (Auto)
        ctk.CTkLabel(card_hardware, text="Marque du PC (Auto) :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, padx=20, pady=8, sticky="w")
        self.entry_pc_brand = ctk.CTkEntry(card_hardware, placeholder_text="Marque auto...", border_color="#0099DA", height=36)
        self.entry_pc_brand.insert(0, auto_specs.get("brand", ""))
        self.entry_pc_brand.grid(row=1, column=1, padx=20, pady=8, sticky="ew")

        # Modèle PC (Auto)
        ctk.CTkLabel(card_hardware, text="Modèle du PC (Auto) :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, padx=20, pady=8, sticky="w")
        self.entry_pc_model = ctk.CTkEntry(card_hardware, placeholder_text="Modèle auto...", border_color="#0099DA", height=36)
        self.entry_pc_model.insert(0, auto_specs.get("model", ""))
        self.entry_pc_model.grid(row=2, column=1, padx=20, pady=8, sticky="ew")

        # N° de Série (Auto)
        ctk.CTkLabel(card_hardware, text="N° de Série (Auto) :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=3, column=0, padx=20, pady=8, sticky="w")
        self.entry_serial = ctk.CTkEntry(card_hardware, placeholder_text="Série auto...", border_color="#0099DA", height=36)
        self.entry_serial.insert(0, auto_specs.get("serial", ""))
        self.entry_serial.grid(row=3, column=1, padx=20, pady=8, sticky="ew")

        # Motif
        ctk.CTkLabel(card_hardware, text="Motif de consultation :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=4, column=0, padx=20, pady=8, sticky="nw")
        self.textbox_reason = ctk.CTkTextbox(card_hardware, height=75, border_color="#0099DA", border_width=1)
        self.textbox_reason.insert("1.0", "Surchauffe régulière, ralentissements au lancement des logiciels métiers")
        self.textbox_reason.grid(row=4, column=1, padx=20, pady=8, sticky="ew")

        # NOTICE CARD AT BOTTOM
        card_notice = ctk.CTkFrame(self, fg_color="#162032", corner_radius=10, border_width=1, border_color="#1E293B")
        card_notice.grid(row=1, column=0, columnspan=2, padx=0, pady=(15, 0), sticky="ew")

        lbl_notice = ctk.CTkLabel(
            card_notice,
            text="🔒  RAPPEL PROTOCOLE : La date, la marque, le modèle et le numéro de série du PC sont détectés automatiquement. Les données personnelles ne sont pas stockées.",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8"
        )
        lbl_notice.pack(padx=15, pady=12, anchor="w")

    def get_data(self):
        return {
            "clientName": self.entry_client_name.get(),
            "date": self.entry_date.get(),
            "technician": self.entry_technician.get(),
            "clientType": self.option_client_type.get(),
            "pcBrand": self.entry_pc_brand.get(),
            "pcModel": self.entry_pc_model.get(),
            "serialNumber": self.entry_serial.get(),
            "reason": self.textbox_reason.get("1.0", "end-1c")
        }

    def reset_data(self):
        auto_specs = system_diag.get_auto_pc_specs()
        self.entry_client_name.delete(0, "end")
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.entry_technician.delete(0, "end")

        self.entry_pc_brand.delete(0, "end")
        self.entry_pc_brand.insert(0, auto_specs.get("brand", ""))

        self.entry_pc_model.delete(0, "end")
        self.entry_pc_model.insert(0, auto_specs.get("model", ""))

        self.entry_serial.delete(0, "end")
        self.entry_serial.insert(0, auto_specs.get("serial", ""))

        self.textbox_reason.delete("1.0", "end")
