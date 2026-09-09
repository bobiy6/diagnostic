# Mister Genius SA - PC Diagnostic & Rapport Technique

![Mister Genius SA Logo](assets/mister_genius_logo.png)

> **« Il y a toujours une solution »**
> Application autonome et portable de diagnostic PC et d'édition de rapports techniques pour techniciens IT Mister Genius SA.

---

## 📋 Présentation du Projet

**Mister Genius SA - PC Diagnostic & Rapport Technique** est une application desktop Python portable conçue pour s'exécuter directement depuis une clé USB sur les ordinateurs clients (Windows, Linux, macOS).

L'application permet aux techniciens d'effectuer un audit complet du matériel, de réaliser des tests de piétinement (stress test) sécurisés de 25 minutes, d'évaluer la santé globale du PC sur 100 points, et de générer un **rapport PDF professionnel et détaillé** aux couleurs officielles de Mister Genius SA.

---

## ✨ Fonctionnalités Principales

### 👤 1. Fiche Client & Machine
- **Détection Automatique du PC :** Détecte automatiquement la **Marque** (Constructeur), le **Modèle** et le **Numéro de Série** matériel (BIOS, Carte Mère, UUID ou Disque) pour éviter les textes génériques type `"To be filled by O.E.M."`.
- **Date d'Intervention :** Générée automatiquement au jour de la consultation.
- **Classification Client :** Support des profils *Particulier* et *Professionnel* (détermine la fréquence de maintenance conseillée).
- **Conformité RGPD :** Aucune donnée personnelle sensible (adresse, téléphone, email) n'est enregistrée sur la machine client.

### 📋 2. Questionnaire & Relevé Technicien
- **Checklist de Maintenance :** Boutons d'état simples (`oui`, `non`, `inconnu`) pour valider :
  - Dépoussiérage physique des ventilateurs.
  - Remplacement de la pâte thermique.
  - Analyse SMART du disque.
  - Scan Antivirus / Anti-Malware.
  - Mises à jour OS et pilotes.
- **Registre des Pièces Remplacées :** Saisie des composants changés et des motifs d'intervention.
- **Observations Technicien :** Zone de remarques et recommandations techniques.

### 🔍 3. Diagnostic Automatique & Températures en Direct
- **Métriques Matérielles :**
  - **Processeur (CPU) :** Modèle, nombre de cœurs physiques/logiques, fréquence GHz et charge en temps réel.
  - **Mémoire RAM :** Capacité totale, Go utilisés, pourcentage d'occupation et mémoire Swap.
  - **Stockage Disque :** Partitions, système de fichiers, espace libre/utilisé, statistiques d'E/S et évaluation de santé SMART.
  - **Batterie & Alimentation :** Niveau de charge, état de branchement secteur, autonomie estimée et état d'usure.
  - **Système d'Exploitation :** OS, version, architecture, nom d'hôte et temps de fonctionnement (*System Uptime*).
  - **Réseau :** Cartes réseau, adresses IP/MAC, vitesse de liaison et trafic Mo.
- **Ticker Thermique en Direct (2s) :**
  - Mise à jour automatique de la température du CPU, GPU et Disque toutes les 2 secondes sans ralentissement de l'interface.
  - Code couleur dynamique (🟢 Vert < 65°C, 🟡 Jaune 65-80°C, 🔴 Rouge > 80°C).
- **Raccourcis Outils Système :** Accès direct en 1 clic aux utilitaires Windows (*Gestionnaire des tâches*, *Gestionnaire de périphériques*, *Moniteur de ressources*, *Nettoyage de disque*).
- **Exportation :** Boutons pour copier le bilan diagnostic au presse-papier ou l'exporter en JSON.

### ⚡ 4. Benchmarks & Test de Piétinement 25 Minutes
- **Charge Ciblée à ~90% (Protection Matériel) :** Algorithme de stress à cycle de service (*duty cycle*) de ~90% pour tester intensément les composants sans risquer d'endommagement thermique ou de coupure brutale.
- **Test Séquentiel en 5 Étapes (5 min par composant) :**
  1. *Étape 1/5 :* Stress Processeur (CPU) multi-processus sur tous les cœurs.
  2. *Étape 2/5 :* MemTest Intégrité Mémoire RAM (allocation et vérification de motifs).
  3. *Étape 3/5 :* Stress E/S Disque & IOPS 4K (lecture/écriture séquentielle et aléatoire).
  4. *Étape 4/5 :* Stress Carte Graphique (GPU) rendu 3D et transformations matricielles.
  5. *Étape 5/5 :* Analyse de Stabilité Thermique & Système Global.
- **Bouton d'Interruption 🛑 :** Permet d'arrêter le test à tout moment de façon propre et sécurisée.
- **Indicateur d'Anomalies :** Compteur d'erreurs matérielles en temps réel.

### 📊 5. Synthèse & Calcul du Score
- **Calculateur de Santé (sur 100 points) :** Analyse automatique combinant l'état des composants, les résultats de piétinement et la checklist technicien.
- **Prochaine Maintenance Conseillée :**
  - **Particuliers :** Maintenance annuelle (+12 mois).
  - **Professionnels :** Maintenance semi-annuelle (+6 mois).
- **Cartes de Synthèse Visuelles :** Note géante sur 100 avec bordure de couleur dynamique (Vert/Jaune/Rouge) et niveau d'urgence.

### 📄 6. Exportation du Rapport PDF
- **Design Professionnel Mister Genius SA :** Formaté avec ReportLab, incluant le logo haute définition, le bleu officiel Mister Genius (`#0099DA` / `#0072CE`) et la devise *« Il a toujours une solution »*.
- **Contenu Complet :**
  - Informations client et spécifications machine.
  - Note de santé et tableau de bilan par composant.
  - Résultats chiffrés des benchmarks et du test de piétinement 25 min.
  - Relevé de maintenance et pièces remplacées.
  - Zone de signature double (Technicien / Client).

---

## 🏗️ Structure du Projet

```
.
├── app_gui.py                      # Fenêtre principale et navigation CustomTkinter
├── gui_client_view.py              # Vue Fiche Client & Spécifications PC
├── gui_questionnaire_view.py       # Vue Questionnaire & Checklist Technicien
├── gui_diag_view.py                # Vue Diagnostic Auto & Ticker Thermique 2s
├── gui_tests_view.py               # Vue Test de Piétinement 25 min & Interruption
├── gui_synthesis_view.py           # Vue Synthèse & Score sur 100
├── system_diag.py                  # Moteur d'audit matériel psutil / WMI / DMI
├── system_hardware_benchmarks.py   # Moteur de stress test ~90% & multiprocessus
├── pdf_report.py                   # Générateur de rapports PDF ReportLab
├── asset_utils.py                  # Gestionnaire de chemin pour assets PyInstaller
├── build.py                        # Script d'encapsulation PyInstaller pour Clé USB
├── PC_Diagnostic_Rapport_MisterGenius.spec # Fichier de configuration PyInstaller
├── assets/
│   └── mister_genius_logo.png     # Logo officiel Mister Genius SA
└── tests/
    └── test_diag.py                # Tests unitaires
```

---

## 🚀 Installation & Exécution

### Configuration de l'environnement Python
1. Cloner ou télécharger le dépôt sur la machine ou la clé USB.
2. Installer les dépendances requises :
   ```bash
   pip install customtkinter psutil reportlab pillow
   ```

### Lancement de l'application
Pour exécuter l'application en mode développeur ou directement sous Python :
```bash
python3 app_gui.py
```

---

## 📦 Encapsulation Exécutable Portable (Clé USB)

Pour créer un exécutable autonome `.exe` (Windows) ou binaire sans installation Python nécessaire sur le PC client :

```bash
python3 build.py
```

L'exécutable généré se trouvera dans le dossier `dist/` et pourra être copié sur n'importe quelle clé USB de technicien.

---

## 🧪 Tests Unitaires

Pour exécuter la suite de tests automatisée :
```bash
python3 -m unittest discover tests
```

---

## 💙 Charte Graphique Mister Genius SA

- **Cyan Bleu Mister Genius :** `#0099DA`
- **Bleu Genius :** `#0072CE`
- **Jaune Accent :** `#FFC72C`
- **Fond Dark Navy :** `#0F172A` / `#0B0F17`
