import React from 'react';
import { ClipboardCheck, Wrench, MessageSquare, Plus, Trash2, AlertTriangle } from 'lucide-react';

export default function TechnicianQuestionnaire({ questionnaire, setQuestionnaire }) {
  const handleToggleChange = (key, value) => {
    setQuestionnaire(prev => ({
      ...prev,
      checklist: {
        ...prev.checklist,
        [key]: value
      }
    }));
  };

  const handleFieldChange = (field, value) => {
    setQuestionnaire(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addComponentChanged = () => {
    setQuestionnaire(prev => ({
      ...prev,
      replacedComponents: [...prev.replacedComponents, { name: '', reason: '' }]
    }));
  };

  const updateComponentChanged = (index, field, value) => {
    setQuestionnaire(prev => {
      const list = [...prev.replacedComponents];
      list[index][field] = value;
      return { ...prev, replacedComponents: list };
    });
  };

  const removeComponentChanged = (index) => {
    setQuestionnaire(prev => ({
      ...prev,
      replacedComponents: prev.replacedComponents.filter((_, i) => i !== index)
    }));
  };

  const checklistItems = [
    { key: 'dustCleaned', label: 'Dépoussiérage physique effectué' },
    { key: 'thermalPasteReplaced', label: 'Remplacement pâte thermique' },
    { key: 'diskScanOk', label: 'Analyse intégrité disque SMART valide' },
    { key: 'malwareCheck', label: 'Scan Antivirus / Anti-Malware effectué' },
    { key: 'updatesDone', label: 'Mises à jour OS & Pilotes effectuées' },
    { key: 'backupVerified', label: 'Sauvegarde des données client vérifiée' },
    { key: 'chargerOk', label: 'Chargeur et câble en bon état' },
    { key: 'screenPortsOk', label: 'Connectique & écran fonctionnels' }
  ];

  return (
    <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-6">
      <div className="flex items-center space-x-3 border-b border-slate-100 pb-4">
        <div className="bg-emerald-100 p-2.5 rounded-lg text-emerald-600">
          <ClipboardCheck className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-slate-800">Questionnaire Technicien</h2>
          <p className="text-sm text-slate-500">Évaluation visuelle, actions de maintenance et composants</p>
        </div>
      </div>

      {/* Checklist (Oui / Non / Inconnu) */}
      <div>
        <h3 className="text-md font-semibold text-slate-700 mb-3 flex items-center gap-2">
          <ClipboardCheck className="w-4 h-4 text-emerald-600" />
          Contrôles de maintenance (Oui / Non / Inconnu)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {checklistItems.map(item => {
            const currentVal = questionnaire.checklist?.[item.key] || 'inconnu';
            return (
              <div key={item.key} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-sm font-medium text-slate-700">{item.label}</span>
                <div className="flex items-center space-x-1">
                  {[
                    { val: 'oui', label: 'Oui', bg: 'bg-emerald-600 text-white' },
                    { val: 'non', label: 'Non', bg: 'bg-rose-600 text-white' },
                    { val: 'inconnu', label: 'Inconnu', bg: 'bg-amber-500 text-white' }
                  ].map(opt => (
                    <button
                      key={opt.val}
                      type="button"
                      onClick={() => handleToggleChange(item.key, opt.val)}
                      className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-colors ${
                        currentVal === opt.val
                          ? opt.bg
                          : 'bg-white text-slate-600 border border-slate-300 hover:bg-slate-100'
                      }`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Nature of issues */}
      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-1 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-500" />
          Nature des Problèmes Identifiés
        </label>
        <textarea
          rows="3"
          value={questionnaire.issuesNature || ''}
          onChange={(e) => handleFieldChange('issuesNature', e.target.value)}
          placeholder="ex. Surchauffe processeur due à la poussière, secteur disque défectueux, infection malveillante..."
          className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
        />
      </div>

      {/* Replaced Components */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
            <Wrench className="w-4 h-4 text-indigo-600" />
            Composants / Pièces Changés
          </label>
          <button
            type="button"
            onClick={addComponentChanged}
            className="flex items-center space-x-1 text-xs bg-indigo-50 text-indigo-600 hover:bg-indigo-100 px-3 py-1.5 rounded-md font-semibold transition"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Ajouter une pièce</span>
          </button>
        </div>

        {questionnaire.replacedComponents?.length === 0 ? (
          <p className="text-xs text-slate-400 italic bg-slate-50 p-3 rounded-lg border border-slate-200">
            Aucun composant remplacé pour le moment.
          </p>
        ) : (
          <div className="space-y-2">
            {questionnaire.replacedComponents?.map((comp, idx) => (
              <div key={idx} className="flex items-center gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                <input
                  type="text"
                  placeholder="ex. SSD NVMe 500 Go"
                  value={comp.name}
                  onChange={(e) => updateComponentChanged(idx, 'name', e.target.value)}
                  className="flex-1 px-3 py-1 bg-white border border-slate-300 rounded text-sm text-slate-800 focus:ring-2 focus:ring-indigo-500"
                />
                <input
                  type="text"
                  placeholder="Raison / Remarque"
                  value={comp.reason}
                  onChange={(e) => updateComponentChanged(idx, 'reason', e.target.value)}
                  className="flex-1 px-3 py-1 bg-white border border-slate-300 rounded text-sm text-slate-800 focus:ring-2 focus:ring-indigo-500"
                />
                <button
                  type="button"
                  onClick={() => removeComponentChanged(idx)}
                  className="p-1.5 text-rose-600 hover:bg-rose-50 rounded"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* General Comments & Observations */}
      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-1 flex items-center gap-2">
          <MessageSquare className="w-4 h-4 text-slate-500" />
          Commentaires sur la maintenance & Observations
        </label>
        <textarea
          rows="3"
          value={questionnaire.observations || ''}
          onChange={(e) => handleFieldChange('observations', e.target.value)}
          placeholder="ex. Système stabilisé après remplacement SSD et nettoyage. Performances x3 constatées."
          className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
        />
      </div>
    </div>
  );
}
