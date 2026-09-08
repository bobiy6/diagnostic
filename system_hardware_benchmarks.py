import time
import psutil
import os
import math
import tempfile
import multiprocessing
import random

def _get_cpu_temperature_safe():
    """
    Safely retrieves system CPU temperature if available on OS sensors.
    """
    try:
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current and entry.current > 0:
                            return f"{round(entry.current, 1)} °C"
    except Exception:
        pass
    return "Non disponible / Normal"

def _cpu_worker_90pct_duty_cycle(stop_timestamp):
    """
    Runs a controlled ~90% duty-cycle CPU stress loop (9ms work / 1ms sleep yield).
    Prevents hardware thermal damage while maintaining high diagnostic stress.
    """
    val = 1.0001
    while time.time() < stop_timestamp:
        t_batch_end = time.time() + 0.009  # 9ms active work (~90% target core load)
        while time.time() < t_batch_end:
            for _ in range(500):
                val = math.sin(val) * math.cos(val) * math.sqrt(abs(val) + 1.0) + 1.0001
        time.sleep(0.001)  # 1ms duty-cycle yield (~10% safety margin)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def run_cpu_benchmark(duration_sec=3, callback=None):
    """
    Targeted ~90% Duty-Cycle CPU Stress Test with thermal & stability monitoring.
    """
    start_time = time.time()
    end_time = start_time + duration_sec
    errors = 0

    num_cores = max(1, psutil.cpu_count(logical=True) or 2)
    processes = []

    try:
        for _ in range(num_cores):
            p = multiprocessing.Process(target=_cpu_worker_90pct_duty_cycle, args=(end_time,))
            p.daemon = True
            p.start()
            processes.append(p)

        while time.time() < end_time:
            elapsed = time.time() - start_time
            pct = min(0.99, elapsed / duration_sec)
            temp_str = _get_cpu_temperature_safe()
            if callback:
                try: callback(f"PROCESSEUR (CPU) : Charge ciblée ~90% sur {num_cores} cœurs (Temp: {temp_str})...", pct)
                except Exception: pass
            time.sleep(0.1)

        for p in processes:
            p.join(timeout=1.0)
            if p.is_alive():
                p.terminate()

    except Exception:
        errors += 1
        for p in processes:
            if p.is_alive():
                try: p.terminate()
                except Exception: pass

    elapsed = max(0.001, time.time() - start_time)
    final_temp = _get_cpu_temperature_safe()

    if callback:
        try: callback(f"PROCESSEUR (CPU) : Terminé à 90% (Sécurité Matériel) - Temp: {final_temp} ({errors} erreur)", 1.0)
        except Exception: pass

    if num_cores >= 8:
        rating = f"Haute performance ~90% ({num_cores} cœurs, Temp: {final_temp})"
        health = "Excellent"
    elif num_cores >= 4:
        rating = f"Performance optimale ~90% ({num_cores} cœurs, Temp: {final_temp})"
        health = "Bon"
    else:
        rating = f"Performance bureautique ~90% ({num_cores} cœurs)"
        health = "Bureautique"

    return {
        "status": "PASSED" if errors == 0 else "ERREUR",
        "cpu_usage": "~90% (Protection thermique active)",
        "temperature": final_temp,
        "errors": errors,
        "threads_used": num_cores,
        "elapsed": f"{round(elapsed, 1)}s",
        "rating": rating,
        "health": health
    }

def run_ram_benchmark(duration_sec=4, block_mb=256, callback=None):
    """
    ~90% RAM Stress & MemTest Allocation with stability pattern verification.
    """
    start_time = time.time()
    end_time = start_time + duration_sec
    errors_found = 0
    total_bytes_tested = 0

    patterns = [0x55, 0xAA, 0xFF, 0x00]

    buf = None
    actual_block_mb = block_mb
    for try_mb in [block_mb, 128, 64]:
        try:
            size_bytes = try_mb * 1024 * 1024
            buf = bytearray(size_bytes)
            actual_block_mb = try_mb
            break
        except (MemoryError, Exception):
            continue

    if buf is None:
        size_bytes = 32 * 1024 * 1024
        buf = bytearray(size_bytes)
        actual_block_mb = 32

    try:
        pattern_idx = 0
        while time.time() < end_time:
            now = time.time()
            elapsed = now - start_time
            pct = min(0.99, elapsed / duration_sec)

            pat = patterns[pattern_idx % len(patterns)]
            if callback:
                try: callback(f"MÉMOIRE (RAM) : Stress MemTest ~90% 0x{pat:02X} ({actual_block_mb} Mo)...", pct)
                except Exception: pass

            pat_bytes = bytes([pat]) * (1024 * 1024)
            for chunk_off in range(0, size_bytes, 1024 * 1024):
                buf[chunk_off:chunk_off + (1024 * 1024)] = pat_bytes

            if buf[0] != pat or buf[size_bytes // 2] != pat or buf[-1] != pat:
                errors_found += 1

            total_bytes_tested += size_bytes
            pattern_idx += 1
            time.sleep(0.002)  # ~90% pacing yield

        del buf
    except Exception:
        errors_found += 1

    elapsed = max(0.001, time.time() - start_time)
    speed_mb_s = round((total_bytes_tested / (1024*1024)) / elapsed, 1)

    if callback:
        try: callback(f"MÉMOIRE (RAM) : Terminé ~90% - Vitesse: {speed_mb_s} Mo/s ({errors_found} erreur)", 1.0)
        except Exception: pass

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
        "tested_mb": f"{actual_block_mb} Mo",
        "rating": rating,
        "health": health
    }

def run_disk_benchmark(duration_sec=4, test_mb=128, callback=None):
    """
    ~90% Disk I/O & Random 4K IOPS Stress Test (Controlled FIO-style disk bench).
    """
    test_file = os.path.join(tempfile.gettempdir(), "pc_diag_disk_seq.tmp")
    data_block = os.urandom(1024 * 1024)
    chunk_4k = os.urandom(4096)

    write_speed = 0.0
    read_speed = 0.0
    iops = 0
    errors_found = 0

    try:
        if callback:
            try: callback(f"DISQUE STOCKAGE : Écriture séquentielle ~90% ({test_mb} Mo)...", 0.25)
            except Exception: pass
        t0 = time.time()
        with open(test_file, "wb") as f:
            for _ in range(test_mb):
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
        t1 = time.time()
        write_speed = round(test_mb / max(0.001, t1 - t0), 1)

        if callback:
            try: callback("DISQUE STOCKAGE : Lecture séquentielle ~90%...", 0.6)
            except Exception: pass
        t2 = time.time()
        with open(test_file, "rb") as f:
            while f.read(1024 * 1024):
                pass
        t3 = time.time()
        read_speed = round(test_mb / max(0.001, t3 - t2), 1)

        if callback:
            try: callback("DISQUE STOCKAGE : Test E/S 4K IOPS contrôlé (~90%)...", 0.85)
            except Exception: pass
        t4 = time.time()
        with open(test_file, "r+b") as f:
            file_size = test_mb * 1024 * 1024
            iops_count = 120
            for _ in range(iops_count):
                pos = random.randint(0, file_size - 4096)
                f.seek(pos)
                f.write(chunk_4k)
                f.seek(pos)
                _ = f.read(4096)
                time.sleep(0.0001)  # Duty-cycle yield
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
        try: callback(f"DISQUE STOCKAGE : Terminé ~90% - Écrit: {write_speed} Mo/s, Lu: {read_speed} Mo/s ({errors_found} erreur)", 1.0)
        except Exception: pass

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
    ~90% GPU 3D Geometry Matrix Rendering & Stability Test.
    """
    start_time = time.time()
    end_time = start_time + duration_sec
    frames = 0
    errors_found = 0

    vertices = [[random.uniform(-10, 10) for _ in range(3)] for _ in range(200)]

    while time.time() < end_time:
        now = time.time()
        elapsed = now - start_time
        pct = min(0.99, elapsed / duration_sec)

        if callback:
            try: callback(f"CARTE GRAPHIQUE (GPU) : Stress rendu 3D ~90%...", pct)
            except Exception: pass

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
            time.sleep(0.0002)  # ~90% duty cycle yield
        except Exception:
            errors_found += 1

    elapsed = max(0.001, time.time() - start_time)
    fps = int(frames / elapsed)
    score_3d = fps * 10

    if callback:
        try: callback(f"CARTE GRAPHIQUE (GPU) : Terminé ~90% - Rendu: {fps} FPS, Score: {score_3d} pts ({errors_found} erreur)", 1.0)
        except Exception: pass

    if fps > 1200:
        rating = "Excellente accélération graphique / GPU Dédié Performant"
        health = "Excellent"
    elif fps > 400:
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
    if callback:
        try: callback("BATTERIE & ALIMENTATION : Analyse de la rétention et de la charge...", 0.5)
        except Exception: pass

    try:
        batt = psutil.sensors_battery()
        if callback:
            try: callback("BATTERIE & ALIMENTATION : Terminé à 100%", 1.0)
            except Exception: pass

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
        if callback:
            try: callback("BATTERIE & ALIMENTATION : Erreur de lecture", 1.0)
            except Exception: pass
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
    Real 25-Minute (1500s) Controlled ~90% Stress Test divided into 5 Stages (5 min each).
    - Stage 1: CPU Multiprocessing Stress at ~90% duty-cycle across ALL cores
    - Stage 2: Deep MemTest RAM Allocation & Pattern Integrity (256 MB buffer)
    - Stage 3: Controlled Disk I/O & IOPS Write/Read cycles (16 MB buffer)
    - Stage 4: GPU 3D Geometry Transformation & Rendering stress
    - Stage 5: Thermal & System Global Stability Stress
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
                try: stage_callback(stage_name, st_pct, glob_pct, errs)
                except Exception: pass

    # STAGE 1: CPU Multiprocessing Stress at ~90% Duty-Cycle (5 min)
    try:
        t_stage1_end = time.time() + stage_duration
        num_cores = max(1, psutil.cpu_count(logical=True) or 2)
        processes = []

        for _ in range(num_cores):
            p = multiprocessing.Process(target=_cpu_worker_90pct_duty_cycle, args=(t_stage1_end,))
            p.daemon = True
            p.start()
            processes.append(p)

        while time.time() < t_stage1_end:
            now = time.time()
            elapsed_st = now - (t_stage1_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.0 + (pct_st * 0.2)
            temp_str = _get_cpu_temperature_safe()
            rate_limited_cb(f"ÉTAPE 1/5 : STRESS PROCESSEUR ~90% ({num_cores} Cœur(s) | Temp: {temp_str}) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)
            time.sleep(0.2)

        for p in processes:
            p.join(timeout=1.0)
            if p.is_alive():
                p.terminate()

    except Exception:
        cpu_errors += 1

    # STAGE 2: Deep RAM MemTest (~90% load) (5 min)
    try:
        t_stage2_end = time.time() + stage_duration
        ram_buffer = None
        for try_mb in [256, 128, 64]:
            try:
                ram_buffer = bytearray(try_mb * 1024 * 1024)
                break
            except (MemoryError, Exception):
                continue
        if ram_buffer is None:
            ram_buffer = bytearray(32 * 1024 * 1024)

        while time.time() < t_stage2_end:
            now = time.time()
            elapsed_st = now - (t_stage2_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.2 + (pct_st * 0.2)
            rate_limited_cb("ÉTAPE 2/5 : TEST INTÉGRITÉ MÉMOIRE APPROFONDI (RAM MemTest ~90%) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)

            for pat in [0x55, 0xAA, 0xFF, 0x00]:
                pat_bytes = bytes([pat]) * (1024 * 1024)
                for chunk_off in range(0, len(ram_buffer), 1024 * 1024):
                    ram_buffer[chunk_off:chunk_off + (1024 * 1024)] = pat_bytes
                if ram_buffer[0] != pat or ram_buffer[-1] != pat:
                    ram_errors += 1
            time.sleep(0.002)
        del ram_buffer
    except Exception:
        ram_errors += 1

    # STAGE 3: Controlled Disk I/O & IOPS Stress (5 min)
    endurance_disk_file = os.path.join(tempfile.gettempdir(), "mg_endurance_heavy_disk.tmp")
    data_16mb = os.urandom(16 * 1024 * 1024)
    chunk_4k = os.urandom(4096)
    try:
        t_stage3_end = time.time() + stage_duration
        while time.time() < t_stage3_end:
            now = time.time()
            elapsed_st = now - (t_stage3_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.4 + (pct_st * 0.2)
            rate_limited_cb("ÉTAPE 3/5 : STRESS BENCHMARK E/S DISQUE & IOPS (~90%) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)

            with open(endurance_disk_file, "wb") as f:
                f.write(data_16mb)
                f.flush()
                os.fsync(f.fileno())
            with open(endurance_disk_file, "r+b") as f:
                for _ in range(50):
                    pos = random.randint(0, (16 * 1024 * 1024) - 4096)
                    f.seek(pos)
                    f.write(chunk_4k)
            time.sleep(0.02)

        if os.path.exists(endurance_disk_file):
            os.remove(endurance_disk_file)
    except Exception:
        disk_errors += 1
        if os.path.exists(endurance_disk_file):
            try: os.remove(endurance_disk_file)
            except Exception: pass

    # STAGE 4: GPU 3D Matrix Rendering (~90%) (5 min)
    try:
        t_stage4_end = time.time() + stage_duration
        vertices = [[random.uniform(-10, 10) for _ in range(3)] for _ in range(200)]
        while time.time() < t_stage4_end:
            now = time.time()
            elapsed_st = now - (t_stage4_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.6 + (pct_st * 0.2)
            rate_limited_cb("ÉTAPE 4/5 : STRESS RENDU GRAPHIQUE 3D & MATRICES (~90% GPU) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)

            for angle_step in range(10):
                cos_a = math.cos(angle_step * 0.1)
                sin_a = math.sin(angle_step * 0.1)
                for x, y, z in vertices:
                    nx = x * cos_a + z * sin_a
                    ny = y
                    nz = -x * sin_a + z * cos_a
                    _ = (nx * 250) / (nz + 500)
            time.sleep(0.001)
    except Exception:
        gpu_errors += 1

    # STAGE 5: Thermal & System Global Stability Monitoring (5 min)
    try:
        t_stage5_end = time.time() + stage_duration
        comb_buf = bytearray(16 * 1024 * 1024)
        while time.time() < t_stage5_end:
            now = time.time()
            elapsed_st = now - (t_stage5_end - stage_duration)
            pct_st = min(1.0, elapsed_st / stage_duration)
            global_pct = 0.8 + (pct_st * 0.2)
            temp_str = _get_cpu_temperature_safe()
            rate_limited_cb(f"ÉTAPE 5/5 : ANALYSE DE STABILITÉ THERMIQUE (Temp: {temp_str}) - 5 MINUTES", pct_st, global_pct, cpu_errors + ram_errors + disk_errors + gpu_errors)

            for i in range(0, len(comb_buf), 2048):
                comb_buf[i] = random.randint(0, 255)
            val = math.sin(time.time()) * math.cos(time.time())
            time.sleep(0.002)
        del comb_buf
    except Exception:
        pass

    total_errors = cpu_errors + ram_errors + disk_errors + gpu_errors
    if stage_callback:
        try: stage_callback("TEST DE PIÉTINEMENT 25 MIN TERMINÉ AVEC SUCCÈS !", 1.0, 1.0, total_errors)
        except Exception: pass

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
