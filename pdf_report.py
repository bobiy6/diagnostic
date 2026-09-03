import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String

def calculate_synthesis(client_data, questionnaire, auto_data, test_results=None):
    score = 100
    problems = []
    actions = []
    recommendations = []

    # Benchmark results evaluation
    cpu_health = "Bon"
    ram_health = "Bon"
    disk_health = "Bon"
    gpu_health = "Bon"
    battery_health = auto_data.get("battery", {}).get("health", "Non disponible")

    if test_results:
        # CPU
        cpu_res = test_results.get("cpu", {})
        if cpu_res.get("health") == "Ralentissement / Lent":
            score -= 10
            cpu_health = "Ralentissement / Surcharge"
            problems.append(f"Processeur sous-performant ({cpu_res.get('ops_per_sec', 'N/A')})")

        # RAM
        ram_res = test_results.get("ram", {})
        if ram_res.get("errors_found", 0) > 0:
            score -= 30
            ram_health = "DÉFAILLANT (Erreurs MemTest)"
            problems.append(f"ANOMALIE MATÉRIELLE: {ram_res.get('errors_found')} erreur(s) mémoire RAM détectée(s)")
            actions.append("Remplacement de la barrette de RAM défectueuse")

        # Disk
        disk_res = test_results.get("disk", {})
        if disk_res.get("health") == "Dégradé / À remplacer":
            score -= 25
            disk_health = "Dégradé / À remplacer"
            problems.append(f"Vitesse de transfert disque anormalement lente ({disk_res.get('write_speed', 'N/A')})")
            actions.append("Remplacement recommandé par un SSD NVMe / SATA rapide")
        elif disk_res.get("health") == "Usure modérée / Lent":
            score -= 10
            disk_health = "Usure modérée (HDD Mécanique)"
            recommendations.append("Envisager le passage à un SSD pour multiplier par 5 la vitesse")

        # GPU
        gpu_res = test_results.get("gpu", {})
        if gpu_res.get("health") == "Excellent":
            gpu_health = f"Excellent ({gpu_res.get('fps', 'N/A')})"
        elif gpu_res.get("health") == "Bon":
            gpu_health = f"Bon ({gpu_res.get('fps', 'N/A')})"

        # Battery
        batt_res = test_results.get("battery", {})
        if batt_res.get("health") == "À remplacer":
            score -= 15
            battery_health = "Fortement dégradée (À remplacer)"
            problems.append(f"Batterie usée ({batt_res.get('estimated_wear', 'N/A')})")
            actions.append("Remplacement de la batterie recommandé")

    # Checklist evaluation
    checklist = questionnaire.get("checklist", {})
    if checklist.get("dustCleaned") == "non":
        score -= 10
        problems.append("Poussière accumulée dans les ventilateurs / dissipateurs")
        actions.append("Nettoyage et dépoussiérage physique conseillés")

    if checklist.get("thermalPasteReplaced") == "non":
        score -= 5
        recommendations.append("Remplacement préventif de la pâte thermique")

    if checklist.get("diskScanOk") == "non":
        score -= 20
        disk_health = "Anomalie / Secteurs défectueux"
        problems.append("Anomalies ou secteurs défectueux détectés sur le disque")
        actions.append("Remplacement impératif du disque")

    if checklist.get("malwareCheck") == "non":
        score -= 15
        problems.append("Contrôle Antivirus / Anti-Malware non réalisé")
        actions.append("Analyse complète de sécurité recommandée")

    if checklist.get("updatesDone") == "non":
        score -= 10
        problems.append("Système d'exploitation ou pilotes obsolètes")
        actions.append("Mise à jour de Windows et des pilotes matériels")

    issues_nature = questionnaire.get("issuesNature", "")
    if issues_nature and issues_nature.strip():
        score -= 10
        problems.append(f"Symptôme / Problème signalé : {issues_nature}")

    replaced_comps = questionnaire.get("replacedComponents", [])
    for comp in replaced_comps:
        if comp.get("name"):
            actions.append(f"Changement composant : {comp['name']} ({comp.get('reason', 'Remplacement effectué')})")

    score = max(10, min(100, score))

    if score < 50:
        urgency = "Critique"
    elif score < 70:
        urgency = "Moyen"
    elif score < 85:
        urgency = "Normal"
    else:
        urgency = "Faible"

    is_pro = client_data.get("clientType") == "Professionnel"
    maint_interval = "6 mois (Professionnel)" if is_pro else "1 an (Particulier)"
    recommendations.append(
        "Planifier une maintenance préventive semi-annuelle (tous les 6 mois) pour environnement professionnel."
        if is_pro else
        "Planifier une maintenance préventive annuelle (tous les 12 mois) pour particulier."
    )

    base_date_str = client_data.get("date")
    try:
        base_date = datetime.datetime.strptime(base_date_str, "%Y-%m-%d")
    except Exception:
        base_date = datetime.datetime.now()

    if is_pro:
        month = base_date.month + 6
        year = base_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        day = min(base_date.day, 28)
        next_maint_date = datetime.date(year, month, day).strftime("%Y-%m-%d")
    else:
        next_maint_date = datetime.date(base_date.year + 1, base_date.month, min(base_date.day, 28)).strftime("%Y-%m-%d")

    return {
        "score": score,
        "urgency": urgency,
        "cpu_health": cpu_health,
        "ram_health": ram_health,
        "disk_health": disk_health,
        "gpu_health": gpu_health,
        "battery_health": battery_health,
        "problems": problems,
        "actions": actions,
        "recommendations": recommendations,
        "maintenanceInterval": maint_interval,
        "nextMaintenanceDate": next_maint_date
    }

def create_logo_drawing():
    d = Drawing(36, 36)
    d.add(Rect(0, 0, 36, 36, rx=6, ry=6, fillColor=colors.HexColor('#2563EB'), strokeColor=None))
    d.add(Rect(6, 12, 24, 16, rx=2, ry=2, fillColor=colors.white, strokeColor=None))
    d.add(Rect(14, 6, 8, 4, fillColor=colors.HexColor('#CBD5E1'), strokeColor=None))
    d.add(Rect(10, 4, 16, 2, fillColor=colors.HexColor('#94A3B8'), strokeColor=None))
    d.add(String(13, 17, "PC", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#2563EB')))
    return d

def generate_pdf_report(filepath, client_data, questionnaire, auto_data, test_results=None):
    synthesis = calculate_synthesis(client_data, questionnaire, auto_data, test_results)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=10,
        spaceAfter=6
    )

    normal_text = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#334155'),
        leading=12
    )

    bold_text = ParagraphStyle(
        'BoldText',
        parent=normal_text,
        fontName='Helvetica-Bold'
    )

    elements = []

    # Title Banner with Logo
    header_table_data = [
        [
            create_logo_drawing(),
            [
                Paragraph("PC DIAGNOSTIC & RAPPORT", title_style),
                Paragraph("Rapport d'Expertise Technique & Bilan Matériel Approfondi", subtitle_style)
            ]
        ]
    ]

    t_header = Table(header_table_data, colWidths=[45, 495])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    elements.append(t_header)
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # 1. Client & PC Info
    elements.append(Paragraph("1. INFORMATIONS CLIENT & MACHINE", section_heading))
    client_table_data = [
        [
            Paragraph(f"<b>Client :</b> {client_data.get('clientName', 'Non spécifié')}", normal_text),
            Paragraph(f"<b>Date :</b> {client_data.get('date', 'N/A')}", normal_text),
            Paragraph(f"<b>Technicien :</b> {client_data.get('technician', 'N/A')}", normal_text)
        ],
        [
            Paragraph(f"<b>Type Client :</b> {client_data.get('clientType', 'Particulier')}", normal_text),
            Paragraph(f"<b>Machine :</b> {client_data.get('pcBrand', '')} {client_data.get('pcModel', '')}", normal_text),
            Paragraph(f"<b>N° Série :</b> {client_data.get('serialNumber', 'N/A')}", normal_text)
        ]
    ]

    t_client = Table(client_table_data, colWidths=[180, 180, 180])
    t_client.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_client)

    if client_data.get("reason"):
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"<b>Motif de consultation :</b> {client_data['reason']}", normal_text))

    elements.append(Spacer(1, 10))

    # 2. Synthesis Score Table
    elements.append(Paragraph("2. SYNTHÈSE DE SANTÉ & ÉTAT DE VIE", section_heading))

    score_color = colors.HexColor('#16A34A') if synthesis['score'] >= 80 else (colors.HexColor('#D97706') if synthesis['score'] >= 60 else colors.HexColor('#DC2626'))

    synth_table_data = [
        [
            Paragraph(f"<b>Note de Santé Global :</b> <font color='{score_color}'><b>{synthesis['score']} / 100</b></font>", normal_text),
            Paragraph(f"<b>Niveau d'Urgence :</b> {synthesis['urgency']}", normal_text),
            Paragraph(f"<b>Prochaine Maintenance :</b> {synthesis['nextMaintenanceDate']}", normal_text)
        ],
        [
            Paragraph(f"<b>Santé CPU :</b> {synthesis['cpu_health']}", normal_text),
            Paragraph(f"<b>Santé RAM :</b> {synthesis['ram_health']}", normal_text),
            Paragraph(f"<b>Santé Disque :</b> {synthesis['disk_health']}", normal_text)
        ]
    ]

    t_synth = Table(synth_table_data, colWidths=[180, 180, 180])
    t_synth.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_synth)

    elements.append(Spacer(1, 10))

    # 3. Real Benchmarks & Automatic Diagnostics
    elements.append(Paragraph("3. BENCHMARKS MATÉRIELS RÉELS & MESURES DE PERFORMANCE", section_heading))

    cpu = auto_data.get("cpu", {})
    ram = auto_data.get("ram", {})
    battery = auto_data.get("battery", {})
    os_info = auto_data.get("os", {})
    disks = auto_data.get("disks", [])
    disks_str = " | ".join([f"{d.get('mount')}: {d.get('total')} ({d.get('healthStatus')})" for d in disks]) if disks else "Non disponible"

    bench_cpu_str = "Non exécuté"
    if test_results and "cpu" in test_results:
        c_res = test_results["cpu"]
        bench_cpu_str = f"{c_res.get('ops_per_sec', 'N/A')} ({c_res.get('threads_used')} threads)"

    bench_ram_str = "Non exécuté"
    if test_results and "ram" in test_results:
        r_res = test_results["ram"]
        bench_ram_str = f"Débit: {r_res.get('write_read_speed', 'N/A')} | Erreurs MemTest: {r_res.get('errors_found', 0)}"

    bench_disk_str = "Non exécuté"
    if test_results and "disk" in test_results:
        d_res = test_results["disk"]
        bench_disk_str = f"Écrit: {d_res.get('write_speed', 'N/A')} | Lu: {d_res.get('read_speed', 'N/A')} | 4K: {d_res.get('iops_4k', 'N/A')}"

    bench_gpu_str = "Non exécuté"
    if test_results and "gpu" in test_results:
        g_res = test_results["gpu"]
        bench_gpu_str = f"FPS: {g_res.get('fps', 'N/A')} | Score 3D: {g_res.get('score_3d', 'N/A')}"

    diag_rows = [
        [Paragraph("<b>Composant / Système</b>", bold_text), Paragraph("<b>Caractéristiques & Benchmark Réel Mesuré</b>", bold_text), Paragraph("<b>État de Vie</b>", bold_text)],
        [Paragraph("Processeur (CPU)", normal_text), Paragraph(f"{cpu.get('model', 'N/A')} | Benchmark: {bench_cpu_str}", normal_text), Paragraph(synthesis['cpu_health'], normal_text)],
        [Paragraph("Mémoire (RAM)", normal_text), Paragraph(f"{ram.get('total', 'N/A')} Total | MemTest: {bench_ram_str}", normal_text), Paragraph(synthesis['ram_health'], normal_text)],
        [Paragraph("Disques Stockage", normal_text), Paragraph(f"{disks_str} | Benchmark IOPS: {bench_disk_str}", normal_text), Paragraph(synthesis['disk_health'], normal_text)],
        [Paragraph("Carte Graphique (GPU)", normal_text), Paragraph(f"GPU Rendu | Benchmark 3D: {bench_gpu_str}", normal_text), Paragraph(synthesis['gpu_health'], normal_text)],
        [Paragraph("Batterie", normal_text), Paragraph(f"{battery.get('percent', 'N/A')} - {battery.get('isCharging', 'N/A')} (Autonomie: {battery.get('lifetime', 'N/A')})", normal_text), Paragraph(synthesis['battery_health'], normal_text)],
        [Paragraph("Système d'exploitation", normal_text), Paragraph(f"{os_info.get('distro', 'N/A')} (Uptime: {os_info.get('uptime', 'N/A')})", normal_text), Paragraph("Actif", normal_text)],
        [Paragraph("Antivirus / Sécurité", normal_text), Paragraph(auto_data.get("antivirus", {}).get("status", "Non disponible"), normal_text), Paragraph("Protégé", normal_text)]
    ]

    t_diag = Table(diag_rows, colWidths=[140, 300, 100])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_diag)

    elements.append(Spacer(1, 10))

    # 4. Questionnaire & Maintenance Actions
    elements.append(Paragraph("4. RELEVÉ DE MAINTENANCE & CONTRÔLES TECHNICIEN", section_heading))

    chk = questionnaire.get("checklist", {})
    chk_rows = [
        [Paragraph("<b>Contrôle Technicien</b>", bold_text), Paragraph("<b>Résultat</b>", bold_text)],
        [Paragraph("Dépoussiérage physique effectué", normal_text), Paragraph(chk.get("dustCleaned", "inconnu").upper(), normal_text)],
        [Paragraph("Remplacement pâte thermique", normal_text), Paragraph(chk.get("thermalPasteReplaced", "inconnu").upper(), normal_text)],
        [Paragraph("Analyse intégrité disque SMART", normal_text), Paragraph(chk.get("diskScanOk", "inconnu").upper(), normal_text)],
        [Paragraph("Scan Antivirus / Anti-Malware effectué", normal_text), Paragraph(chk.get("malwareCheck", "inconnu").upper(), normal_text)],
        [Paragraph("Mises à jour OS & Pilotes effectuées", normal_text), Paragraph(chk.get("updatesDone", "inconnu").upper(), normal_text)]
    ]

    t_chk = Table(chk_rows, colWidths=[380, 160])
    t_chk.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_chk)

    # Replaced Components
    replaced = questionnaire.get("replacedComponents", [])
    if replaced:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("<b>Composants remplacés :</b>", bold_text))
        for comp in replaced:
            if comp.get("name"):
                elements.append(Paragraph(f"• {comp['name']} ({comp.get('reason', 'N/A')})", normal_text))

    if questionnaire.get("observations"):
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"<b>Observations du technicien :</b> {questionnaire['observations']}", normal_text))

    elements.append(Spacer(1, 14))

    # 5. Signatures Block
    sig_data = [
        [Paragraph("<b>Signature Technicien</b>", bold_text), Paragraph("<b>Bon pour accord Client / Signature</b>", bold_text)],
        ["\n\n\n", "\n\n\n"]
    ]
    t_sig = Table(sig_data, colWidths=[260, 260])
    t_sig.setStyle(TableStyle([
        ('BOX', (0, 0), (0, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('BOX', (1, 0), (1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(KeepTogether([t_sig]))

    doc.build(elements)
    return filepath
