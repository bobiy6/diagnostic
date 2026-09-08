import customtkinter as ctk
import datetime

class ClientView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

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

        # Date
        ctk.CTkLabel(card_intervention, text="Date d'intervention :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, padx=20, pady=8, sticky="w")
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
            text="💻  SPÉCIFICATIONS PC CLIENT",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0099DA"
        )
        header_hw.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="w")

        # Marque PC
        ctk.CTkLabel(card_hardware, text="Marque du PC :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, padx=20, pady=8, sticky="w")
        self.entry_pc_brand = ctk.CTkEntry(card_hardware, placeholder_text="ex. Asus, Lenovo, HP...", border_color="#0099DA", height=36)
        self.entry_pc_brand.insert(0, "Asus")
        self.entry_pc_brand.grid(row=1, column=1, padx=20, pady=8, sticky="ew")

        # Modèle PC
        ctk.CTkLabel(card_hardware, text="Modèle du PC :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, padx=20, pady=8, sticky="w")
        self.entry_pc_model = ctk.CTkEntry(card_hardware, placeholder_text="ex. ZenBook 15 / ThinkPad X1", border_color="#0099DA", height=36)
        self.entry_pc_model.insert(0, "ZenBook Pro 15")
        self.entry_pc_model.grid(row=2, column=1, padx=20, pady=8, sticky="ew")

        # N° de Série
        ctk.CTkLabel(card_hardware, text="N° de Série :", font=ctk.CTkFont(size=12, weight="bold")).grid(row=3, column=0, padx=20, pady=8, sticky="w")
        self.entry_serial = ctk.CTkEntry(card_hardware, placeholder_text="ex. SN-883920-AS", border_color="#0099DA", height=36)
        self.entry_serial.insert(0, "SN-883920-AS")
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
            text="🔒  RAPPEL PROTOCOLE : Les données personnelles (adresse, téléphone, email) ne sont pas stockées pour garantir la confidentialité client conforme RGPD.",
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
        self.entry_client_name.delete(0, "end")
        self.entry_technician.delete(0, "end")
        self.entry_pc_brand.delete(0, "end")
        self.entry_pc_model.delete(0, "end")
        self.entry_serial.delete(0, "end")
        self.textbox_reason.delete("1.0", "end")
