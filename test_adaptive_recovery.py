import unittest
from datetime import date
from adaptive_recovery import recovery_plan, weekly_progress

class RecoveryTests(unittest.TestCase):
    def plan(self, **kwargs):
        args = dict(stage="Pregnancy", goal="Rest and recovery", capacity="High",
                    setback=False, concern="None", sleep="Restful", stress="Low",
                    today=date(2026,11,17))
        args.update(kwargs)
        return recovery_plan(**args)
    def test_normal(self):
        self.assertEqual(len(self.plan().actions), 2)
    def test_sleep(self):
        self.assertEqual(len(self.plan(sleep="Poor").actions), 1)
    def test_stress(self):
        self.assertIn("Comeback Coach", self.plan(stress="High").message)
    def test_gap(self):
        p = self.plan(history=[{"date":"2026-11-14","goal":"Rest and recovery","completed":True}])
        self.assertIn("gap", " ".join(p.explanation))
    def test_safety(self):
        for concern in ("I need urgent medical help","I have a health concern"):
            self.assertEqual(self.plan(concern=concern, sleep="Poor",stress="High").actions, ())
    def test_unique_days(self):
        r = {"date":"2026-11-17","completed":True}
        self.assertEqual(weekly_progress([r,r],date(2026,11,17))["completed_days"],1)
