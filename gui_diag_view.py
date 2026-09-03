import customtkinter as ctk
import system_diag

class DiagView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(header_frame, text="Diagnostic Automatique System", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(side="left")

        btn_refresh = ctk.CTkButton(header_frame, text="Actualiser", width=100, command=self.refresh_diag)
        btn_refresh.pack(side="right")

        self.textbox_diag = ctk.CTkTextbox(self, height=380, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox_diag.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.refresh_diag()

    def refresh_diag(self):
        diag_data = system_diag.get_system_diagnostics()
        self.auto_data = diag_data

        formatted_text = f"=== DIAGNOSTIC MACHINE AUTOMATIQUE ({diag_data['timestamp']}) ===\n\n"

        cpu = diag_data.get("cpu", {})
        formatted_text += f"[PROCESSEUR (CPU)]\n"
        formatted_text += f" • Modèle : {cpu.get('model')}\n"
        formatted_text += f" • Cœurs : {cpu.get('cores')}\n"
        formatted_text += f" • Fréquence : {cpu.get('speed')}\n"
        formatted_text += f" • Utilisation : {cpu.get('usage')}\n\n"

        ram = diag_data.get("ram", {})
        formatted_text += f"[MÉMOIRE (RAM)]\n"
        formatted_text += f" • Totale : {ram.get('total')}\n"
        formatted_text += f" • Utilisée : {ram.get('used')} ({ram.get('usedPercent')})\n"
        formatted_text += f" • Libre : {ram.get('free')}\n\n"

        formatted_text += f"[DISQUES DE STOCKAGE]\n"
        for d in diag_data.get("disks", []):
            formatted_text += f" • {d.get('mount')} ({d.get('fstype')}) : Total {d.get('total')} | Libre {d.get('free')} | Occupé {d.get('usedPercent')}\n"
        formatted_text += "\n"

        batt = diag_data.get("battery", {})
        formatted_text += f"[BATTERIE]\n"
        formatted_text += f" • Niveau : {batt.get('percent')}\n"
        formatted_text += f" • Statut charge : {batt.get('isCharging')}\n"
        formatted_text += f" • État de santé : {batt.get('health')}\n\n"

        os_info = diag_data.get("os", {})
        formatted_text += f"[SYSTÈME D'EXPLOITATION]\n"
        formatted_text += f" • OS : {os_info.get('distro')}\n"
        formatted_text += f" • Version : {os_info.get('version')}\n"
        formatted_text += f" • Architecture : {os_info.get('arch')}\n"
        formatted_text += f" • Nom hôte : {os_info.get('hostname')}\n\n"

        net = diag_data.get("network", [])
        formatted_text += f"[RÉSEAU]\n"
        for n in net:
            formatted_text += f" • Interface {n.get('iface')} : IP {n.get('ip')} ({n.get('status')})\n"

        self.textbox_diag.delete("1.0", "end")
        self.textbox_diag.insert("1.0", formatted_text)

    def get_data(self):
        return getattr(self, "auto_data", system_diag.get_system_diagnostics())
