import customtkinter as ctk
import system_diag

class DiagView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        # TOP BAR
        header_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1F2937")
        header_frame.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        title = ctk.CTkLabel(
            header_frame,
            text="🔍  DIAGNOSTIC AUTOMATIQUE MATÉRIEL & SYSTÈME",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0099DA"
        )
        title.pack(side="left", padx=20, pady=12)

        btn_refresh = ctk.CTkButton(
            header_frame,
            text="🔄  Actualiser Métriques",
            fg_color="#0099DA",
            hover_color="#0072CE",
            height=34,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.refresh_diag
        )
        btn_refresh.pack(side="right", padx=15, pady=12)

        # QUICK STAT BADGES FRAME
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")
        for i in range(4):
            self.stats_frame.grid_columnconfigure(i, weight=1)

        self.card_cpu = self._create_stat_card(self.stats_frame, 0, "💻 PROCESSEUR", "Charge: --", "Cœurs: --")
        self.card_ram = self._create_stat_card(self.stats_frame, 1, "⚡ MÉMOIRE RAM", "Total: --", "Libre: --")
        self.card_disk = self._create_stat_card(self.stats_frame, 2, "💾 STOCKAGE", "Espace: --", "État: --")
        self.card_batt = self._create_stat_card(self.stats_frame, 3, "🔋 BATTERIE", "Niveau: --", "Santé: --")

        # DETAILED TEXT CONSOLE
        self.textbox_diag = ctk.CTkTextbox(
            self,
            height=380,
            font=ctk.CTkFont(family="Courier", size=11),
            fg_color="#0F172A",
            border_width=1,
            border_color="#1E293B"
        )
        self.textbox_diag.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

        self.refresh_diag()

    def _create_stat_card(self, parent, col, title, line1, line2):
        card = ctk.CTkFrame(parent, fg_color="#111827", corner_radius=10, border_width=1, border_color="#1F2937")
        card.grid(row=0, column=col, padx=(0 if col==0 else 5, 0 if col==3 else 5), pady=0, sticky="ew")

        lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=11, weight="bold"), text_color="#0099DA")
        lbl_t.pack(anchor="w", padx=12, pady=(10, 2))

        lbl_1 = ctk.CTkLabel(card, text=line1, font=ctk.CTkFont(size=11), text_color="#F8FAFC")
        lbl_1.pack(anchor="w", padx=12, pady=1)

        lbl_2 = ctk.CTkLabel(card, text=line2, font=ctk.CTkFont(size=10), text_color="#94A3B8")
        lbl_2.pack(anchor="w", padx=12, pady=(1, 10))

        return {"card": card, "line1": lbl_1, "line2": lbl_2}

    def refresh_diag(self):
        diag_data = system_diag.get_system_diagnostics()
        self.auto_data = diag_data

        cpu = diag_data.get("cpu", {})
        ram = diag_data.get("ram", {})
        disks = diag_data.get("disks", [])
        batt = diag_data.get("battery", {})

        # Update Stat Badges
        self.card_cpu["line1"].configure(text=f"Charge: {cpu.get('usage', 'N/A')}")
        self.card_cpu["line2"].configure(text=f"Cœurs: {cpu.get('cores', 'N/A')} ({cpu.get('freq', 'N/A')})")

        self.card_ram["line1"].configure(text=f"Total: {ram.get('total', 'N/A')}")
        self.card_ram["line2"].configure(text=f"Utilisé: {ram.get('usedPercent', 'N/A')}")

        main_disk = disks[0] if disks else {}
        self.card_disk["line1"].configure(text=f"Libre: {main_disk.get('free', 'N/A')}")
        self.card_disk["line2"].configure(text=f"État: {main_disk.get('healthStatus', 'N/A')}")

        self.card_batt["line1"].configure(text=f"Niveau: {batt.get('percent', 'N/A')}")
        self.card_batt["line2"].configure(text=f"Santé: {batt.get('health', 'N/A')}")

        # Formatted Output
        formatted_text = f"=== MISTER GENIUS SA • DÉTAILS DIAGNOSTIC AUTOMATIQUE ({diag_data['timestamp']}) ===\n\n"

        formatted_text += f"[PROCESSEUR (CPU)]\n"
        formatted_text += f" • Modèle : {cpu.get('model')}\n"
        formatted_text += f" • Cœurs : {cpu.get('cores')}\n"
        formatted_text += f" • Fréquence : {cpu.get('freq')}\n"
        formatted_text += f" • Charge actuelle : {cpu.get('usage')}\n"
        formatted_text += f" • Températures : {cpu.get('temperature')}\n\n"

        formatted_text += f"[MÉMOIRE (RAM & SWAP)]\n"
        formatted_text += f" • Capacité totale : {ram.get('total')}\n"
        formatted_text += f" • Utilisée : {ram.get('used')} ({ram.get('usedPercent')})\n"
        formatted_text += f" • Disponible : {ram.get('free')}\n"
        formatted_text += f" • Mémoire Swap : {ram.get('swap')}\n\n"

        formatted_text += f"[DISQUES DE STOCKAGE]\n"
        for d in disks:
            formatted_text += f" • {d.get('mount')} ({d.get('device')} | {d.get('fstype')})\n"
            formatted_text += f"   - Espace : Total {d.get('total')} | Utilisé {d.get('used')} ({d.get('usedPercent')}) | Libre {d.get('free')}\n"
            formatted_text += f"   - Statistiques E/S : {d.get('io')}\n"
            formatted_text += f"   - État estimé : {d.get('healthStatus')}\n"
        formatted_text += "\n"

        formatted_text += f"[BATTERIE & ALIMENTATION]\n"
        formatted_text += f" • Niveau de charge : {batt.get('percent')}\n"
        formatted_text += f" • Alimentation secteur : {batt.get('isCharging')}\n"
        formatted_text += f" • Autonomie restante : {batt.get('lifetime')}\n"
        formatted_text += f" • Estimation d'usure : {batt.get('wearEstimation')}\n"
        formatted_text += f" • État de santé : {batt.get('health')}\n\n"

        os_info = diag_data.get("os", {})
        formatted_text += f"[SYSTÈME D'EXPLOITATION & SYSTEM UPTIME]\n"
        formatted_text += f" • OS : {os_info.get('distro')}\n"
        formatted_text += f" • Version : {os_info.get('version')}\n"
        formatted_text += f" • Architecture : {os_info.get('arch')}\n"
        formatted_text += f" • Nom d'hôte : {os_info.get('hostname')}\n"
        formatted_text += f" • Temps de fonctionnement (Uptime) : {os_info.get('uptime')}\n\n"

        net = diag_data.get("network", [])
        formatted_text += f"[RÉSEAU & INTERFACES INTERNET]\n"
        for n in net:
            formatted_text += f" • {n.get('iface')} [{n.get('status')}] : IP {n.get('ip')} | MAC {n.get('mac')} | Vitesse {n.get('speed')}\n"
            formatted_text += f"   - Trafic réseau : {n.get('io')}\n"

        self.textbox_diag.delete("1.0", "end")
        self.textbox_diag.insert("1.0", formatted_text)

    def get_data(self):
        return getattr(self, "auto_data", system_diag.get_system_diagnostics())
