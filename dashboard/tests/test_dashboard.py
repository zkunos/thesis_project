"""Functional checks against saved analysis results and Streamlit interactions."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
from pathlib import Path
import re
import json
import unittest
import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest
from dashboard import data, views


def app(function):
    return AppTest.from_string(
        f"import streamlit as st\nfrom dashboard.views import {function}\nst.set_page_config(layout='wide')\n{function}()",
        default_timeout=60).run()


class ResultsTests(unittest.TestCase):
    def test_report_values_and_profile_totals(self):
        summary = data.research_summary()
        self.assertEqual((summary["discovery"], summary["validation"], summary["trajectory_n"], summary["trajectory_k"]), (5828,1457,2013,1))
        self.assertAlmostEqual(summary["ari2"], .959, places=3)
        self.assertAlmostEqual(summary["ari3"], .935, places=3)
        self.assertAlmostEqual(summary["scaling_ari"], .243, places=3)
        profile = pd.read_csv(data.RESULTS / "dashboard/robust_profiles.csv")
        sizes = profile.groupby("cluster").n.first()
        self.assertEqual(sorted(sizes.tolist()), [51,185,1221])
        self.assertEqual(int(sizes.sum()), 1457)

    def test_profile_assignment_matches_saved_validation_rows(self):
        manifest = data.table("index_patient_manifest.csv", True)
        validation = manifest[manifest.split == "validation"].head(8)
        raw = data.table("eligible_data_matrix.csv", index_col=0)
        expected = data.table("selected_assignments.csv", True)
        expected = expected[expected.model == "domains:kmeans:2"].set_index("assessment_key")
        for row in validation.itertuples():
            result = data.assign_profile(raw.loc[row.source_row].to_dict(), 2)
            self.assertEqual(result["cluster"], int(expected.loc[row.assessment_key, "cluster"]))
            self.assertTrue(np.isfinite(result["domains"]).all())

    def test_blank_and_nonfinite_input_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            data.assign_profile({})
        with self.assertRaisesRegex(ValueError, "finite"):
            data.assign_profile({"ASPAN": float("inf")})


class InterfaceTests(unittest.TestCase):
    def test_group_colors_and_heatmap_scale_survive_filtering(self):
        view = app("profiles")
        def specs():
            return [json.loads(element.proto.spec) for element in view.get("plotly_chart")]
        original_line, original_heat = specs()
        original_colors = {trace["name"]: trace["line"]["color"] for trace in original_line["data"]}
        view.multiselect[0].set_value([2, 0]).run()
        filtered_line, filtered_heat = specs()
        for trace in filtered_line["data"]:
            self.assertEqual(trace["line"]["color"], original_colors[trace["name"]])
            self.assertEqual(trace["line"]["color"], data.group_colors()[trace["name"]])
        for bound in ["cmin", "cmax"]:
            self.assertEqual(original_heat["layout"]["coloraxis"][bound], filtered_heat["layout"]["coloraxis"][bound])
        explorer = app("explorer")
        for element in explorer.get("plotly_chart"):
            for trace in json.loads(element.proto.spec)["data"]:
                self.assertEqual(trace["marker"]["color"], original_colors[trace["name"]])

    def test_all_pages_render(self):
        for name, function in views.PAGES.items():
            with self.subTest(page=name):
                view = app(function.__name__)
                self.assertFalse(view.exception, [e.message for e in view.exception])
                text = " ".join(str(element.value) for kind in [view.markdown, view.caption, view.info, view.warning] for element in kind)
                self.assertFalse(re.search(r"\baudit(?:ed|ing|s)?\b|\bNB\s*\d+\b|\bnotebooks?\b", text, re.I))

    def test_empty_cluster_selection(self):
        view = app("profiles")
        view.multiselect[0].set_value([]).run()
        self.assertFalse(view.exception)
        self.assertIn("Select at least one", view.info[0].value)

    def test_switch_imputation_and_representation(self):
        view = app("explorer")
        view.selectbox[0].select("KNN").run()
        self.assertFalse(view.exception)
        self.assertEqual(view.metric[1].value, "4")
        view = app("research")
        view.selectbox[0].select("tests").run()
        self.assertFalse(view.exception)

    def test_profile_form(self):
        view = app("new_profile")
        view.button[0].click().run()
        self.assertFalse(view.exception)
        self.assertIn("at least one", view.error[0].value)
        view.number_input[0].set_value(6.)
        view.button[0].click().run()
        self.assertFalse(view.exception)
        self.assertEqual(view.metric[1].value, "1 / 14")
        self.assertTrue(view.warning)


if __name__ == "__main__":
    unittest.main(verbosity=2)
