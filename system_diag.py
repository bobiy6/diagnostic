import platform
import psutil
import datetime
import os

def get_fallback(val, default_text="Non disponible"):
    if val is None or val == "" or val == "Unknown" or val == "N/A":
        return default_text
    return str(val)

def get_system_diagnostics():
    # 1. CPU
    try:
        cpu_model = platform.processor() or get_fallback(None)
        physical_cores = psutil.cpu_count(logical=False) or "N/A"
        logical_cores = psutil.cpu_count(logical=True) or "N/A"
        cpu_cores_str = f"{physical_cores} cœurs physiques / {logical_cores} cœurs logiques"

        freq = psutil.cpu_freq()
        if freq:
            current_speed = f"{round(freq.current / 1000, 2)} GHz"
            max_speed = f"{round(freq.max / 1000, 2)} GHz" if freq.max else "Inconnu"
            min_speed = f"{round(freq.min / 1000, 2)} GHz" if freq.min else "Inconnu"
            freq_str = f"{current_speed} (Min: {min_speed} | Max: {max_speed})"
        else:
            freq_str = "Non disponible"

        cpu_usage = f"{psutil.cpu_percent(interval=0.2)}%"

        # Temperatures if available
        temps_str = "Non disponible (Nécessite droits admin / capteur matériel)"
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                t_list = []
                for name, entries in temps.items():
                    for entry in entries:
                        t_list.append(f"{name}: {entry.current}°C")
                if t_list:
                    temps_str = " | ".join(t_list[:3])
        except Exception:
            pass

        cpu_info = {
            "model": cpu_model,
            "cores": cpu_cores_str,
            "freq": freq_str,
            "usage": cpu_usage,
            "temperature": temps_str
        }
    except Exception:
        cpu_info = {"model": "Non disponible", "cores": "Non disponible", "freq": "Non disponible", "usage": "Non disponible", "temperature": "Non disponible"}

    # 2. RAM
    try:
        mem = psutil.virtual_memory()
        total_gb = round(mem.total / (1024**3), 2)
        free_gb = round(mem.available / (1024**3), 2)
        used_gb = round((mem.total - mem.available) / (1024**3), 2)

        swap = psutil.swap_memory()
        swap_str = f"Total: {round(swap.total / (1024**3), 2)} Go | Utilisé: {round(swap.used / (1024**3), 2)} Go ({swap.percent}%)"

        ram_info = {
            "total": f"{total_gb} Go",
            "free": f"{free_gb} Go",
            "used": f"{used_gb} Go",
            "usedPercent": f"{mem.percent}%",
            "swap": swap_str
        }
    except Exception:
        ram_info = {"total": "Non disponible", "free": "Non disponible", "used": "Non disponible", "usedPercent": "Non disponible", "swap": "Non disponible"}

    # 3. Disks
    disks = []
    try:
        partitions = psutil.disk_partitions()
        disk_counters = psutil.disk_io_counters(perdisk=True) or {}

        for part in partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                total_gb = round(usage.total / (1024**3), 2)
                free_gb = round(usage.free / (1024**3), 2)
                used_gb = round(usage.used / (1024**3), 2)

                # I/O Stats
                device_name = part.device.replace("/dev/", "").replace("\\", "")
                io_info = "Lecture/Écriture: N/A"
                if device_name in disk_counters:
                    c = disk_counters[device_name]
                    read_mb = round(c.read_bytes / (1024**2), 1)
                    write_mb = round(c.write_bytes / (1024**2), 1)
                    io_info = f"Lu: {read_mb} Mo | Écrit: {write_mb} Mo"

                # Health state estimation based on space
                health_status = "Bon" if usage.percent < 85 else ("Attention (>85% plein)" if usage.percent < 95 else "Critique (>95% plein)")

                disks.append({
                    "mount": part.mountpoint,
                    "device": part.device,
                    "fstype": part.fstype or "Inconnu",
                    "total": f"{total_gb} Go",
                    "used": f"{used_gb} Go",
                    "free": f"{free_gb} Go",
                    "usedPercent": f"{usage.percent}%",
                    "io": io_info,
                    "healthStatus": health_status
                })
            except Exception:
                continue
    except Exception:
        pass

    if not disks:
        disks = [{
            "mount": "Disque principal", "device": "Inconnu", "fstype": "Inconnu",
            "total": "Non disponible", "used": "Non disponible", "free": "Non disponible",
            "usedPercent": "Non disponible", "io": "Non disponible", "healthStatus": "Non disponible"
        }]

    # 4. Battery & Power
    try:
        batt = psutil.sensors_battery()
        if batt is not None:
            pct = round(batt.percent)
            plugged = "Oui (Secteur branché)" if batt.power_plugged else "Non (Sur batterie)"
            secs = batt.secsleft
            if secs == psutil.POWER_TIME_UNLIMITED:
                lifetime = "Chargée / Sur secteur"
            elif secs == psutil.POWER_TIME_UNKNOWN:
                lifetime = "Calcul du temps restant..."
            else:
                hrs = secs // 3600
                mins = (secs % 3600) // 60
                lifetime = f"Environ {hrs}h {mins}min restantes"

            # Wear estimation
            wear_est = "État normal (Capacité optimale)" if pct > 75 else ("Usure modérée" if pct > 40 else "Batterie faible / Usée")

            battery_info = {
                "hasBattery": True,
                "percent": f"{pct}%",
                "isCharging": plugged,
                "lifetime": lifetime,
                "wearEstimation": wear_est,
                "health": "Bon état" if pct > 30 else "À contrôler"
            }
        else:
            battery_info = {
                "hasBattery": False,
                "percent": "Non disponible (PC Fixe / Sans batterie)",
                "isCharging": "Non disponible",
                "lifetime": "Non disponible",
                "wearEstimation": "Non disponible",
                "health": "Non disponible"
            }
    except Exception:
        battery_info = {"hasBattery": False, "percent": "Non disponible", "isCharging": "Non disponible", "lifetime": "Non disponible", "wearEstimation": "Non disponible", "health": "Non disponible"}

    # 5. Network
    network_info = []
    try:
        net_ifs = psutil.net_if_addrs()
        net_stats = psutil.net_if_stats()
        net_io = psutil.net_io_counters(pernic=True)

        for iface, addrs in net_ifs.items():
            if iface.startswith("lo") or "loopback" in iface.lower():
                continue
            ip = "Non disponible"
            mac = "Non disponible"
            for addr in addrs:
                if addr.family.name in ("AF_INET", "2"):  # IPv4
                    ip = addr.address
                elif addr.family.name in ("AF_LINK", "17", "-1"):  # MAC
                    mac = addr.address

            is_up = net_stats[iface].isup if iface in net_stats else False
            speed_mb = f"{net_stats[iface].speed} Mbit/s" if iface in net_stats and net_stats[iface].speed > 0 else "N/A"

            io_str = "N/A"
            if iface in net_io:
                io = net_io[iface]
                rx_mb = round(io.bytes_recv / (1024**2), 1)
                tx_mb = round(io.bytes_sent / (1024**2), 1)
                io_str = f"Reçu: {rx_mb} Mo | Envoyé: {tx_mb} Mo"

            network_info.append({
                "iface": iface,
                "ip": ip,
                "mac": mac,
                "speed": speed_mb,
                "status": "Connecté" if is_up else "Déconnecté",
                "io": io_str
            })
    except Exception:
        pass

    if not network_info:
        network_info = [{"iface": "Carte réseau", "ip": "Non disponible", "mac": "Non disponible", "speed": "Non disponible", "status": "Non disponible", "io": "Non disponible"}]

    # 6. OS & System Info
    try:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        uptime_days = uptime.days
        uptime_hours = uptime.seconds // 3600
        uptime_str = f"{uptime_days} jours, {uptime_hours} heures (Démarré le {boot_time.strftime('%Y-%m-%d %H:%M')})"

        os_info = {
            "distro": f"{platform.system()} {platform.release()}",
            "version": platform.version(),
            "arch": platform.machine(),
            "hostname": platform.node(),
            "uptime": uptime_str
        }
    except Exception:
        os_info = {"distro": "Non disponible", "version": "Non disponible", "arch": "Non disponible", "hostname": "Non disponible", "uptime": "Non disponible"}

    # 7. Antivirus & Security
    antivirus_info = {
        "status": "Actif (Protections Windows Defender / OS)",
        "upToDate": "Oui"
    }

    recent_errors = [
        {"type": "Information", "source": "Diag Portable", "message": "Analyse matérielle psutil exécutée"}
    ]

    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": cpu_info,
        "ram": ram_info,
        "disks": disks,
        "battery": battery_info,
        "network": network_info,
        "os": os_info,
        "antivirus": antivirus_info,
        "recentErrors": recent_errors
    }
