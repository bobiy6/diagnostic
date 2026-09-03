import { describe, it, expect } from 'vitest';
import { calculateSynthesis } from '../utils/synthesisCalculator';

describe('Synthesis Calculator Unit Tests', () => {
  it('calculates full health score (100/100) when all checklist items pass', () => {
    const clientData = { clientType: 'Particulier', date: '2026-09-01' };
    const questionnaire = {
      checklist: {
        dustCleaned: 'oui',
        thermalPasteReplaced: 'oui',
        diskScanOk: 'oui',
        malwareCheck: 'oui',
        updatesDone: 'oui'
      },
      issuesNature: '',
      replacedComponents: []
    };
    const autoData = { battery: { hasBattery: true, percent: '95%' } };

    const result = calculateSynthesis({ clientData, questionnaire, autoData, testResults: {} });

    expect(result.score).toBe(100);
    expect(result.urgency).toBe('Faible');
    expect(result.nextMaintenanceDate).toBe('2027-09-01'); // +1 year for Particulier
  });

  it('calculates maintenance interval as 6 months for Professionnel clients', () => {
    const clientData = { clientType: 'Professionnel', date: '2026-09-01' };
    const questionnaire = { checklist: { dustCleaned: 'oui' } };

    const result = calculateSynthesis({ clientData, questionnaire, autoData: {}, testResults: {} });

    expect(result.maintenanceInterval).toContain('6 mois');
    expect(result.nextMaintenanceDate).toBe('2027-03-01'); // +6 months
  });

  it('deducts points and updates states when issues and unperformed checks are present', () => {
    const clientData = { clientType: 'Particulier', date: '2026-09-01' };
    const questionnaire = {
      checklist: {
        dustCleaned: 'non', // -10
        diskScanOk: 'non', // -20
        malwareCheck: 'non' // -15
      },
      issuesNature: 'Surchauffe importante' // -10
    };

    const result = calculateSynthesis({ clientData, questionnaire, autoData: {}, testResults: {} });

    expect(result.score).toBe(45); // 100 - 10 - 20 - 15 - 10 = 45
    expect(result.urgency).toBe('Critique');
    expect(result.hwState).toBe('Dégradé');
    expect(result.swState).toBe('Nécessite Attention');
    expect(result.problems.length).toBeGreaterThan(0);
  });
});
