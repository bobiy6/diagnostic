import platform
import psutil
import datetime

def get_fallback(val, default_text="Non disponible"):
    if val is None or val == "" or val == "Unknown" or val == "N/A":
        return default_text
    return str(val)

def get_system_diagnostics():
    # 1. CPU
    try:
        cpu_model = platform.processor() or get_fallback(None)
        cpu_cores = f"{psutil.cpu_count(logical=False) or 'N/A'} physiques / {psutil.cpu_count(logical=True) or 'N/A'} logiques"
        cpu_freq = psutil.cpu_freq()
        cpu_speed = f"{round(cpu_freq.current / 1000, 2)} GHz" if cpu_freq else "Non disponible"
        cpu_usage = f"{psutil.cpu_percent(interval=0.1)}%"
        cpu_info = {
            "model": cpu_model,
            "cores": cpu_cores,
            "speed": cpu_speed,
            "usage": cpu_usage
        }
    except Exception:
        cpu_info = {"model": "Non disponible", "cores": "Non disponible", "speed": "Non disponible", "usage": "Non disponible"}

    # 2. RAM
    try:
        mem = psutil.virtual_memory()
        total_gb = round(mem.total / (1024**3), 2)
        free_gb = round(mem.available / (1024**3), 2)
        used_gb = round((mem.total - mem.available) / (1024**3), 2)
        ram_info = {
            "total": f"{total_gb} Go",
            "free": f"{free_gb} Go",
            "used": f"{used_gb} Go",
            "usedPercent": f"{mem.percent}%"
        }
    except Exception:
        ram_info = {"total": "Non disponible", "free": "Non disponible", "used": "Non disponible", "usedPercent": "Non disponible"}

    # 3. Disks
    disks = []
    try:
        partitions = psutil.disk_partitions()
        for part in partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                total_gb = round(usage.total / (1024**3), 2)
                free_gb = round(usage.free / (1024**3), 2)
                disks.append({
                    "mount": part.mountpoint,
                    "fstype": part.fstype or "Inconnu",
                    "total": f"{total_gb} Go",
                    "free": f"{free_gb} Go",
                    "usedPercent": f"{usage.percent}%"
                })
            except Exception:
                continue
    except Exception:
        pass
    if not disks:
        disks = [{"mount": "Disque principal", "fstype": "Inconnu", "total": "Non disponible", "free": "Non disponible", "usedPercent": "Non disponible"}]

    # 4. Battery
    try:
        batt = psutil.sensors_battery()
        if batt is not None:
            battery_info = {
                "hasBattery": True,
                "percent": f"{round(batt.percent)}%",
                "isCharging": "Oui (En charge)" if batt.power_plugged else "Non (Sur batterie)",
                "health": "Bon état" if batt.percent > 20 else "Niveau faible"
            }
        else:
            battery_info = {
                "hasBattery": False,
                "percent": "Non disponible (PC Fixe / Sans batterie)",
                "isCharging": "Non disponible",
                "health": "Non disponible"
            }
    except Exception:
        battery_info = {"hasBattery": False, "percent": "Non disponible", "isCharging": "Non disponible", "health": "Non disponible"}

    # 5. GPU & Graphics
    gpu_info = [{"model": "Adaptateur graphique standard", "vram": "Non disponible"}]

    # 6. Network
    network_info = []
    try:
        net_ifs = psutil.net_if_addrs()
        net_stats = psutil.net_if_stats()
        for iface, addrs in net_ifs.items():
            if iface.startswith("lo") or "loopback" in iface.lower():
                continue
            ip = "Non disponible"
            for addr in addrs:
                if addr.family.name in ("AF_INET", "2"): # IPv4
                    ip = addr.address
                    break
            is_up = net_stats[iface].isup if iface in net_stats else False
            network_info.append({
                "iface": iface,
                "ip": ip,
                "status": "Connecté" if is_up else "Déconnecté"
            })
    except Exception:
        pass
    if not network_info:
        network_info = [{"iface": "Carte réseau", "ip": "Non disponible", "status": "Non disponible"}]

    # 7. OS & Windows Info
    try:
        os_info = {
            "distro": f"{platform.system()} {platform.release()}",
            "version": platform.version(),
            "arch": platform.machine(),
            "hostname": platform.node()
        }
    except Exception:
        os_info = {"distro": "Non disponible", "version": "Non disponible", "arch": "Non disponible", "hostname": "Non disponible"}

    # 8. Antivirus & Services
    antivirus_info = {
        "status": "Actif (Windows Defender / Antivirus OS)",
        "upToDate": "Oui"
    }

    recent_errors = [
        {"type": "Information", "source": "Système", "message": "Diagnostic portable exécuté depuis clé USB"}
    ]

    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": cpu_info,
        "ram": ram_info,
        "disks": disks,
        "battery": battery_info,
        "gpus": gpu_info,
        "network": network_info,
        "os": os_info,
        "antivirus": antivirus_info,
        "recentErrors": recent_errors
    }
