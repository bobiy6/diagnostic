import customtkinter as ctk
import datetime

class ClientView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(1, weight=1)

        # Title Header
        title = ctk.CTkLabel(
            self,
            text="Fiche Client & Machine - Mister Genius SA",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#DC2626"
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Informations sur l'intervention technique (sans coordonnées personnelles)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        # Fields
        ctk.CTkLabel(self, text="Nom Client / Raison Sociale :").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.entry_client_name = ctk.CTkEntry(self, placeholder_text="ex. Dupont Jean / SARL Tech", border_color="#DC2626")
        self.entry_client_name.insert(0, "Dupont Informatique")
        self.entry_client_name.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Date d'intervention :").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.entry_date = ctk.CTkEntry(self, border_color="#DC2626")
        self.entry_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Technicien Mister Genius :").grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.entry_technician = ctk.CTkEntry(self, placeholder_text="ex. Alexandre Martin", border_color="#DC2626")
        self.entry_technician.insert(0, "Alexandre Martin")
        self.entry_technician.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Type de Client :").grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.option_client_type = ctk.CTkOptionMenu(
            self,
            values=["Particulier", "Professionnel"],
            fg_color="#DC2626",
            button_color="#B91C1C",
            button_hover_color="#991B1B"
        )
        self.option_client_type.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Marque du PC :").grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.entry_pc_brand = ctk.CTkEntry(self, placeholder_text="ex. Asus, Lenovo, HP...", border_color="#DC2626")
        self.entry_pc_brand.insert(0, "Asus")
        self.entry_pc_brand.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Modèle du PC :").grid(row=7, column=0, padx=20, pady=10, sticky="w")
        self.entry_pc_model = ctk.CTkEntry(self, placeholder_text="ex. ZenBook 15 / ThinkPad X1", border_color="#DC2626")
        self.entry_pc_model.insert(0, "ZenBook Pro 15")
        self.entry_pc_model.grid(row=7, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="N° de Série :").grid(row=8, column=0, padx=20, pady=10, sticky="w")
        self.entry_serial = ctk.CTkEntry(self, placeholder_text="ex. SN-883920-AS", border_color="#DC2626")
        self.entry_serial.insert(0, "SN-883920-AS")
        self.entry_serial.grid(row=8, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Motif de consultation :").grid(row=9, column=0, padx=20, pady=10, sticky="nw")
        self.textbox_reason = ctk.CTkTextbox(self, height=80, border_color="#DC2626", border_width=1)
        self.textbox_reason.insert("1.0", "Surchauffe régulière, ralentissements au lancement des logiciels métiers")
        self.textbox_reason.grid(row=9, column=1, padx=20, pady=10, sticky="ew")

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
