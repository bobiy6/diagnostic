import React from 'react';
import { User, Laptop, Calendar, Wrench, Shield, FileText } from 'lucide-react';

export default function ClientForm({ clientData, setClientData }) {
  const handleChange = (field, value) => {
    setClientData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-6">
      <div className="flex items-center space-x-3 border-b border-slate-100 pb-4">
        <div className="bg-indigo-100 p-2.5 rounded-lg text-indigo-600">
          <User className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-slate-800">Fiche Client & Machine</h2>
          <p className="text-sm text-slate-500">Informations générales sur l'intervention (sans coordonnées personnelles)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Client Name */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Nom du Client / Raison Sociale
          </label>
          <div className="relative">
            <User className="w-5 h-5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={clientData.clientName || ''}
              onChange={(e) => handleChange('clientName', e.target.value)}
              placeholder="ex. Dupont Jean / SARL Tech"
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
            />
          </div>
        </div>

        {/* Date */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Date d'Intervention
          </label>
          <div className="relative">
            <Calendar className="w-5 h-5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="date"
              value={clientData.date || ''}
              onChange={(e) => handleChange('date', e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
            />
          </div>
        </div>

        {/* Technician Name */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Nom du Technicien
          </label>
          <div className="relative">
            <Wrench className="w-5 h-5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={clientData.technician || ''}
              onChange={(e) => handleChange('technician', e.target.value)}
              placeholder="ex. Marc Martin"
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
            />
          </div>
        </div>

        {/* Client Type */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Type de Client
          </label>
          <div className="relative">
            <Shield className="w-5 h-5 absolute left-3 top-2.5 text-slate-400" />
            <select
              value={clientData.clientType || 'Particulier'}
              onChange={(e) => handleChange('clientType', e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
            >
              <option value="Particulier">Particulier (Maintenance annuelle recommandée)</option>
              <option value="Professionnel">Professionnel (Maintenance semi-annuelle recommandée)</option>
            </select>
          </div>
        </div>

        {/* Brand / Model / Serial */}
        <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
          <div>
            <label className="block text-xs font-semibold text-slate-600 mb-1">
              Marque de la Machine
            </label>
            <input
              type="text"
              value={clientData.pcBrand || ''}
              onChange={(e) => handleChange('pcBrand', e.target.value)}
              placeholder="ex. Asus, Lenovo, HP..."
              className="w-full px-3 py-1.5 bg-white border border-slate-300 rounded-md text-sm text-slate-800 focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-600 mb-1">
              Modèle du PC
            </label>
            <input
              type="text"
              value={clientData.pcModel || ''}
              onChange={(e) => handleChange('pcModel', e.target.value)}
              placeholder="ex. ThinkPad X1 / Pavilion 15"
              className="w-full px-3 py-1.5 bg-white border border-slate-300 rounded-md text-sm text-slate-800 focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-600 mb-1">
              N° de Série / Tag
            </label>
            <input
              type="text"
              value={clientData.serialNumber || ''}
              onChange={(e) => handleChange('serialNumber', e.target.value)}
              placeholder="ex. SN-98234-XYZ"
              className="w-full px-3 py-1.5 bg-white border border-slate-300 rounded-md text-sm text-slate-800 focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        {/* Reason for consultation */}
        <div className="md:col-span-2">
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Motif de la demande / Symptômes signalés
          </label>
          <div className="relative">
            <FileText className="w-5 h-5 absolute left-3 top-3 text-slate-400" />
            <textarea
              rows="3"
              value={clientData.reason || ''}
              onChange={(e) => handleChange('reason', e.target.value)}
              placeholder="ex. Lenteurs au démarrage, bruits suspects de ventilateur, écran bleu régulier..."
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800"
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  );
}
