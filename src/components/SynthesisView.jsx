import React from 'react';
import { Award, AlertTriangle, CheckCircle, ShieldCheck, Calendar, Wrench, FileText } from 'lucide-react';
import { calculateSynthesis } from '../utils/synthesisCalculator';

export default function SynthesisView({ clientData, questionnaire, autoData, testResults }) {
  const synthesis = calculateSynthesis({ clientData, questionnaire, autoData, testResults });

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-emerald-600 bg-emerald-50 border-emerald-200';
    if (score >= 60) return 'text-amber-600 bg-amber-50 border-amber-200';
    return 'text-rose-600 bg-rose-50 border-rose-200';
  };

  const getUrgencyBadge = (urgency) => {
    switch (urgency) {
      case 'Critique':
        return <span className="px-3 py-1 bg-rose-100 text-rose-800 rounded-full text-xs font-bold border border-rose-300">Urgence Critique</span>;
      case 'Moyen':
        return <span className="px-3 py-1 bg-amber-100 text-amber-800 rounded-full text-xs font-bold border border-amber-300">Urgence Moyenne</span>;
      case 'Normal':
        return <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-bold border border-blue-300">Urgence Normale</span>;
      default:
        return <span className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold border border-emerald-300">Urgence Faible</span>;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-6">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div className="flex items-center space-x-3">
          <div className="bg-indigo-100 p-2.5 rounded-lg text-indigo-600">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">Synthèse Générale du Diagnostic</h2>
            <p className="text-sm text-slate-500">Bilan de santé, état général et préconisations</p>
          </div>
        </div>
        <div>
          {getUrgencyBadge(synthesis.urgency)}
        </div>
      </div>

      {/* Global Score and Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Score Card */}
        <div className={`p-4 rounded-xl border flex flex-col items-center justify-center text-center space-y-1 ${getScoreColor(synthesis.score)}`}>
          <span className="text-xs font-bold uppercase tracking-wider">Note de Santé</span>
          <span className="text-4xl font-extrabold">{synthesis.score}<span className="text-xl font-medium text-slate-500">/100</span></span>
        </div>

        {/* Hardware Status */}
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col justify-between">
          <span className="text-xs font-semibold text-slate-500">État Matériel</span>
          <span className="text-lg font-bold text-slate-800">{synthesis.hwState}</span>
        </div>

        {/* Software Status */}
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col justify-between">
          <span className="text-xs font-semibold text-slate-500">État Logiciel</span>
          <span className="text-lg font-bold text-slate-800">{synthesis.swState}</span>
        </div>

        {/* Battery Status */}
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col justify-between">
          <span className="text-xs font-semibold text-slate-500">État Batterie</span>
          <span className="text-lg font-bold text-slate-800">{synthesis.batteryState}</span>
        </div>
      </div>

      {/* Problems, Actions & Recommendations Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Identified Problems */}
        <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-3">
          <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            Problèmes Identifiés ({synthesis.problems.length})
          </h3>
          {synthesis.problems.length === 0 ? (
            <p className="text-xs text-slate-500 italic">Aucun dysfonctionnement majeur à signaler.</p>
          ) : (
            <ul className="space-y-2 text-xs text-slate-700">
              {synthesis.problems.map((prob, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-rose-500 font-bold">•</span>
                  <span>{prob}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Interventions & Actions */}
        <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-3">
          <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <Wrench className="w-4 h-4 text-indigo-600" />
            Actions Réalisées / Préconisées
          </h3>
          {synthesis.actions.length === 0 ? (
            <p className="text-xs text-slate-500 italic">Aucune action corrective requise.</p>
          ) : (
            <ul className="space-y-2 text-xs text-slate-700">
              {synthesis.actions.map((act, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-indigo-500 font-bold">•</span>
                  <span>{act}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Recommendations & Next Maintenance */}
        <div className="bg-indigo-50/50 rounded-xl p-4 border border-indigo-100 space-y-3">
          <h3 className="text-sm font-bold text-indigo-900 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-indigo-600" />
            Recommandations Technicien
          </h3>
          <ul className="space-y-2 text-xs text-indigo-900">
            {synthesis.recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-indigo-600 font-bold">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>

          <div className="pt-2 border-t border-indigo-100 mt-2 flex items-center space-x-2 text-xs font-semibold text-indigo-800">
            <Calendar className="w-4 h-4 text-indigo-600" />
            <span>Prochaine Maintenance : {synthesis.nextMaintenanceDate}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
