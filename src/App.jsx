import React, { useState, useEffect } from 'react';
import {
  PlusCircle,
  User,
  ClipboardCheck,
  Cpu,
  Activity,
  Award,
  FileDown,
  Laptop,
  Wrench,
  CheckCircle2
} from 'lucide-react';

import ClientForm from './components/ClientForm';
import TechnicianQuestionnaire from './components/TechnicianQuestionnaire';
import AutomatedDiagnostics from './components/AutomatedDiagnostics';
import MachineTests from './components/MachineTests';
import SynthesisView from './components/SynthesisView';
import { generatePDFReport } from './utils/pdfGenerator';

export default function App() {
  const [activeTab, setActiveTab] = useState('client');
  const [notification, setNotification] = useState(null);

  // Form State: Client & Machine
  const [clientData, setClientData] = useState({
    clientName: 'Dupont Informatique',
    date: new Date().toISOString().split('T')[0],
    technician: 'Alexandre Martin',
    clientType: 'Particulier',
    pcBrand: 'Asus',
    pcModel: 'ZenBook Pro 15',
    serialNumber: 'SN-883920-AS',
    reason: 'Surchauffe régulière, ralentissements au lancement des logiciels métiers'
  });

  // Form State: Questionnaire
  const [questionnaire, setQuestionnaire] = useState({
    checklist: {
      dustCleaned: 'oui',
      thermalPasteReplaced: 'oui',
      diskScanOk: 'oui',
      malwareCheck: 'oui',
      updatesDone: 'oui',
      backupVerified: 'oui',
      chargerOk: 'oui',
      screenPortsOk: 'oui'
    },
    issuesNature: 'Ventilateur encrassé et pilote de carte graphique obsolète.',
    replacedComponents: [
      { name: 'SSD NVMe 1 To', reason: 'Amélioration de la vitesse de démarrage' }
    ],
    observations: 'Nettoyage complet effectué, dépoussiérage des ouïes d\'aération. Remise à niveau des pilotes.'
  });

  // Automated Diagnostic State
  const [autoData, setAutoData] = useState(null);
  const [loadingDiagnostics, setLoadingDiagnostics] = useState(false);

  // Machine Test State
  const [testResults, setTestResults] = useState({});

  const showNotification = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 3500);
  };

  const fetchDiagnostics = async () => {
    setLoadingDiagnostics(true);
    try {
      const res = await fetch('/api/system-info');
      if (res.ok) {
        const data = await res.json();
        setAutoData(data);
      } else {
        showNotification('Impossible de charger les données matérielles.');
      }
    } catch (err) {
      console.error(err);
      showNotification('Erreur de connexion au serveur diagnostic.');
    } finally {
      setLoadingDiagnostics(false);
    }
  };

  useEffect(() => {
    fetchDiagnostics();
  }, []);

  const handleNewDiagnostic = () => {
    if (window.confirm('Voulez-vous réinitialiser le formulaire pour un nouveau diagnostic ?')) {
      setClientData({
        clientName: '',
        date: new Date().toISOString().split('T')[0],
        technician: '',
        clientType: 'Particulier',
        pcBrand: '',
        pcModel: '',
        serialNumber: '',
        reason: ''
      });
      setQuestionnaire({
        checklist: {
          dustCleaned: 'inconnu',
          thermalPasteReplaced: 'inconnu',
          diskScanOk: 'inconnu',
          malwareCheck: 'inconnu',
          updatesDone: 'inconnu',
          backupVerified: 'inconnu',
          chargerOk: 'inconnu',
          screenPortsOk: 'inconnu'
        },
        issuesNature: '',
        replacedComponents: [],
        observations: ''
      });
      setTestResults({});
      setActiveTab('client');
      showNotification('Nouveau diagnostic réinitialisé avec succès.');
    }
  };

  const handleExportPDF = () => {
    generatePDFReport({ clientData, questionnaire, autoData, testResults });
    showNotification('Rapport PDF généré avec succès !');
  };

  const tabs = [
    { id: 'client', label: 'Fiche Client', icon: User },
    { id: 'questionnaire', label: 'Questionnaire', icon: ClipboardCheck },
    { id: 'auto', label: 'Diagnostic Auto', icon: Cpu },
    { id: 'tests', label: 'Tests Machine', icon: Activity },
    { id: 'synthesis', label: 'Synthèse', icon: Award }
  ];

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 flex flex-col font-sans">
      {/* Top Application Header */}
      <header className="bg-slate-900 text-white shadow-lg border-b border-slate-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-600 rounded-xl text-white shadow-md">
              <Laptop className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-black tracking-wide text-white">PC Diagnostic & Rapport</h1>
              <p className="text-xs text-slate-400">Plateforme de diagnostic et génération de fiches techniques</p>
            </div>
          </div>

          {/* Top Quick Actions */}
          <div className="flex items-center space-x-3">
            <button
              onClick={handleNewDiagnostic}
              className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3.5 py-2 rounded-lg text-xs font-semibold border border-slate-700 transition"
            >
              <PlusCircle className="w-4 h-4 text-emerald-400" />
              <span>Nouveau diagnostic</span>
            </button>

            <button
              onClick={handleExportPDF}
              className="flex items-center space-x-1.5 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-md transition"
            >
              <FileDown className="w-4 h-4" />
              <span>Générer PDF</span>
            </button>
          </div>
        </div>

        {/* Navigation Tabs Bar */}
        <div className="max-w-7xl mx-auto px-4 mt-2 border-t border-slate-800/80">
          <nav className="flex space-x-1 overflow-x-auto py-2 scrollbar-none">
            {tabs.map((tab) => {
              const TabIcon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-xs font-bold transition whitespace-nowrap ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                  }`}
                >
                  <TabIcon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* Main Content View */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6">
        {notification && (
          <div className="mb-4 bg-emerald-500 text-white px-4 py-3 rounded-xl shadow-md flex items-center justify-between font-semibold text-sm animate-fade-in">
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-5 h-5" />
              <span>{notification}</span>
            </div>
          </div>
        )}

        {activeTab === 'client' && (
          <ClientForm clientData={clientData} setClientData={setClientData} />
        )}

        {activeTab === 'questionnaire' && (
          <TechnicianQuestionnaire questionnaire={questionnaire} setQuestionnaire={setQuestionnaire} />
        )}

        {activeTab === 'auto' && (
          <AutomatedDiagnostics
            autoData={autoData}
            fetchDiagnostics={fetchDiagnostics}
            loading={loadingDiagnostics}
          />
        )}

        {activeTab === 'tests' && (
          <MachineTests testResults={testResults} setTestResults={setTestResults} />
        )}

        {activeTab === 'synthesis' && (
          <SynthesisView
            clientData={clientData}
            questionnaire={questionnaire}
            autoData={autoData}
            testResults={testResults}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        <p>PC Diagnostic & Rapport • Conçu pour les techniciens de maintenance informatique</p>
      </footer>
    </div>
  );
}
