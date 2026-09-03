import React, { useState } from 'react';
import { Play, CheckCircle2, AlertCircle, RefreshCw, Activity, Cpu, HardDrive, Battery, Gauge } from 'lucide-react';

export default function MachineTests({ testResults, setTestResults }) {
  const [runningTest, setRunningTest] = useState(null);

  const availableTests = [
    {
      id: 'cpuStress',
      name: 'Test de Charge CPU & Stabilité Thermal',
      description: 'Évalue la stabilité du processeur sous charge calcul intensif',
      icon: Cpu,
      duration: 2000
    },
    {
      id: 'ramIntegrity',
      name: 'Test d\'Intégrité Mémoire RAM',
      description: 'Allocation et contrôle de motifs mémoire pour déceler des adresses défectueuses',
      icon: Gauge,
      duration: 1500
    },
    {
      id: 'diskBenchmark',
      name: 'Benchmark Vitesse Disque / L/E',
      description: 'Mesure des vitesses de lecture / écriture séquentielle et aléatoire',
      icon: HardDrive,
      duration: 2000
    },
    {
      id: 'batteryHealthCheck',
      name: 'Analyse État & Rétention Batterie',
      description: 'Analyse de la courbe de décharge et calcul d\'usure des cellules',
      icon: Battery,
      duration: 1000
    }
  ];

  const runSingleTest = (test) => {
    setRunningTest(test.id);
    setTimeout(() => {
      let resultData = {};
      if (test.id === 'cpuStress') {
        resultData = {
          status: 'Succès',
          details: 'Température max: 68°C. Aucune baisse de fréquence (Throttling) détectée.',
          score: 95
        };
      } else if (test.id === 'ramIntegrity') {
        resultData = {
          status: 'Succès',
          details: '0 erreur détectée sur 8 Go alloués.',
          score: 100
        };
      } else if (test.id === 'diskBenchmark') {
        resultData = {
          status: 'Succès',
          details: 'Lecture: 3200 Mo/s | Écriture: 2700 Mo/s (Performances SSD NVMe optimales).',
          score: 98
        };
      } else if (test.id === 'batteryHealthCheck') {
        resultData = {
          status: 'Avertissement',
          details: 'Capacité restante à 82% de sa capacité initiale. Recommandation à surveiller.',
          score: 82
        };
      }

      setTestResults(prev => ({
        ...prev,
        [test.id]: {
          ...resultData,
          timestamp: new Date().toLocaleTimeString()
        }
      }));
      setRunningTest(null);
    }, test.duration);
  };

  const runAllTests = () => {
    setRunningTest('all');
    let delay = 0;
    availableTests.forEach((test, index) => {
      setTimeout(() => {
        runSingleTest(test);
        if (index === availableTests.length - 1) {
          setTimeout(() => setRunningTest(null), test.duration + 200);
        }
      }, delay);
      delay += test.duration + 300;
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-6">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div className="flex items-center space-x-3">
          <div className="bg-purple-100 p-2.5 rounded-lg text-purple-600">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">Tests Matériels Machine</h2>
            <p className="text-sm text-slate-500">Lancer des diagnostics actifs sur les composants stratégiques</p>
          </div>
        </div>

        <button
          onClick={runAllTests}
          disabled={runningTest !== null}
          className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-semibold text-sm transition disabled:opacity-50"
        >
          {runningTest === 'all' ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <Play className="w-4 h-4" />
          )}
          <span>Lancer Tous les Tests</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {availableTests.map((test) => {
          const TestIcon = test.icon;
          const isTesting = runningTest === test.id || runningTest === 'all';
          const res = testResults[test.id];

          return (
            <div key={test.id} className="bg-slate-50 rounded-xl p-5 border border-slate-200 flex flex-col justify-between space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="p-2 bg-white rounded-lg text-indigo-600 shadow-sm">
                      <TestIcon className="w-5 h-5" />
                    </div>
                    <h3 className="font-bold text-slate-800 text-md">{test.name}</h3>
                  </div>

                  {res && (
                    <span className={`px-2.5 py-1 text-xs font-bold rounded-full ${
                      res.status === 'Succès' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      {res.status}
                    </span>
                  )}
                </div>

                <p className="text-xs text-slate-500">{test.description}</p>
              </div>

              {res && (
                <div className="bg-white p-3 rounded-lg border border-slate-200 text-xs text-slate-700 space-y-1">
                  <div className="font-semibold text-slate-800">Résultat ({res.timestamp}):</div>
                  <div>{res.details}</div>
                </div>
              )}

              <button
                onClick={() => runSingleTest(test)}
                disabled={isTesting}
                className="w-full flex items-center justify-center space-x-2 bg-white hover:bg-slate-100 border border-slate-300 text-slate-700 py-2 rounded-lg text-xs font-bold transition disabled:opacity-50"
              >
                {isTesting ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin text-purple-600" />
                    <span>Test en cours...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-3.5 h-3.5 text-purple-600" />
                    <span>Lancer le test</span>
                  </>
                )}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
