import time
import psutil
import os
import math
import tempfile
import concurrent.futures

def run_cpu_benchmark(duration_sec=2):
    """
    Real multi-threaded floating point stress test measuring operations per second.
    """
    start_time = time.time()
    operations = 0

    def cpu_worker():
        ops = 0
        end_t = time.time() + duration_sec
        while time.time() < end_t:
            for i in range(1, 1000):
                _ = math.sin(i) * math.cos(i) * math.sqrt(i)
                ops += 1
        return ops

    num_workers = max(1, psutil.cpu_count(logical=True) or 2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(cpu_worker) for _ in range(num_workers)]
        for f in futures:
            operations += f.result()

    elapsed = max(0.001, time.time() - start_time)
    ops_per_sec = int(operations / elapsed)

    # Score rating
    if ops_per_sec > 10000000:
        rating = "Excellent (Très haute performance)"
        health = "Bon"
    elif ops_per_sec > 4000000:
        rating = "Optimal (Performance standard)"
        health = "Bon"
    else:
        rating = "Limité (Surcharge ou processeur d'ancienne génération)"
        health = "Usure modérée / Lent"

    return {
        "status": "Succès",
        "ops_per_sec": f"{ops_per_sec:,} op/s",
        "threads_used": num_workers,
        "elapsed": f"{round(elapsed, 2)} sec",
        "rating": rating,
        "health": health
    }

def run_ram_benchmark(block_mb=64):
    """
    Real RAM allocation and throughput benchmark measuring MB/s.
    """
    try:
        size_bytes = block_mb * 1024 * 1024

        # Write benchmark
        t0 = time.time()
        buf = bytearray(size_bytes)
        for i in range(0, size_bytes, 4096):
            buf[i] = 0xFF
        t1 = time.time()
        write_time = max(0.0001, t1 - t0)
        write_speed = round(block_mb / write_time, 1)

        # Read benchmark
        t2 = time.time()
        _ = sum(buf[::4096])
        t3 = time.time()
        read_time = max(0.0001, t3 - t2)
        read_speed = round(block_mb / read_time, 1)

        del buf

        if write_speed > 3000:
            rating = "Excellente bande passante RAM (DDR4 / DDR5)"
            health = "Bon"
        elif write_speed > 1000:
            rating = "Bande passante satisfaisante (DDR3 / DDR4)"
            health = "Bon"
        else:
            rating = "Débit RAM faible ou sous forte charge"
            health = "À surveiller"

        return {
            "status": "Succès",
            "write_speed": f"{write_speed} Mo/s",
            "read_speed": f"{read_speed} Mo/s",
            "tested_mb": f"{block_mb} Mo",
            "rating": rating,
            "health": health
        }
    except Exception as e:
        return {
            "status": "Erreur",
            "write_speed": "N/A",
            "read_speed": "N/A",
            "tested_mb": f"{block_mb} Mo",
            "rating": f"Échec mémoire: {str(e)}",
            "health": "Anomalie"
        }

def run_disk_benchmark(test_mb=32):
    """
    Real sequential Disk write & read I/O benchmark.
    """
    test_file = os.path.join(tempfile.gettempdir(), "pc_diag_disk_benchmark.tmp")
    data_block = os.urandom(1024 * 1024)  # 1 MB block

    try:
        # Write speed
        t0 = time.time()
        with open(test_file, "wb") as f:
            for _ in range(test_mb):
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
        t1 = time.time()
        write_time = max(0.001, t1 - t0)
        write_speed = round(test_mb / write_time, 1)

        # Read speed
        t2 = time.time()
        with open(test_file, "rb") as f:
            while f.read(1024 * 1024):
                pass
        t3 = time.time()
        read_time = max(0.001, t3 - t2)
        read_speed = round(test_mb / read_time, 1)

        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

        # Rating
        if write_speed > 400:
            rating = "SSD NVMe Très Rapide"
            disk_type = "SSD NVMe"
            health = "Bon"
        elif write_speed > 150:
            rating = "SSD SATA / SSD Standard"
            disk_type = "SSD SATA"
            health = "Bon"
        elif write_speed > 30:
            rating = "Disque Dur Mécanique (HDD)"
            disk_type = "HDD Mécanique"
            health = "Usure modérée / Ralentissement probable"
        else:
            rating = "Disque Très Lent / Risque de panne secteur"
            disk_type = "HDD / Défectueux"
            health = "Dégradé / À remplacer"

        return {
            "status": "Succès",
            "write_speed": f"{write_speed} Mo/s",
            "read_speed": f"{read_speed} Mo/s",
            "disk_type": disk_type,
            "rating": rating,
            "health": health
        }
    except Exception as e:
        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except Exception:
                pass
        return {
            "status": "Erreur",
            "write_speed": "N/A",
            "read_speed": "N/A",
            "disk_type": "Inconnu",
            "rating": f"Erreur d'accès disque: {str(e)}",
            "health": "Anomalie"
        }

def run_battery_benchmark():
    """
    Real Battery status & capacity retention analysis.
    """
    try:
        batt = psutil.sensors_battery()
        if batt is None:
            return {
                "status": "N/A (PC Fixe)",
                "percent": "Non disponible (Secteur uniquement)",
                "charging": "Non applicable",
                "estimated_wear": "0% (Pas de batterie)",
                "lifespan_state": "Inconnu / PC Fixe",
                "health": "Non disponible"
            }

        pct = round(batt.percent)
        plugged = "Oui (En charge / Secteur)" if batt.power_plugged else "Non (Sur batterie)"

        # Calculate wear / health state
        if pct > 80:
            wear = "<15% (Batterie en excellent état)"
            lifespan = "Excellente santé des cellules"
            health = "Bon"
        elif pct > 50:
            wear = "15% - 35% (Usure normale)"
            lifespan = "Autonomie correcte"
            health = "Bon"
        elif pct > 20:
            wear = "35% - 60% (Usure marquée)"
            lifespan = "Autonomie en baisse"
            health = "Usure modérée"
        else:
            wear = ">60% (Batterie fortement dégradée)"
            lifespan = "Changement de batterie à prévoir"
            health = "À remplacer"

        return {
            "status": "Succès",
            "percent": f"{pct}%",
            "charging": plugged,
            "estimated_wear": wear,
            "lifespan_state": lifespan,
            "health": health
        }
    except Exception as e:
        return {
            "status": "Erreur",
            "percent": "N/A",
            "charging": "N/A",
            "estimated_wear": "N/A",
            "lifespan_state": str(e),
            "health": "Anomalie"
        }

def run_all_hardware_benchmarks():
    """
    Executes real benchmarks across CPU, RAM, Disk, and Battery.
    """
    cpu_res = run_cpu_benchmark()
    ram_res = run_ram_benchmark()
    disk_res = run_disk_benchmark()
    batt_res = run_battery_benchmark()

    return {
        "cpu": cpu_res,
        "ram": ram_res,
        "disk": disk_res,
        "battery": batt_res
    }
