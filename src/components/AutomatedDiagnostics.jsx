import React, { useState, useEffect } from 'react';
import { Cpu, HardDrive, Battery, Monitor, Wifi, ShieldAlert, RefreshCw, AlertTriangle, Layers, Server } from 'lucide-react';

export default function AutomatedDiagnostics({ autoData, fetchDiagnostics, loading }) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-md border border-slate-200 p-12 text-center space-y-4">
        <RefreshCw className="w-10 h-10 text-indigo-600 animate-spin mx-auto" />
        <h3 className="text-lg font-bold text-slate-800">Analyse du système en cours...</h3>
        <p className="text-sm text-slate-500">Collecte des informations matérielles et logicielles en temps réel.</p>
      </div>
    );
  }

  const renderFallback = (val) => val || 'Non disponible';

  return (
    <div className="space-y-6">
      {/* Header bar */}
      <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="bg-blue-100 p-2.5 rounded-lg text-blue-600">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">Diagnostic Automatique Machine</h2>
            <p className="text-sm text-slate-500">Données système détectées automatiquement</p>
          </div>
        </div>
        <button
          onClick={fetchDiagnostics}
          className="flex items-center space-x-2 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 px-4 py-2 rounded-lg font-semibold text-sm transition"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Actualiser les données</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* CPU */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <Cpu className="w-5 h-5" />
            <span>Processeur (CPU)</span>
          </div>
          <div className="space-y-1.5 text-sm text-slate-700">
            <div><span className="font-semibold text-slate-500">Modèle:</span> {renderFallback(autoData?.cpu?.brand)}</div>
            <div><span className="font-semibold text-slate-500">Fréquence:</span> {renderFallback(autoData?.cpu?.speed)}</div>
            <div><span className="font-semibold text-slate-500">Cœurs:</span> {renderFallback(autoData?.cpu?.cores)}</div>
            <div><span className="font-semibold text-slate-500">Fabricant:</span> {renderFallback(autoData?.cpu?.manufacturer)}</div>
          </div>
        </div>

        {/* RAM */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <Layers className="w-5 h-5" />
            <span>Mémoire (RAM)</span>
          </div>
          <div className="space-y-1.5 text-sm text-slate-700">
            <div><span className="font-semibold text-slate-500">Capacité Totale:</span> {renderFallback(autoData?.ram?.total)}</div>
            <div><span className="font-semibold text-slate-500">Utilisée:</span> {renderFallback(autoData?.ram?.used)}</div>
            <div><span className="font-semibold text-slate-500">Disponible:</span> {renderFallback(autoData?.ram?.free)}</div>
            <div><span className="font-semibold text-slate-500">Taux d'utilisation:</span> {renderFallback(autoData?.ram?.usedPercent)}</div>
          </div>
        </div>

        {/* Disks */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <HardDrive className="w-5 h-5" />
            <span>Disques Stockage</span>
          </div>
          {autoData?.disks?.map((disk, idx) => (
            <div key={idx} className="space-y-1 text-sm text-slate-700 bg-slate-50 p-2.5 rounded-lg border border-slate-200 mb-1">
              <div className="font-semibold text-indigo-600">{disk.fs} ({disk.type})</div>
              <div><span className="font-semibold text-slate-500">Taille:</span> {renderFallback(disk.total)}</div>
              <div><span className="font-semibold text-slate-500">Libre:</span> {renderFallback(disk.free)}</div>
              <div><span className="font-semibold text-slate-500">Occupé:</span> {renderFallback(disk.usedPercent)}</div>
            </div>
          ))}
        </div>

        {/* Battery */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <Battery className="w-5 h-5" />
            <span>Batterie</span>
          </div>
          <div className="space-y-1.5 text-sm text-slate-700">
            <div><span className="font-semibold text-slate-500">Statut:</span> {renderFallback(autoData?.battery?.isCharging)}</div>
            <div><span className="font-semibold text-slate-500">Niveau:</span> {renderFallback(autoData?.battery?.percent)}</div>
            <div><span className="font-semibold text-slate-500">Cycles:</span> {renderFallback(autoData?.battery?.cycleCount)}</div>
            <div><span className="font-semibold text-slate-500">Santé globale:</span> {renderFallback(autoData?.battery?.health)}</div>
          </div>
        </div>

        {/* GPU */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <Monitor className="w-5 h-5" />
            <span>Carte Graphique (GPU)</span>
          </div>
          {autoData?.gpus?.map((gpu, idx) => (
            <div key={idx} className="space-y-1 text-sm text-slate-700">
              <div><span className="font-semibold text-slate-500">Modèle:</span> {renderFallback(gpu.model)}</div>
              <div><span className="font-semibold text-slate-500">Fabricant:</span> {renderFallback(gpu.vendor)}</div>
              <div><span className="font-semibold text-slate-500">VRAM:</span> {renderFallback(gpu.vram)}</div>
            </div>
          ))}
        </div>

        {/* Network */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <Wifi className="w-5 h-5" />
            <span>Réseau</span>
          </div>
          {autoData?.network?.map((net, idx) => (
            <div key={idx} className="space-y-1 text-sm text-slate-700">
              <div><span className="font-semibold text-slate-500">Interface:</span> {renderFallback(net.iface)}</div>
              <div><span className="font-semibold text-slate-500">Adresse IP:</span> {renderFallback(net.ip4)}</div>
              <div><span className="font-semibold text-slate-500">Adresse MAC:</span> {renderFallback(net.mac)}</div>
              <div><span className="font-semibold text-slate-500">État:</span> {renderFallback(net.operstate)}</div>
            </div>
          ))}
        </div>

        {/* OS / Windows */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <Server className="w-5 h-5" />
            <span>Système d'exploitation (Windows)</span>
          </div>
          <div className="space-y-1.5 text-sm text-slate-700">
            <div><span className="font-semibold text-slate-500">OS / Distro:</span> {renderFallback(autoData?.os?.distro)}</div>
            <div><span className="font-semibold text-slate-500">Version / Release:</span> {renderFallback(autoData?.os?.release)}</div>
            <div><span className="font-semibold text-slate-500">Architecture:</span> {renderFallback(autoData?.os?.arch)}</div>
            <div><span className="font-semibold text-slate-500">Nom Hôte:</span> {renderFallback(autoData?.os?.hostname)}</div>
          </div>
        </div>

        {/* Antivirus & Services */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <ShieldAlert className="w-5 h-5" />
            <span>Sécurité & Services</span>
          </div>
          <div className="space-y-1.5 text-sm text-slate-700">
            <div><span className="font-semibold text-slate-500">Antivirus:</span> {renderFallback(autoData?.antivirus?.status)}</div>
            <div><span className="font-semibold text-slate-500">Services Total:</span> {renderFallback(autoData?.services?.totalServices)}</div>
            <div><span className="font-semibold text-slate-500">Services Actifs:</span> {renderFallback(autoData?.services?.runningServices)}</div>
          </div>
        </div>

        {/* Erreurs fréquentes / Journaux récents */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-3">
          <div className="flex items-center space-x-2 text-indigo-600 font-bold border-b border-slate-100 pb-2">
            <AlertTriangle className="w-5 h-5" />
            <span>Anomalies & Erreurs Récentes</span>
          </div>
          {autoData?.recentErrors?.length > 0 ? (
            <div className="space-y-2">
              {autoData.recentErrors.map(err => (
                <div key={err.id} className="text-xs bg-amber-50 text-amber-900 border border-amber-200 p-2 rounded">
                  <span className="font-bold">[{err.type}]</span> {err.message}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-sm text-slate-500 italic">Aucune erreur récente signalée</div>
          )}
        </div>
      </div>
    </div>
  );
}
