import os
import unittest
import tempfile
import pdf_report
import system_diag
import system_hardware_benchmarks

class TestPCDiagnostic(unittest.TestCase):
    def test_system_diag_detailed_structure(self):
        diag = system_diag.get_system_diagnostics()
        self.assertIn("cpu", diag)
        self.assertIn("freq", diag["cpu"])
        self.assertIn("ram", diag)
        self.assertIn("swap", diag["ram"])
        self.assertIn("disks", diag)
        self.assertIn("battery", diag)
        self.assertIn("wearEstimation", diag["battery"])
        self.assertIn("os", diag)
        self.assertIn("uptime", diag["os"])

    def test_advanced_hardware_benchmarks(self):
        benchmarks = system_hardware_benchmarks.run_all_hardware_benchmarks(quick=True)
        self.assertIn("cpu", benchmarks)
        self.assertIn("ops_per_sec", benchmarks["cpu"])
        self.assertIn("ram", benchmarks)
        self.assertIn("write_read_speed", benchmarks["ram"])
        self.assertIn("errors", benchmarks["ram"])
        self.assertIn("disk", benchmarks)
        self.assertIn("iops_4k", benchmarks["disk"])
        self.assertIn("gpu", benchmarks)
        self.assertIn("fps", benchmarks["gpu"])
        self.assertIn("score_3d", benchmarks["gpu"])
        self.assertIn("battery", benchmarks)

    def test_synthesis_score_particulier(self):
        client_data = {"clientType": "Particulier", "date": "2026-09-01"}
        questionnaire = {"checklist": {"dustCleaned": "oui", "diskScanOk": "oui"}}
        synth = pdf_report.calculate_synthesis(client_data, questionnaire, {})
        self.assertEqual(synth["score"], 100)
        self.assertEqual(synth["nextMaintenanceDate"], "2027-09-01")

    def test_synthesis_score_professionnel(self):
        client_data = {"clientType": "Professionnel", "date": "2026-09-01"}
        questionnaire = {"checklist": {"dustCleaned": "oui"}}
        synth = pdf_report.calculate_synthesis(client_data, questionnaire, {})
        self.assertIn("6 mois", synth["maintenanceInterval"])
        self.assertEqual(synth["nextMaintenanceDate"], "2027-03-01")

    def test_pdf_report_generation_mg_branding(self):
        filepath = os.path.join(tempfile.gettempdir(), "test_mg_unit_report.pdf")
        if os.path.exists(filepath):
            os.remove(filepath)
        benchmarks = system_hardware_benchmarks.run_all_hardware_benchmarks(quick=True)
        pdf_report.generate_pdf_report(
            filepath,
            {"clientName": "Mister Genius SA Test Client"},
            {"checklist": {}},
            system_diag.get_system_diagnostics(),
            benchmarks
        )
        self.assertTrue(os.path.exists(filepath))

if __name__ == "__main__":
    unittest.main()
