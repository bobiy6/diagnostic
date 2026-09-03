export function calculateSynthesis({ clientData, questionnaire, autoData, testResults }) {
  let score = 100;
  const problems = [];
  const actions = [];
  const recommendations = [];

  // Hardware evaluation
  let hwState = 'Excellent';
  if (questionnaire?.checklist?.dustCleaned === 'non') {
    score -= 10;
    problems.push('Poussière accumulée dans le système de refroidissement');
    actions.push('Nettoyage et dépoussiérage physique conseillés');
  }

  if (questionnaire?.checklist?.thermalPasteReplaced === 'non') {
    score -= 5;
    recommendations.push('Remplacement préventif de la pâte thermique');
  }

  if (questionnaire?.checklist?.diskScanOk === 'non') {
    score -= 20;
    hwState = 'Dégradé';
    problems.push('Anomalies ou secteurs défectueux détectés sur le disque');
    actions.push('Remplacement du disque par un SSD recommandé');
  }

  // Battery status
  let batteryState = 'Inconnu / Non applicable';
  if (autoData?.battery?.hasBattery) {
    if (autoData.battery.percent) {
      batteryState = `Opérationnelle (${autoData.battery.percent})`;
    }
    if (testResults?.batteryHealthCheck?.status === 'Avertissement') {
      score -= 10;
      batteryState = 'Capacité dégradée';
      problems.push('Autonomie batterie en baisse');
      recommendations.push('Prévoir le remplacement de la batterie à moyen terme');
    }
  }

  // Software evaluation
  let swState = 'Optimal';
  if (questionnaire?.checklist?.malwareCheck === 'non') {
    score -= 15;
    swState = 'Nécessite Attention';
    problems.push('Pertes de sécurité potentielles (Analyse malware non exécutée)');
    actions.push('Exécuter une analyse antivirus approfondie');
  }

  if (questionnaire?.checklist?.updatesDone === 'non') {
    score -= 10;
    swState = 'Nécessite Attention';
    problems.push('Système d\'exploitation non à jour');
    actions.push('Installer les dernières mises à jour Windows/OS');
  }

  if (questionnaire?.issuesNature && questionnaire.issuesNature.trim() !== '') {
    score -= 10;
    problems.push(`Problème signalé : ${questionnaire.issuesNature}`);
  }

  if (questionnaire?.replacedComponents?.length > 0) {
    questionnaire.replacedComponents.forEach(c => {
      if (c.name) {
        actions.push(`Remplacement composant : ${c.name} (${c.reason || 'Symptôme résolu'})`);
      }
    });
  }

  // Clamp score
  score = Math.max(10, Math.min(100, score));

  // Determine Urgency
  let urgency = 'Faible';
  if (score < 50) {
    urgency = 'Critique';
  } else if (score < 70) {
    urgency = 'Moyen';
  } else if (score < 85) {
    urgency = 'Normal';
  }

  // Recommendation on next maintenance interval
  const isPro = clientData?.clientType === 'Professionnel';
  const maintenanceInterval = isPro ? '6 mois (Professionnel)' : '1 an (Particulier)';
  recommendations.push(
    isPro
      ? 'Planifier une maintenance préventive semi-annuelle (tous les 6 mois) pour environnement professionnel.'
      : 'Planifier une maintenance préventive annuelle (tous les 12 mois) pour particulier.'
  );

  // Compute recommended next date
  const baseDate = clientData?.date ? new Date(clientData.date) : new Date();
  const nextDate = new Date(baseDate);
  if (isPro) {
    nextDate.setMonth(nextDate.getMonth() + 6);
  } else {
    nextDate.setFullYear(nextDate.getFullYear() + 1);
  }

  return {
    score,
    hwState,
    swState,
    batteryState,
    urgency,
    problems,
    actions,
    recommendations,
    maintenanceInterval,
    nextMaintenanceDate: nextDate.toISOString().split('T')[0]
  };
}
