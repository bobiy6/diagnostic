import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { calculateSynthesis } from './synthesisCalculator';

export function generatePDFReport({ clientData, questionnaire, autoData, testResults }) {
  const doc = new jsPDF();
  const synthesis = calculateSynthesis({ clientData, questionnaire, autoData, testResults });

  // Header Colors & Styling
  const primaryColor = [37, 99, 235]; // Blue 600
  const secondaryColor = [30, 41, 59]; // Slate 800

  // Header Banner
  doc.setFillColor(...primaryColor);
  doc.rect(0, 0, 210, 25, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(18);
  doc.setFont('helvetica', 'bold');
  doc.text('PC DIAGNOSTIC & RAPPORT', 14, 16);

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text('Rapport d\'Intervention & Bilan Technique', 130, 16);

  let yPos = 35;

  // 1. Client & PC Info Block
  doc.setTextColor(...secondaryColor);
  doc.setFontSize(12);
  doc.setFont('helvetica', 'bold');
  doc.text('1. INFORMATIONS CLIENT & MACHINE', 14, yPos);
  yPos += 4;

  const clientInfoData = [
    [
      `Client: ${clientData.clientName || 'Non spécifié'}`,
      `Date: ${clientData.date || new Date().toLocaleDateString()}`,
      `Technicien: ${clientData.technician || 'Non spécifié'}`
    ],
    [
      `Type Client: ${clientData.clientType || 'Particulier'}`,
      `Marque / Modèle: ${clientData.pcBrand || ''} ${clientData.pcModel || ''}`,
      `N° Série: ${clientData.serialNumber || 'Non spécifié'}`
    ]
  ];

  autoTable(doc, {
    startY: yPos,
    body: clientInfoData,
    theme: 'plain',
    styles: { fontSize: 9, cellPadding: 2, textColor: [51, 65, 85] },
    columnStyles: {
      0: { cellWidth: 70 },
      1: { cellWidth: 65 },
      2: { cellWidth: 55 }
    }
  });

  yPos = doc.lastAutoTable.finalY + 6;

  if (clientData.reason) {
    doc.setFontSize(9);
    doc.setFont('helvetica', 'italic');
    doc.text(`Motif de consultation : ${clientData.reason}`, 14, yPos);
    yPos += 8;
  }

  // 2. Synthesis & Health Score
  doc.setFontSize(12);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(...secondaryColor);
  doc.text('2. SYNTHÈSE DU DIAGNOSTIC', 14, yPos);
  yPos += 6;

  const synthesisTable = [
    [
      `Note de Santé Global : ${synthesis.score} / 100`,
      `Niveau d'Urgence : ${synthesis.urgency}`,
      `Prochaine Maintenance : ${synthesis.nextMaintenanceDate}`
    ],
    [
      `État Matériel : ${synthesis.hwState}`,
      `État Logiciel : ${synthesis.swState}`,
      `Batterie : ${synthesis.batteryState}`
    ]
  ];

  autoTable(doc, {
    startY: yPos,
    body: synthesisTable,
    theme: 'grid',
    headStyles: { fillColor: primaryColor },
    styles: { fontSize: 9, cellPadding: 3, fontStyle: 'bold' }
  });

  yPos = doc.lastAutoTable.finalY + 8;

  // 3. Automated Diagnostics (System Details)
  doc.setFontSize(12);
  doc.setFont('helvetica', 'bold');
  doc.text('3. DIAGNOSTICS AUTOMATIQUES DU SYSTÈME', 14, yPos);
  yPos += 6;

  const diagRows = [
    ['Processeur (CPU)', autoData?.cpu?.brand || 'Non disponible', autoData?.cpu?.speed || 'Non disponible'],
    ['Mémoire (RAM)', `${autoData?.ram?.total || 'Non disponible'} (Utilisé: ${autoData?.ram?.usedPercent || 'N/A'})`, 'Normal'],
    ['Stockage (Disques)', autoData?.disks?.map(d => `${d.fs}: ${d.total} (${d.usedPercent} occupé)`).join(' | ') || 'Non disponible', 'Normal'],
    ['Batterie', autoData?.battery?.hasBattery ? `${autoData.battery.percent} - ${autoData.battery.isCharging}` : 'Non disponible (PC Fixe)', autoData?.battery?.health || 'N/A'],
    ['Carte Graphique (GPU)', autoData?.gpus?.map(g => g.model).join(', ') || 'Non disponible', 'Normal'],
    ['Système d\'exploitation', `${autoData?.os?.distro || 'Non disponible'} ${autoData?.os?.release || ''}`, 'Actif'],
    ['Sécurité / Antivirus', autoData?.antivirus?.status || 'Non disponible', 'Protégé']
  ];

  autoTable(doc, {
    startY: yPos,
    head: [['Composant / Système', 'Caractéristiques / Mesure', 'État']],
    body: diagRows,
    theme: 'striped',
    headStyles: { fillColor: [51, 65, 85], textColor: [255, 255, 255] },
    styles: { fontSize: 8.5, cellPadding: 2.5 }
  });

  yPos = doc.lastAutoTable.finalY + 8;

  // Check if page break needed
  if (yPos > 230) {
    doc.addPage();
    yPos = 20;
  }

  // 4. Questionnaire & Maintenance Checklist
  doc.setFontSize(12);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(...secondaryColor);
  doc.text('4. RELEVÉ DE MAINTENANCE & INTERVENTIONS', 14, yPos);
  yPos += 6;

  const checklistRows = [
    ['Dépoussiérage physique', questionnaire?.checklist?.dustCleaned?.toUpperCase() || 'INCONNU'],
    ['Remplacement pâte thermique', questionnaire?.checklist?.thermalPasteReplaced?.toUpperCase() || 'INCONNU'],
    ['Analyse intégrité disque SMART', questionnaire?.checklist?.diskScanOk?.toUpperCase() || 'INCONNU'],
    ['Scan Antivirus / Anti-Malware', questionnaire?.checklist?.malwareCheck?.toUpperCase() || 'INCONNU'],
    ['Mises à jour OS & Pilotes', questionnaire?.checklist?.updatesDone?.toUpperCase() || 'INCONNU'],
    ['Sauvegarde des données', questionnaire?.checklist?.backupVerified?.toUpperCase() || 'INCONNU']
  ];

  autoTable(doc, {
    startY: yPos,
    head: [['Contrôle Technicien', 'Résultat']],
    body: checklistRows,
    theme: 'grid',
    headStyles: { fillColor: [71, 85, 105], textColor: [255, 255, 255] },
    styles: { fontSize: 8.5, cellPadding: 2 }
  });

  yPos = doc.lastAutoTable.finalY + 8;

  // 5. Replaced Components & Observations
  if (questionnaire?.replacedComponents?.length > 0) {
    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    doc.text('Composants / Pièces Remplacées :', 14, yPos);
    yPos += 5;

    questionnaire.replacedComponents.forEach(comp => {
      if (comp.name) {
        doc.setFontSize(8.5);
        doc.setFont('helvetica', 'normal');
        doc.text(`• ${comp.name} (${comp.reason || 'Symptôme corrigé'})`, 18, yPos);
        yPos += 4.5;
      }
    });
    yPos += 4;
  }

  if (questionnaire?.observations) {
    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    doc.text('Observations du Technicien :', 14, yPos);
    yPos += 5;
    doc.setFontSize(8.5);
    doc.setFont('helvetica', 'normal');
    doc.text(questionnaire.observations, 18, yPos, { maxWidth: 175 });
    yPos += 10;
  }

  // 6. Signatures Section
  if (yPos > 240) {
    doc.addPage();
    yPos = 30;
  }

  yPos += 5;
  doc.setDrawColor(203, 213, 225);
  doc.line(14, yPos, 196, yPos);
  yPos += 8;

  doc.setFontSize(9);
  doc.setFont('helvetica', 'bold');
  doc.text('Signature du Technicien', 25, yPos);
  doc.text('Signature / Bon pour Accord Client', 125, yPos);

  yPos += 6;
  doc.rect(25, yPos, 60, 20);
  doc.rect(125, yPos, 60, 20);

  // Download PDF
  const filename = `Rapport_Diagnostic_${clientData.clientName || 'PC'}_${new Date().toISOString().slice(0,10)}.pdf`;
  doc.save(filename);
}
