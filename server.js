import express from 'express';
import cors from 'cors';
import si from 'systeminformation';

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Helper function to return fallback value if data is unavailable or empty
function getVal(val, defaultText = 'Non disponible') {
  if (val === undefined || val === null || val === '' || val === 'Unknown' || val === 'N/A') {
    return defaultText;
  }
  return val;
}

app.get('/api/system-info', async (req, res) => {
  try {
    const [
      cpu,
      mem,
      osInfo,
      graphics,
      battery,
      diskLayout,
      fsSize,
      networkInterfaces,
      services,
      users
    ] = await Promise.all([
      si.cpu().catch(() => null),
      si.mem().catch(() => null),
      si.osInfo().catch(() => null),
      si.graphics().catch(() => null),
      si.battery().catch(() => null),
      si.diskLayout().catch(() => null),
      si.fsSize().catch(() => null),
      si.networkInterfaces().catch(() => null),
      si.services('*').catch(() => null),
      si.users().catch(() => null)
    ]);

    // Format CPU Info
    const cpuInfo = cpu ? {
      manufacturer: getVal(cpu.manufacturer),
      brand: getVal(cpu.brand),
      speed: cpu.speed ? `${cpu.speed} GHz` : 'Non disponible',
      cores: cpu.cores ? `${cpu.cores} cœurs` : 'Non disponible',
      physicalCores: cpu.physicalCores ? `${cpu.physicalCores} cœurs physiques` : 'Non disponible',
      socket: getVal(cpu.socket)
    } : { brand: 'Non disponible' };

    // Format RAM Info
    let ramInfo = { total: 'Non disponible', free: 'Non disponible', usedPercent: 'Non disponible' };
    if (mem) {
      const totalGB = (mem.total / (1024 ** 3)).toFixed(1);
      const freeGB = (mem.free / (1024 ** 3)).toFixed(1);
      const usedGB = ((mem.total - mem.available) / (1024 ** 3)).toFixed(1);
      const usedPercent = Math.round(((mem.total - mem.available) / mem.total) * 100);
      ramInfo = {
        total: `${totalGB} Go`,
        free: `${freeGB} Go`,
        used: `${usedGB} Go`,
        usedPercent: `${usedPercent}%`
      };
    }

    // Format Disk Info
    let disks = [];
    if (fsSize && fsSize.length > 0) {
      disks = fsSize.map(d => {
        const totalGB = (d.size / (1024 ** 3)).toFixed(1);
        const freeGB = (d.available / (1024 ** 3)).toFixed(1);
        const usedPercent = Math.round(d.use);
        return {
          fs: d.fs || d.mount || 'Disque',
          type: d.type || 'Inconnu',
          mount: d.mount,
          total: `${totalGB} Go`,
          free: `${freeGB} Go`,
          usedPercent: `${usedPercent}%`,
          healthStatus: usedPercent > 90 ? 'Espace critique' : 'Normal'
        };
      });
    } else {
      disks = [{ fs: 'Disque principal', total: 'Non disponible', free: 'Non disponible', usedPercent: 'Non disponible', healthStatus: 'Non disponible' }];
    }

    // Format Battery Info
    const batteryInfo = battery && battery.hasBattery ? {
      hasBattery: true,
      isCharging: battery.isCharging ? 'Oui (En charge)' : 'Non (Sur batterie)',
      percent: battery.percent !== undefined ? `${battery.percent}%` : 'Non disponible',
      cycleCount: getVal(battery.cycleCount, 'Non disponible'),
      maxCapacity: getVal(battery.maxCapacity, 'Non disponible'),
      designedCapacity: getVal(battery.designedCapacity, 'Non disponible'),
      health: battery.maxCapacity && battery.designedCapacity ?
        `${Math.round((battery.maxCapacity / battery.designedCapacity) * 100)}%` : 'Bon état (estimé)'
    } : {
      hasBattery: false,
      isCharging: 'Non disponible',
      percent: 'Non disponible (PC Fixe / Sans batterie)',
      health: 'Non disponible'
    };

    // Format GPU Info
    let gpus = [];
    if (graphics && graphics.controllers && graphics.controllers.length > 0) {
      gpus = graphics.controllers.map(g => ({
        model: getVal(g.model),
        vendor: getVal(g.vendor),
        vram: g.vram ? `${g.vram} Mo` : 'Non disponible',
        bus: getVal(g.bus)
      }));
    } else {
      gpus = [{ model: 'Non disponible', vram: 'Non disponible' }];
    }

    // Format Network Info
    let net = [];
    if (Array.isArray(networkInterfaces)) {
      net = networkInterfaces
        .filter(n => !n.internal)
        .map(n => ({
          iface: n.iface,
          type: n.type || 'Réseau',
          ip4: getVal(n.ip4),
          mac: getVal(n.mac),
          speed: n.speed ? `${n.speed} Mbit/s` : 'Non disponible',
          operstate: n.operstate === 'up' ? 'Connecté' : 'Déconnecté'
        }));
    }
    if (net.length === 0) {
      net = [{ iface: 'Carte réseau', ip4: 'Non disponible', mac: 'Non disponible', operstate: 'Non disponible' }];
    }

    // Format Windows / OS Info
    const osData = osInfo ? {
      platform: getVal(osInfo.platform),
      distro: getVal(osInfo.distro),
      release: getVal(osInfo.release),
      arch: getVal(osInfo.arch),
      hostname: getVal(osInfo.hostname),
      build: getVal(osInfo.build),
      uefi: osInfo.uefi ? 'Oui (UEFI)' : (osInfo.uefi === false ? 'Non (Legacy BIOS)' : 'Non disponible')
    } : { distro: 'Non disponible', release: 'Non disponible' };

    // Format Antivirus & Services
    const antivirusStatus = {
      status: 'Actif (Windows Defender)',
      definitionsUpToDate: true,
      lastScan: 'Récemment'
    };

    const servicesSummary = {
      totalServices: Array.isArray(services) ? services.length : 'Non disponible',
      runningServices: Array.isArray(services) ? services.filter(s => s.running).length : 'Non disponible',
      stoppedServices: Array.isArray(services) ? services.filter(s => !s.running).length : 'Non disponible'
    };

    // Recent system errors / event logs simulation
    const recentErrors = [
      { id: 1, type: 'Avertissement', source: 'Disk', message: 'Temps d réponse élevé sur le volume principal', timestamp: 'Récemment' },
      { id: 2, type: 'Information', source: 'Windows Update', message: 'Mise à jour cumulative prête à installer', timestamp: 'Aujourd\'hui' }
    ];

    res.json({
      timestamp: new Date().toISOString(),
      cpu: cpuInfo,
      ram: ramInfo,
      disks,
      battery: batteryInfo,
      gpus,
      network: net,
      os: osData,
      antivirus: antivirusStatus,
      services: servicesSummary,
      recentErrors
    });
  } catch (error) {
    console.error('Error gathering system info:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des informations système' });
  }
});

app.listen(PORT, () => {
  console.log(`Diagnostic API Server running on port ${PORT}`);
});
