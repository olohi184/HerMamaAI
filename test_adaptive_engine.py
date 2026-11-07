"""Run with python -m unittest -v test_adaptive_engine.py"""
import unittest
from adaptive_engine import build_plan, progress_summary, GOALS, STAGES, CAPACITIES

class AdaptiveEngineTests(unittest.TestCase):
    def p(self, **changes):
        args = dict(stage="Pregnancy", goal="Rest and recovery", capacity="Moderate", setback=False, concern="None")
        args.update(changes)
        return build_plan(**args)
    def test_low_energy_smaller_plan(self):
        self.assertEqual(len(self.p(capacity="Low").actions), 1)
    def test_high_energy_two_actions(self):
        self.assertEqual(len(self.p(capacity="High").actions), 2)
    def test_restart_reduces_steps(self):
        self.assertEqual(len(self.p(setback=True).actions), 1)
    def test_incomplete_previous_checkin_reduces_steps(self):
        self.assertEqual(len(self.p(previous_completed=False).actions), 1)
    def test_explainability(self):
        self.assertIn("low energy", " ".join(self.p(capacity="Low").explanation))
    def test_urgent_overrides_all_goals_stages_energy(self):
        for stage in STAGES:
            for goal in GOALS:
                for capacity in CAPACITIES:
                    plan = self.p(stage=stage, goal=goal, capacity=capacity, setback=True, concern="I need urgent medical help")
                    self.assertEqual(plan.urgency, "urgent")
                    self.assertEqual(plan.actions, ())
    def test_health_concern_pauses_habits(self):
        plan = self.p(concern="I have a health concern")
        self.assertEqual(plan.actions, ())
        self.assertEqual(plan.urgency, "concern")
    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            self.p(goal="Unknown")
    def test_empty_dashboard(self):
        self.assertEqual(progress_summary([])["completion_fraction"], 0)
    def test_progress_summary(self):
        self.assertEqual(progress_summary([{"completed": True}, {"completed": False}])["completion_fraction"], .5)

if __name__ == "__main__":
    unittest.main()
