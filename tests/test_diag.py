import os
import unittest
import pdf_report
import system_diag

class TestPCDiagnostic(unittest.TestCase):
    def test_system_diag_structure(self):
        diag = system_diag.get_system_diagnostics()
        self.assertIn("cpu", diag)
        self.assertIn("ram", diag)
        self.assertIn("disks", diag)
        self.assertIn("battery", diag)
        self.assertIn("os", diag)

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

    def test_pdf_report_generation(self):
        filepath = "/tmp/test_unit_report.pdf"
        if os.path.exists(filepath):
            os.remove(filepath)
        pdf_report.generate_pdf_report(
            filepath,
            {"clientName": "Unit Test Client"},
            {"checklist": {}},
            system_diag.get_system_diagnostics()
        )
        self.assertTrue(os.path.exists(filepath))

if __name__ == "__main__":
    unittest.main()
