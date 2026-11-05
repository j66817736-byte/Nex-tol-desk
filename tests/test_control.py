from __future__ import annotations

import unittest

from control.catalog import get_modules
from control.jobs import JobManager


class CatalogTests(unittest.TestCase):
    def test_catalog_is_copy_and_has_data_boundary(self) -> None:
        modules = get_modules()
        self.assertTrue(any(module["id"] == "data" and module["status"] == "disconnected" for module in modules))
        modules.clear()
        self.assertTrue(get_modules())


class JobManagerTests(unittest.TestCase):
    def test_diagnostic_explains_steps_and_does_not_claim_external_access(self) -> None:
        manager = JobManager()
        job = manager.run_diagnostic()
        self.assertEqual(job["status"], "completed")
        self.assertEqual(len(job["steps"]), 4)
        self.assertEqual(manager.list_jobs()[0]["id"], job["id"])
        self.assertIn("no lee", job["note"])


if __name__ == "__main__":
    unittest.main()
