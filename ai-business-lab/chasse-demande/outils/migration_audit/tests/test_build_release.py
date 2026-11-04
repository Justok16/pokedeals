from __future__ import annotations

import hashlib
import re
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_release import build_release, verify_archive, verify_sidecar


class BuildReleaseTests(unittest.TestCase):
    def make_source(self, root: Path) -> None:
        (root / "tests").mkdir(parents=True)
        (root / "README.md").write_text("release test\n", encoding="utf-8")
        (root / "tests" / "test_sample.py").write_text("assert True\n", encoding="utf-8")
        (root / "__pycache__").mkdir()
        (root / "__pycache__" / "ignored.pyc").write_bytes(b"cache")
        (root / ".venv").mkdir()
        (root / ".venv" / "secret.txt").write_text("ignored", encoding="utf-8")

    def test_builds_archive_and_verifies_all_manifest_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "project"
            source.mkdir()
            self.make_source(source)
            archive = base / "release.zip"
            build_release(source, archive)
            names = verify_archive(archive)
            self.assertIn("project/README.md", names)
            self.assertIn("project/MANIFEST.sha256", names)
            self.assertTrue(verify_sidecar(archive))

    def test_archive_is_deterministic_for_identical_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "project"
            source.mkdir()
            self.make_source(source)
            first = base / "first.zip"
            second = base / "second.zip"
            digest_one = build_release(source, first)
            digest_two = build_release(source, second)
            self.assertEqual(digest_one, digest_two)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_cache_and_virtual_environment_are_excluded(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "project"
            source.mkdir()
            self.make_source(source)
            archive = base / "release.zip"
            build_release(source, archive)
            with zipfile.ZipFile(archive) as zf:
                names = zf.namelist()
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(".venv" in name for name in names))

    def test_output_inside_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "project"
            source.mkdir()
            self.make_source(source)
            with self.assertRaisesRegex(ValueError, "hors du dossier source"):
                build_release(source, source / "release.zip")

    def test_external_checksum_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "project"
            source.mkdir()
            self.make_source(source)
            archive = base / "release.zip"
            build_release(source, archive)
            archive.write_bytes(archive.read_bytes() + b"tampered")
            with self.assertRaisesRegex(ValueError, "SHA-256 externe"):
                verify_sidecar(archive)

    def test_tampered_archive_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "project"
            source.mkdir()
            self.make_source(source)
            archive = base / "release.zip"
            build_release(source, archive)
            bad = base / "bad.zip"
            with zipfile.ZipFile(archive) as original, zipfile.ZipFile(bad, "w") as target:
                for item in original.infolist():
                    data = original.read(item.filename)
                    if item.filename == "project/README.md":
                        data += b"tampered\n"
                    target.writestr(item, data)
            with self.assertRaisesRegex(ValueError, "empreinte incorrecte"):
                verify_archive(bad)

    def test_version_metadata_is_synchronised(self):
        project = Path(__file__).resolve().parents[1]
        version_line = next(line for line in (project / "migration_audit.py").read_text(encoding="utf-8").splitlines() if line.startswith("VERSION = "))
        version = version_line.split('"')[1]
        readme = (project / "README.md").read_text(encoding="utf-8")
        changelog = (project / "CHANGELOG.md").read_text(encoding="utf-8")
        verification = (project / "VERIFICATION.txt").read_text(encoding="utf-8")
        self.assertTrue(readme.startswith(f"# DIG16 Migration Audit {version}\n"))
        self.assertTrue(changelog.startswith(f"# Changelog\n\n## {version} "))
        self.assertIn(f"DIG16 Migration Audit {version}", verification)
        test_count = sum(
            len(re.findall(r"^\s+def test_", path.read_text(encoding="utf-8"), flags=re.MULTILINE))
            for path in (project / "tests").glob("test_*.py")
        )
        self.assertIn(f"La suite comprend {test_count} tests", readme)
        self.assertIn(f"Tests unitaires: {test_count}/{test_count} PASS", verification)


    def test_verify_sidecar_rejects_malformed_checksum_and_wrong_filename(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "project"
            source.mkdir()
            self.make_source(source)
            archive = base / "release.zip"
            build_release(source, archive)
            sidecar = Path(str(archive) + ".sha256")
            for bad_value, message in (
                ("not-a-digest  release.zip\n", "format"),
                (("0" * 64) + "  another.zip\n", "bon ZIP"),
                ("\n", "format"),
            ):
                with self.subTest(value=bad_value):
                    sidecar.write_text(bad_value, encoding="ascii")
                    with self.assertRaisesRegex(ValueError, message):
                        verify_sidecar(archive)

    def test_verify_archive_rejects_duplicate_file_members(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "project"
            source.mkdir()
            self.make_source(source)
            archive = base / "release.zip"
            build_release(source, archive)
            duplicate = base / "duplicate.zip"
            with zipfile.ZipFile(archive, "r") as original, zipfile.ZipFile(duplicate, "w") as target:
                for name in original.namelist():
                    target.writestr(name, original.read(name))
                target.writestr("project/README.md", b"duplicate")
            with self.assertRaisesRegex(ValueError, "dupliqué"):
                verify_archive(duplicate)

    def test_workflow_runs_release_builder_after_unit_tests(self):
        project = Path(__file__).resolve().parents[1]
        workflow = (project / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")
        self.assertIn("python build_release.py --output", workflow)
        self.assertIn("runner.temp", workflow)


if __name__ == "__main__":
    unittest.main()
