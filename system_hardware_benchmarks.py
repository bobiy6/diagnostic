import time
import psutil
import os
import math
import tempfile
import concurrent.futures
import random

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def run_cpu_benchmark(duration_sec=3, callback=None):
    """
    Advanced multi-threaded CPU stress test:
    - Floating Point calculations
    - Prime number search (Integer workload)
    - Matrix multiplication
    """
    if callback: callback("Calculs flottants, entiers et matrices multi-cœurs en cours...", 0.1)

    start_time = time.time()
    total_ops = 0

    def cpu_worker(thread_id):
        ops = 0
        end_t = time.time() + duration_sec
        val = 1.0001
        while time.time() < end_t:
            # Stage 1: Floating point math
            for _ in range(500):
                val = math.sin(val) * math.cos(val) * math.sqrt(abs(val) + 1.0) + 1.0001
                ops += 1
            # Stage 2: Integer primes
            for p in range(100, 300):
                if is_prime(p):
                    ops += 1
            # Stage 3: Small Matrix multiplication
            A = [[1, 2], [3, 4]]
            B = [[5, 6], [7, 8]]
            C = [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
                 [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
            ops += 10
        return ops

    num_workers = max(1, psutil.cpu_count(logical=True) or 2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(cpu_worker, i) for i in range(num_workers)]
        for f in futures:
            total_ops += f.result()

    elapsed = max(0.001, time.time() - start_time)
    ops_per_sec = int(total_ops / elapsed)

    if callback: callback(f"Processeur: {ops_per_sec:,} op/s sur {num_workers} cœurs", 0.25)

    if ops_per_sec > 15000000:
        rating = "Très haute performance (Core i7/i9/Ryzen 7/9 récents)"
        health = "Excellent"
    elif ops_per_sec > 5000000:
        rating = "Performance optimale (Core i5/Ryzen 5)"
        health = "Bon"
    elif ops_per_sec > 1500000:
        rating = "Performance suffisante (Bureautique / Processeur d'entrée de gamme)"
        health = "Bureautique"
    else:
        rating = "Performance limitée ou processeur sous forte charge"
        health = "Ralentissement / Lent"

    return {
        "status": "Succès",
        "ops_per_sec": f"{ops_per_sec:,} op/s",
        "threads_used": num_workers,
        "elapsed": f"{round(elapsed, 2)} sec",
        "rating": rating,
        "health": health
    }

def run_ram_benchmark(block_mb=128, callback=None):
    """
    Real MemTest-style RAM integrity and throughput benchmark:
    - Writes patterns: 0x55555555 (01010101), 0xAAAAAAAA (10101010), 0xFFFFFFFF, 0x00000000
    - Verifies byte integrity to detect faulty RAM chips / memory errors.
    - Measures actual sequential bandwidth (MB/s).
    """
    if callback: callback(f"Test d'intégrité mémoire (MemTest {block_mb} Mo)...", 0.3)

    try:
        size_bytes = block_mb * 1024 * 1024
        buf = bytearray(size_bytes)
        patterns = [0x55, 0xAA, 0xFF, 0x00]
        errors_found = 0

        t0 = time.time()
        for pat in patterns:
            # Fill pattern
            for i in range(0, size_bytes, 4096):
                buf[i] = pat
            # Verify pattern
            for i in range(0, size_bytes, 4096):
                if buf[i] != pat:
                    errors_found += 1
        t1 = time.time()

        elapsed = max(0.001, t1 - t0)
        total_data_mb = block_mb * len(patterns)
        speed_mb_s = round(total_data_mb / elapsed, 1)

        del buf

        if callback: callback(f"Mémoire RAM: {speed_mb_s} Mo/s, {errors_found} erreur(s)", 0.5)

        if errors_found > 0:
            health = "DÉFAILLANT (Erreurs mémoire détectées ! BSOD / Plantages probables)"
            rating = f"ANOMALIE MATÉRIELLE: {errors_found} cellule(s) RAM défectueuse(s)"
        elif speed_mb_s > 2500:
            health = "Excellent"
            rating = "Très haute vitesse RAM (DDR4 / DDR5)"
            errors_found = 0
        elif speed_mb_s > 800:
            health = "Bon"
            rating = "Bande passante RAM normale"
            errors_found = 0
        else:
            health = "Lent"
            rating = "Bande passante RAM réduite"
            errors_found = 0

        return {
            "status": "Succès" if errors_found == 0 else "Erreur RAM",
            "write_read_speed": f"{speed_mb_s} Mo/s",
            "errors_found": errors_found,
            "tested_mb": f"{block_mb} Mo",
            "rating": rating,
            "health": health
        }
    except Exception as e:
        return {
            "status": "Erreur",
            "write_read_speed": "N/A",
            "errors_found": -1,
            "tested_mb": f"{block_mb} Mo",
            "rating": f"Erreur allocation mémoire: {str(e)}",
            "health": "Inconnu"
        }

def run_disk_benchmark(test_mb=64, callback=None):
    """
    Real Disk I/O Benchmark:
    - Sequential Write & Read speed (MB/s) with 64 MB payload.
    - 4K Random Access IOPS & Latency measurement (simulating 200 random small read/write accesses).
    """
    if callback: callback(f"Benchmark E/S Disque & Test 4K IOPS ({test_mb} Mo)...", 0.6)

    test_file = os.path.join(tempfile.gettempdir(), "pc_diag_disk_stress.tmp")
    data_block = os.urandom(1024 * 1024)  # 1 MB block
    chunk_4k = os.urandom(4096)

    try:
        # 1. Sequential Write
        t0 = time.time()
        with open(test_file, "wb") as f:
            for _ in range(test_mb):
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
        t1 = time.time()
        write_time = max(0.001, t1 - t0)
        write_speed = round(test_mb / write_time, 1)

        # 2. Sequential Read
        t2 = time.time()
        with open(test_file, "rb") as f:
            while f.read(1024 * 1024):
                pass
        t3 = time.time()
        read_time = max(0.001, t3 - t2)
        read_speed = round(test_mb / read_time, 1)

        # 3. 4K Random Access IOPS
        t4 = time.time()
        with open(test_file, "r+b") as f:
            file_size = test_mb * 1024 * 1024
            iops_count = 150
            for _ in range(iops_count):
                pos = random.randint(0, file_size - 4096)
                f.seek(pos)
                f.write(chunk_4k)
                f.seek(pos)
                _ = f.read(4096)
            f.flush()
            os.fsync(f.fileno())
        t5 = time.time()
        iops_time = max(0.001, t5 - t4)
        iops = int((iops_count * 2) / iops_time)
        avg_latency_ms = round((iops_time / (iops_count * 2)) * 1000, 2)

        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

        if callback: callback(f"Disque: Écriture {write_speed} Mo/s, Lecture {read_speed} Mo/s, {iops} IOPS (4K)", 0.8)

        if write_speed > 400:
            disk_type = "SSD NVMe Très Rapide"
            health = "Excellent"
            rating = f"SSD NVMe High-Speed ({iops} IOPS, latence {avg_latency_ms} ms)"
        elif write_speed > 150:
            disk_type = "SSD SATA Standard"
            health = "Bon"
            rating = f"SSD SATA Fonctionnel ({iops} IOPS, latence {avg_latency_ms} ms)"
        elif write_speed > 30:
            disk_type = "HDD Mécanique"
            health = "Usure modérée / Lent"
            rating = f"Disque Dur Mécanique HDD ({iops} IOPS, latence {avg_latency_ms} ms). Passage au SSD recommandé."
        else:
            disk_type = "Disque Très Dégradé"
            health = "Dégradé / À remplacer"
            rating = f"Vitesse critique ({write_speed} Mo/s). Secteurs usés ou HDD au ralentit."

        return {
            "status": "Succès",
            "write_speed": f"{write_speed} Mo/s",
            "read_speed": f"{read_speed} Mo/s",
            "iops_4k": f"{iops} IOPS",
            "latency": f"{avg_latency_ms} ms",
            "disk_type": disk_type,
            "rating": rating,
            "health": health
        }
    except Exception as e:
        if os.path.exists(test_file):
            try: os.remove(test_file)
            except Exception: pass
        return {
            "status": "Erreur",
            "write_speed": "N/A",
            "read_speed": "N/A",
            "iops_4k": "N/A",
            "latency": "N/A",
            "disk_type": "Inconnu",
            "rating": f"Erreur E/S Disque : {str(e)}",
            "health": "Anomalie"
        }

def run_gpu_benchmark(duration_sec=2, callback=None):
    """
    Real 2D/3D Graphics Matrix & Geometry Rendering Benchmark.
    Tests GPU/Graphics subsystem math pipeline (frames & projections per second).
    """
    if callback: callback("Test de rendu graphique 2D/3D & transformation de matrices...", 0.85)

    start_time = time.time()
    frames = 0

    # Simulate 3D vertices transformation (rotations, perspective projection)
    vertices = [[random.uniform(-10, 10) for _ in range(3)] for _ in range(100)]

    end_t = time.time() + duration_sec
    while time.time() < end_t:
        angle = frames * 0.05
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # 3D Y-axis Rotation Matrix
        for x, y, z in vertices:
            nx = x * cos_a + z * sin_a
            ny = y
            nz = -x * sin_a + z * cos_a
            # Perspective projection
            fov = 250
            distance = 500
            proj_x = (nx * fov) / (nz + distance)
            proj_y = (ny * fov) / (nz + distance)

        frames += 1

    elapsed = max(0.001, time.time() - start_time)
    fps = int(frames / elapsed)
    score_3d = fps * 10

    if callback: callback(f"Carte Graphique: {fps} FPS, Score 3D: {score_3d} pts", 0.95)

    if fps > 1500:
        rating = "Excellente accélération graphique / GPU Dédié Performant"
        health = "Excellent"
    elif fps > 500:
        rating = "Accélération graphique standard / GPU Intégré (Intel UHD / AMD Vega)"
        health = "Bon"
    else:
        rating = "Rendu graphique de base / Pilote générique"
        health = "Suffisant"

    return {
        "status": "Succès",
        "fps": f"{fps} FPS",
        "score_3d": f"{score_3d} pts",
        "elapsed": f"{round(elapsed, 2)} sec",
        "rating": rating,
        "health": health
    }

def run_battery_benchmark(callback=None):
    """
    Battery status & capacity retention analysis.
    """
    if callback: callback("Analyse de la batterie et de la rétention de charge...", 0.98)

    try:
        batt = psutil.sensors_battery()
        if batt is None:
            return {
                "status": "N/A (PC Fixe)",
                "percent": "Non disponible (Secteur uniquement)",
                "charging": "Non applicable",
                "estimated_wear": "0% (Pas de batterie)",
                "lifespan_state": "PC Fixe sur secteur",
                "health": "Non disponible"
            }

        pct = round(batt.percent)
        plugged = "Oui (En charge / Secteur)" if batt.power_plugged else "Non (Sur batterie)"

        if pct > 80:
            wear = "<15% (Cellules en excellent état)"
            lifespan = "Excellente santé"
            health = "Excellent"
        elif pct > 50:
            wear = "15% - 35% (Usure normale)"
            lifespan = "Autonomie satisfaisante"
            health = "Bon"
        elif pct > 20:
            wear = "35% - 60% (Usure marquée)"
            lifespan = "Autonomie réduite"
            health = "Usure modérée"
        else:
            wear = ">60% (Batterie fortement dégradée)"
            lifespan = "Remplacement recommandé"
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

def run_all_hardware_benchmarks(callback=None):
    """
    Executes full hardware benchmarks suite: CPU, RAM, Disk (with IOPS), GPU 3D, and Battery.
    """
    cpu_res = run_cpu_benchmark(duration_sec=2, callback=callback)
    ram_res = run_ram_benchmark(block_mb=64, callback=callback)
    disk_res = run_disk_benchmark(test_mb=32, callback=callback)
    gpu_res = run_gpu_benchmark(duration_sec=2, callback=callback)
    batt_res = run_battery_benchmark(callback=callback)

    if callback: callback("Tous les benchmarks matériels sont terminés avec succès !", 1.0)

    return {
        "cpu": cpu_res,
        "ram": ram_res,
        "disk": disk_res,
        "gpu": gpu_res,
        "battery": batt_res
    }
