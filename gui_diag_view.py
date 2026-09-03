import customtkinter as ctk
import system_diag

class DiagView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        title = ctk.CTkLabel(header_frame, text="Diagnostic Automatique du Matériel", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(side="left")

        btn_refresh = ctk.CTkButton(header_frame, text="Actualiser le Diagnostic", width=160, command=self.refresh_diag)
        btn_refresh.pack(side="right")

        self.textbox_diag = ctk.CTkTextbox(self, height=420, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox_diag.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.refresh_diag()

    def refresh_diag(self):
        diag_data = system_diag.get_system_diagnostics()
        self.auto_data = diag_data

        formatted_text = f"=== CARACTÉRISTIQUES DÉTAILLÉES DU MATÉRIEL ({diag_data['timestamp']}) ===\n\n"

        cpu = diag_data.get("cpu", {})
        formatted_text += f"[PROCESSEUR (CPU)]\n"
        formatted_text += f" • Modèle : {cpu.get('model')}\n"
        formatted_text += f" • Cœurs : {cpu.get('cores')}\n"
        formatted_text += f" • Fréquence : {cpu.get('freq')}\n"
        formatted_text += f" • Charge actuelle : {cpu.get('usage')}\n"
        formatted_text += f" • Températures : {cpu.get('temperature')}\n\n"

        ram = diag_data.get("ram", {})
        formatted_text += f"[MÉMOIRE (RAM & SWAP)]\n"
        formatted_text += f" • Capacité totale : {ram.get('total')}\n"
        formatted_text += f" • Utilisée : {ram.get('used')} ({ram.get('usedPercent')})\n"
        formatted_text += f" • Disponible : {ram.get('free')}\n"
        formatted_text += f" • Mémoire Swap : {ram.get('swap')}\n\n"

        formatted_text += f"[DISQUES DE STOCKAGE]\n"
        for d in diag_data.get("disks", []):
            formatted_text += f" • {d.get('mount')} ({d.get('device')} | {d.get('fstype')})\n"
            formatted_text += f"   - Espace : Total {d.get('total')} | Utilisé {d.get('used')} ({d.get('usedPercent')}) | Libre {d.get('free')}\n"
            formatted_text += f"   - Statistiques E/S : {d.get('io')}\n"
            formatted_text += f"   - État estimé : {d.get('healthStatus')}\n"
        formatted_text += "\n"

        batt = diag_data.get("battery", {})
        formatted_text += f"[BATTERIE & ALIMENTATION]\n"
        formatted_text += f" • Niveau de charge : {batt.get('percent')}\n"
        formatted_text += f" • Alimentation secteur : {batt.get('isCharging')}\n"
        formatted_text += f" • Autonomie restante : {batt.get('lifetime')}\n"
        formatted_text += f" • Estimation d'usure : {batt.get('wearEstimation')}\n"
        formatted_text += f" • État de santé : {batt.get('health')}\n\n"

        os_info = diag_data.get("os", {})
        formatted_text += f"[SYSTÈME D'EXPLOITATION & SHUTDOWN]\n"
        formatted_text += f" • OS : {os_info.get('distro')}\n"
        formatted_text += f" • Version : {os_info.get('version')}\n"
        formatted_text += f" • Architecture : {os_info.get('arch')}\n"
        formatted_text += f" • Nom d'hôte : {os_info.get('hostname')}\n"
        formatted_text += f" • Temps de fonctionnement (Uptime) : {os_info.get('uptime')}\n\n"

        net = diag_data.get("network", [])
        formatted_text += f"[RÉSEAU & INTERFACES]\n"
        for n in net:
            formatted_text += f" • {n.get('iface')} [{n.get('status')}] : IP {n.get('ip')} | MAC {n.get('mac')} | Vitesse {n.get('speed')}\n"
            formatted_text += f"   - Trafic réseau : {n.get('io')}\n"

        self.textbox_diag.delete("1.0", "end")
        self.textbox_diag.insert("1.0", formatted_text)

    def get_data(self):
        return getattr(self, "auto_data", system_diag.get_system_diagnostics())
