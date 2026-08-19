import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.cli import main  # noqa: E402
from medlit.downstream import inspect_downstream  # noqa: E402


class DownstreamStatusTests(unittest.TestCase):
    def test_inspection_distinguishes_local_exports_from_optional_tools(self):
        with tempfile.TemporaryDirectory() as temp:
            library = Path(temp) / "zotero.json"
            library.write_text("[]", encoding="utf-8")
            result = inspect_downstream(
                env={"ZOTERO_LIBRARY_JSON": str(library)},
                which_fn=lambda name: "C:/tools/mineru.exe" if name == "mineru" else None,
            )
        self.assertEqual(result["zotero"]["status"], "READY_LOCAL_EXPORT")
        self.assertEqual(result["mineru"]["status"], "READY_LOCAL_TOOL")
        self.assertEqual(result["paperqa2"]["status"], "OPTIONAL_UNVERIFIED")
        self.assertFalse(result["policy"]["allow_cloud_fulltext"])

    def test_inspection_accepts_explicit_isolated_tool_paths(self):
        result = inspect_downstream(
            env={"MEDLIT_PAPERQA_BIN": "D:/isolated/pqa.exe"},
            which_fn=lambda _name: None,
        )
        self.assertEqual(result["paperqa2"]["status"], "CONFIGURED_PATH_UNVERIFIED")
        self.assertEqual(result["paperqa2"]["path"], "D:/isolated/pqa.exe")

    def test_audit_cli_returns_actionable_gate_report(self):
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), patch("medlit.downstream.shutil.which", return_value=None), io.StringIO() as _unused:
            with __import__("contextlib").redirect_stdout(output):
                code = main(["audit", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "GATES_REPORTED")
        self.assertIn("mineru", payload["downstream"])
        self.assertIn("next_user_action", payload["downstream"]["zotero"])


if __name__ == "__main__":
    unittest.main()
