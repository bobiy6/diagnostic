import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def calculate_synthesis(client_data, questionnaire, auto_data, test_results=None):
    score = 100
    problems = []
    actions = []
    recommendations = []

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
        problems.append("Anomalies ou secteurs défectueux détectés sur le disque")
        actions.append("Remplacement du disque par un SSD recommandé")

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
        problems.append(f"Problème identifié : {issues_nature}")

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
        # +6 months
        month = base_date.month + 6
        year = base_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        day = min(base_date.day, 28)
        next_maint_date = datetime.date(year, month, day).strftime("%Y-%m-%d")
    else:
        # +1 year
        next_maint_date = datetime.date(base_date.year + 1, base_date.month, min(base_date.day, 28)).strftime("%Y-%m-%d")

    return {
        "score": score,
        "urgency": urgency,
        "problems": problems,
        "actions": actions,
        "recommendations": recommendations,
        "maintenanceInterval": maint_interval,
        "nextMaintenanceDate": next_maint_date
    }

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

    # Custom styles
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

    # Title & Header Banner
    elements.append(Paragraph("PC DIAGNOSTIC & RAPPORT", title_style))
    elements.append(Paragraph("Fiche Technique d'Intervention & Bilan de Diagnostic", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # 1. Client & PC Info Table
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

    # 2. Diagnostic Synthesis Table
    elements.append(Paragraph("2. SYNTHÈSE DU DIAGNOSTIC", section_heading))

    score_color = colors.HexColor('#16A34A') if synthesis['score'] >= 80 else (colors.HexColor('#D97706') if synthesis['score'] >= 60 else colors.HexColor('#DC2626'))

    synth_table_data = [
        [
            Paragraph(f"<b>Note de Santé Global :</b> <font color='{score_color}'><b>{synthesis['score']} / 100</b></font>", normal_text),
            Paragraph(f"<b>Niveau d'Urgence :</b> {synthesis['urgency']}", normal_text),
            Paragraph(f"<b>Prochaine Maintenance :</b> {synthesis['nextMaintenanceDate']}", normal_text)
        ]
    ]

    t_synth = Table(synth_table_data, colWidths=[180, 180, 180])
    t_synth.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_synth)

    elements.append(Spacer(1, 10))

    # 3. Automatic Diagnostics
    elements.append(Paragraph("3. DIAGNOSTICS AUTOMATIQUES DU SYSTÈME", section_heading))

    cpu = auto_data.get("cpu", {})
    ram = auto_data.get("ram", {})
    battery = auto_data.get("battery", {})
    os_info = auto_data.get("os", {})
    disks = auto_data.get("disks", [])
    disks_str = " | ".join([f"{d.get('mount')}: {d.get('total')} (Libre: {d.get('free')})" for d in disks]) if disks else "Non disponible"

    diag_rows = [
        [Paragraph("<b>Composant / Système</b>", bold_text), Paragraph("<b>Caractéristiques Mesurées</b>", bold_text), Paragraph("<b>État</b>", bold_text)],
        [Paragraph("Processeur (CPU)", normal_text), Paragraph(f"{cpu.get('model', 'N/A')} ({cpu.get('speed', 'N/A')}, {cpu.get('cores', 'N/A')})", normal_text), Paragraph("Normal", normal_text)],
        [Paragraph("Mémoire (RAM)", normal_text), Paragraph(f"{ram.get('total', 'N/A')} Total (Occupé: {ram.get('usedPercent', 'N/A')})", normal_text), Paragraph("Normal", normal_text)],
        [Paragraph("Disques Stockage", normal_text), Paragraph(disks_str, normal_text), Paragraph("Normal", normal_text)],
        [Paragraph("Batterie", normal_text), Paragraph(f"{battery.get('percent', 'N/A')} - {battery.get('isCharging', 'N/A')}", normal_text), Paragraph(battery.get("health", "N/A"), normal_text)],
        [Paragraph("Système d'exploitation", normal_text), Paragraph(f"{os_info.get('distro', 'N/A')} ({os_info.get('arch', 'N/A')})", normal_text), Paragraph("Actif", normal_text)],
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
    elements.append(Paragraph("4. RELEVÉ DE MAINTENANCE & CONTRÔLES", section_heading))

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

    # Observations
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
