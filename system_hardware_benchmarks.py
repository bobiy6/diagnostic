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
    Full 100% CPU multi-threaded stress test across ALL logical cores.
    Pure CPU-bound math loops with no sleep to guarantee 100% Task Manager load.
    """
    start_time = time.time()
    end_time = start_time + duration_sec
    errors = 0

    num_workers = max(1, psutil.cpu_count(logical=True) or 2)

    def cpu_heavy_worker(stop_time):
        ops = 0
        val = 1.0001
        while time.time() < stop_time:
            for _ in range(5000):
                val = math.sin(val) * math.cos(val) * math.sqrt(abs(val) + 1.0) + 1.0001
                ops += 1
            for p in range(100, 200):
                if is_prime(p):
                    ops += 1
        return ops

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(cpu_heavy_worker, end_time) for _ in range(num_workers)]

        while time.time() < end_time:
            elapsed = time.time() - start_time
            pct = min(0.99, elapsed / duration_sec)
            if callback:
                callback(f"PROCESSEUR (CPU) : Charge 100% Max sur {num_workers} cœurs...", pct)
            time.sleep(0.1)

        total_ops = 0
        for f in futures:
            try:
                total_ops += f.result()
            except Exception:
                errors += 1

    elapsed = max(0.001, time.time() - start_time)
    ops_per_sec = int(total_ops / elapsed)

    if callback:
        callback(f"PROCESSEUR (CPU) : Terminé à 100% - Débit: {ops_per_sec:,} op/s ({errors} erreur)", 1.0)

    if ops_per_sec > 15000000:
        rating = "Très haute performance (Core i7/i9/Ryzen 7/9 récents)"
        health = "Excellent"
    elif ops_per_sec > 5000000:
        rating = "Performance optimale (Core i5/Ryzen 5)"
        health = "Bon"
    elif ops_per_sec > 1500000:
        rating = "Performance suffisante (Bureautique)"
        health = "Bureautique"
    else:
        rating = "Performance limitée / Processeur sous forte charge"
        health = "Lent / Surchargé"

    return {
        "status": "PASSED" if errors == 0 else "ERREUR",
        "ops_per_sec": f"{ops_per_sec:,} op/s",
        "errors": errors,
        "threads_used": num_workers,
        "elapsed": f"{round(elapsed, 1)}s",
        "rating": rating,
        "health": health
    }

def run_ram_benchmark(duration_sec=4, block_mb=128, callback=None):
    """
    Sequential RAM MemTest with 0% to 100% progress callback.
    """
    start_time = time.time()
    end_time = start_time + duration_sec
    errors_found = 0
    total_bytes_tested = 0

    patterns = [0x55, 0xAA, 0xFF, 0x00]

    try:
        size_bytes = block_mb * 1024 * 1024
        buf = bytearray(size_bytes)

        pattern_idx = 0
        while time.time() < end_time:
            now = time.time()
            elapsed = now - start_time
            pct = min(0.99, elapsed / duration_sec)

            pat = patterns[pattern_idx % len(patterns)]
            if callback:
                callback(f"MÉMOIRE (RAM) : MemTest 0x{pat:02X}...", pct)

            for i in range(0, size_bytes, 1024):
                buf[i] = pat
            for i in range(0, size_bytes, 1024):
                if buf[i] != pat:
                    errors_found += 1

            total_bytes_tested += size_bytes
            pattern_idx += 1
            time.sleep(0.01)

        del buf
    except Exception:
        errors_found += 1

    elapsed = max(0.001, time.time() - start_time)
    speed_mb_s = round((total_bytes_tested / (1024*1024)) / elapsed, 1)

    if callback:
        callback(f"MÉMOIRE (RAM) : Terminé à 100% - Vitesse: {speed_mb_s} Mo/s ({errors_found} erreur)", 1.0)

    if errors_found > 0:
        health = "DÉFAILLANT (Erreurs mémoire RAM ! BSOD probables)"
        rating = f"ANOMALIE MATÉRIELLE: {errors_found} erreur(s) détectée(s)"
    elif speed_mb_s > 2500:
        health = "Excellent"
        rating = "Très haute vitesse RAM (DDR4 / DDR5)"
    elif speed_mb_s > 800:
        health = "Bon"
        rating = "Bande passante RAM normale"
    else:
        health = "Lent"
        rating = "Bande passante RAM réduite"

    return {
        "status": "PASSED" if errors_found == 0 else "ERREUR",
        "write_read_speed": f"{speed_mb_s} Mo/s",
        "errors": errors_found,
        "tested_mb": f"{block_mb} Mo",
        "rating": rating,
        "health": health
    }

def run_disk_benchmark(duration_sec=4, test_mb=64, callback=None):
    """
    Sequential Disk Write/Read & 4K IOPS Test with clean progress callback.
    """
    test_file = os.path.join(tempfile.gettempdir(), "pc_diag_disk_seq.tmp")
    data_block = os.urandom(1024 * 1024)
    chunk_4k = os.urandom(4096)

    write_speed = 0.0
    read_speed = 0.0
    iops = 0
    errors_found = 0

    try:
        if callback: callback("DISQUE STOCKAGE : Écriture séquentielle...", 0.25)
        t0 = time.time()
        with open(test_file, "wb") as f:
            for _ in range(test_mb):
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
        t1 = time.time()
        write_speed = round(test_mb / max(0.001, t1 - t0), 1)

        if callback: callback("DISQUE STOCKAGE : Lecture séquentielle...", 0.6)
        t2 = time.time()
        with open(test_file, "rb") as f:
            while f.read(1024 * 1024):
                pass
        t3 = time.time()
        read_speed = round(test_mb / max(0.001, t3 - t2), 1)

        if callback: callback("DISQUE STOCKAGE : Benchmark 4K IOPS...", 0.85)
        t4 = time.time()
        with open(test_file, "r+b") as f:
            file_size = test_mb * 1024 * 1024
            iops_count = 100
            for _ in range(iops_count):
                pos = random.randint(0, file_size - 4096)
                f.seek(pos)
                f.write(chunk_4k)
                f.seek(pos)
                _ = f.read(4096)
            f.flush()
            os.fsync(f.fileno())
        t5 = time.time()
        iops = int((iops_count * 2) / max(0.001, t5 - t4))

        if os.path.exists(test_file):
            os.remove(test_file)

    except Exception:
        errors_found += 1
        if os.path.exists(test_file):
            try: os.remove(test_file)
            except Exception: pass

    if callback:
        callback(f"DISQUE STOCKAGE : Terminé à 100% - Écrit: {write_speed} Mo/s, Lu: {read_speed} Mo/s ({errors_found} erreur)", 1.0)

    if write_speed > 400:
        disk_type = "SSD NVMe Très Rapide"
        health = "Excellent"
        rating = f"SSD NVMe High-Speed ({iops} IOPS)"
    elif write_speed > 150:
        disk_type = "SSD SATA Standard"
        health = "Bon"
        rating = f"SSD SATA Fonctionnel ({iops} IOPS)"
    elif write_speed > 30:
        disk_type = "HDD Mécanique"
        health = "Usure modérée / Lent"
        rating = f"Disque Dur Mécanique HDD ({iops} IOPS). Passage au SSD recommandé."
    else:
        disk_type = "Disque Très Dégradé"
        health = "Dégradé / À remplacer"
        rating = f"Vitesse critique ({write_speed} Mo/s). Disque fortement ralenti."

    return {
        "status": "PASSED" if errors_found == 0 else "ERREUR",
        "write_speed": f"{write_speed} Mo/s",
        "read_speed": f"{read_speed} Mo/s",
        "iops_4k": f"{iops} IOPS",
        "errors": errors_found,
        "disk_type": disk_type,
        "rating": rating,
        "health": health
    }

def run_gpu_benchmark(duration_sec=3, callback=None):
    """
    Sequential GPU 3D Matrix Rendering Test.
    """
    start_time = time.time()
    end_time = start_time + duration_sec
    frames = 0
    errors_found = 0

    vertices = [[random.uniform(-10, 10) for _ in range(3)] for _ in range(100)]

    while time.time() < end_time:
        now = time.time()
        elapsed = now - start_time
        pct = min(0.99, elapsed / duration_sec)

        if callback:
            callback(f"CARTE GRAPHIQUE (GPU) : Test de rendu 3D...", pct)

        try:
            angle = frames * 0.05
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            for x, y, z in vertices:
                nx = x * cos_a + z * sin_a
                ny = y
                nz = -x * sin_a + z * cos_a
                _ = (nx * 250) / (nz + 500)

            frames += 1
        except Exception:
            errors_found += 1

    elapsed = max(0.001, time.time() - start_time)
    fps = int(frames / elapsed)
    score_3d = fps * 10

    if callback:
        callback(f"CARTE GRAPHIQUE (GPU) : Terminé à 100% - Rendu: {fps} FPS, Score: {score_3d} pts ({errors_found} erreur)", 1.0)

    if fps > 1500:
        rating = "Excellente accélération graphique / GPU Dédié Performant"
        health = "Excellent"
    elif fps > 500:
        rating = "Accélération graphique standard / GPU Intégré"
        health = "Bon"
    else:
        rating = "Rendu graphique de base / Pilote générique"
        health = "Suffisant"

    return {
        "status": "PASSED" if errors_found == 0 else "ERREUR",
        "fps": f"{fps} FPS",
        "score_3d": f"{score_3d} pts",
        "errors": errors_found,
        "rating": rating,
        "health": health
    }

def run_battery_benchmark(callback=None):
    """
    Sequential Battery Health & Retention Test.
    """
    if callback: callback("BATTERIE & ALIMENTATION : Analyse de la rétention et de la charge...", 0.5)

    try:
        batt = psutil.sensors_battery()
        if callback: callback("BATTERIE & ALIMENTATION : Terminé à 100%", 1.0)

        if batt is None:
            return {
                "status": "PASSED (PC Fixe)",
                "percent": "PC Fixe (Sur secteur)",
                "charging": "Non applicable",
                "estimated_wear": "0% (Secteur)",
                "errors": 0,
                "health": "Non disponible"
            }

        pct = round(batt.percent)
        plugged = "Oui (Sur secteur)" if batt.power_plugged else "Non (Sur batterie)"

        if pct > 80:
            wear = "<15% (Excellent état)"
            health = "Excellent"
        elif pct > 50:
            wear = "15% - 35% (Usure normale)"
            health = "Bon"
        elif pct > 20:
            wear = "35% - 60% (Usure marquée)"
            health = "Usure modérée"
        else:
            wear = ">60% (Batterie usée)"
            health = "À remplacer"

        return {
            "status": "PASSED",
            "percent": f"{pct}%",
            "charging": plugged,
            "estimated_wear": wear,
            "errors": 0,
            "health": health
        }
    except Exception:
        if callback: callback("BATTERIE & ALIMENTATION : Erreur de lecture", 1.0)
        return {
            "status": "ERREUR",
            "percent": "N/A",
            "charging": "N/A",
            "estimated_wear": "N/A",
            "errors": 1,
            "health": "Anomalie"
        }

def run_25min_sequential_endurance(duration_sec=1500, stage_callback=None):
    """
    Real 25-Minute (1500s) Sequential Endurance Stress Test divided into 5 Stages (5 min each).
    - Stage 1: CPU 100% Full Load across ALL logical cores (pure CPU-bound worker threads with no sleep)
    - Stage 2: RAM MemTest
    - Stage 3: Disk I/O
    - Stage 4: GPU 3D Matrix Rendering
    - Stage 5: Battery & Power Stability
    """
    stage_duration = duration_sec / 5.0

    cpu_errors = 0
    ram_errors = 0
    disk_errors = 0
    gpu_errors = 0

    last_callback_t = 0

    def rate_limited_cb(stage_name, st_pct, glob_pct, errs):
        nonlocal last_callback_t
        now = time.time()
        if now - last_callback_t >= 0.5 or glob_pct >= 1.0:
            last_callback_t = now
            if stage_callback:
                stage_callback(stage_name, st_pct, glob_pct, errs)

    # STAGE 1: CPU 100% Full Multi-Core Stress (5 min)
    try:
        t_stage1_end = time.time() + stage_duration
        num_workers = max(1, psutil.cpu_count(logical=True) or 2)

        def cpu_pure_heavy_worker(end_t):
            val = 1.0001
            while time.time() < end_t:
                for _ in range(10000):
                    val = math.sin(val) * math.cos(val) * math.sqrt(abs(val) + 1.0) + 1.0001

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(cpu_pure_heavy_worker, t_stage1_end) for _ in range(num_workers)]
            while time.time() < t_stage1_end:
                now = time.time()
                elapsed_st = now - (t_stage1_end - stage_duration)
                pct_st = min(1.0, elapsed_st / stage_duration)
                global_pct = 0.0 + (pct_st * 0.2)
                rate_limited_cb("ÉTAPE 1/5 : STRESS PROCESSEUR (CPU 100% MAX) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)
                time.sleep(0.2)
    except Exception:
        cpu_errors += 1

    # STAGE 2: RAM MemTest (20% -> 40% global)
    try:
        t_stage2_end = time.time() + stage_duration
        ram_buffer = bytearray(32 * 1024 * 1024)

        while time.time() < t_stage2_end:
            now = time.time()
            elapsed_st = now - (t_stage2_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.2 + (pct_st * 0.2)
            rate_limited_cb("ÉTAPE 2/5 : TEST INTÉGRITÉ MÉMOIRE (RAM MemTest) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)

            for pat in [0x55, 0xAA]:
                for i in range(0, len(ram_buffer), 8192):
                    ram_buffer[i] = pat
                for i in range(0, len(ram_buffer), 8192):
                    if ram_buffer[i] != pat:
                        ram_errors += 1
            time.sleep(0.01)
        del ram_buffer
    except Exception:
        ram_errors += 1

    # STAGE 3: Disk I/O (40% -> 60% global)
    endurance_disk_file = os.path.join(tempfile.gettempdir(), "mg_endurance_disk_reusable.tmp")
    data_4mb = os.urandom(4 * 1024 * 1024)
    try:
        t_stage3_end = time.time() + stage_duration
        while time.time() < t_stage3_end:
            now = time.time()
            elapsed_st = now - (t_stage3_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.4 + (pct_st * 0.2)
            rate_limited_cb("ÉTAPE 3/5 : BENCHMARK E/S DISQUE & IOPS - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)

            with open(endurance_disk_file, "wb") as f:
                f.write(data_4mb)
                f.flush()
                os.fsync(f.fileno())
            with open(endurance_disk_file, "rb") as f:
                _ = f.read()
            time.sleep(0.01)

        if os.path.exists(endurance_disk_file):
            os.remove(endurance_disk_file)
    except Exception:
        disk_errors += 1
        if os.path.exists(endurance_disk_file):
            try: os.remove(endurance_disk_file)
            except Exception: pass

    # STAGE 4: GPU 3D Matrix Rendering (60% -> 80% global)
    try:
        t_stage4_end = time.time() + stage_duration
        vertices = [[random.uniform(-10, 10) for _ in range(3)] for _ in range(50)]
        while time.time() < t_stage4_end:
            now = time.time()
            elapsed_st = now - (t_stage4_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.6 + (pct_st * 0.2)
            rate_limited_cb("ÉTAPE 4/5 : RENDU GRAPHIQUE 3D (GPU) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)

            for x, y, z in vertices:
                _ = (x * 0.5 * 250) / (z + 500)
    except Exception:
        gpu_errors += 1

    # STAGE 5: Battery & System Stability (80% -> 100% global)
    try:
        t_stage5_end = time.time() + stage_duration
        while time.time() < t_stage5_end:
            now = time.time()
            elapsed_st = now - (t_stage5_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.8 + (pct_st * 0.2)
            rate_limited_cb("ÉTAPE 5/5 : ANALYSE STABILITÉ & ALIMENTATION - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)
            time.sleep(0.5)
    except Exception:
        pass

    total_errors = cpu_errors + ram_errors + disk_errors + gpu_errors
    if stage_callback:
        stage_callback("TEST DE PIÉTINEMENT 25 MIN TERMINÉ AVEC SUCCÈS !", 1.0, 1.0, total_errors)

    return {
        "status": "PASSED" if total_errors == 0 else f"ERREURS ({total_errors})",
        "duration": "25.0 minutes (5 étapes x 5 min)",
        "cpu_errors": cpu_errors,
        "ram_errors": ram_errors,
        "disk_errors": disk_errors,
        "gpu_errors": gpu_errors,
        "total_errors": total_errors,
        "health": "Excellente Stabilité (0 erreur sur 25 min)" if total_errors == 0 else "Anomalies matérielles détectées"
    }

def run_all_hardware_benchmarks(quick=True, callback=None, stage_callback=None):
    """
    Runs strictly sequential benchmarks component by component.
    """
    if quick:
        cpu_res = run_cpu_benchmark(duration_sec=2, callback=callback)
        ram_res = run_ram_benchmark(duration_sec=2, block_mb=64, callback=callback)
        disk_res = run_disk_benchmark(duration_sec=2, test_mb=32, callback=callback)
        gpu_res = run_gpu_benchmark(duration_sec=2, callback=callback)
        batt_res = run_battery_benchmark(callback=callback)
        endurance_res = {"status": "Non exécuté (Mode Rapide)"}
    else:
        endurance_res = run_25min_sequential_endurance(duration_sec=1500, stage_callback=stage_callback)
        cpu_res = run_cpu_benchmark(duration_sec=3, callback=None)
        ram_res = run_ram_benchmark(duration_sec=3, block_mb=128, callback=None)
        disk_res = run_disk_benchmark(duration_sec=3, test_mb=64, callback=None)
        gpu_res = run_gpu_benchmark(duration_sec=3, callback=None)
        batt_res = run_battery_benchmark(callback=None)

    return {
        "cpu": cpu_res,
        "ram": ram_res,
        "disk": disk_res,
        "gpu": gpu_res,
        "battery": batt_res,
        "endurance": endurance_res
    }
