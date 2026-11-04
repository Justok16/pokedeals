import csv
import os
import socket
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from migration_audit import AuditResult, assert_public_destination, audit_one, load_mappings, main, normalized_url, write_report  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self._route()

    def do_GET(self):
        self._route()

    def _route(self):
        routes = {
            "/old-301": (301, "/new"),
            "/old-302": (302, "/new"),
            "/new": (200, None),
            "/wrong": (200, None),
            "/loop-a": (301, "/loop-b"),
            "/loop-b": (308, "/loop-a"),
            "/chain-a": (301, "/chain-b"),
            "/chain-b": (308, "/new"),
            "/short-a": (301, "/short-b"),
            "/short-b": (301, "/short-c"),
            "/short-c": (301, "/short-d"),
            "/short-d": (301, "/new"),
            "/long-a": (301, "/long-b"),
            "/long-b": (301, "/long-c"),
            "/long-c": (301, "/long-d"),
            "/long-d": (301, "/long-e"),
            "/long-e": (301, "/new"),
            "/no-head": (405 if self.command == "HEAD" else 200, None),
            "/no-location": (301, None),
            "/multiple-choices": (300, None),
        }
        status, location = routes.get(self.path, (404, None))
        self.send_response(status)
        if location:
            self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, *_args):
        pass


class MigrationAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_normalizes_scheme_host_default_port_and_fragment(self):
        self.assertEqual(normalized_url("HTTPS://Example.COM:443/a#x"), "https://example.com/a")

    def test_default_port_zero_is_not_normalized_away(self):
        self.assertEqual(normalized_url("http://example.com:0/a"), "http://example.com:0/a")

    def test_blocks_private_ip_destinations_by_default(self):
        with self.assertRaisesRegex(ValueError, "non publique"):
            assert_public_destination("http://127.0.0.1:8000/")

    def test_blocks_hostname_that_resolves_to_private_ip(self):
        answer = [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", ("10.0.0.8", 80))]
        with patch("migration_audit.socket.getaddrinfo", return_value=answer):
            with self.assertRaisesRegex(ValueError, "non publique"):
                assert_public_destination("http://internal.example/")

    def test_hostname_connection_uses_the_pinned_resolved_ip(self):
        answer = [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", ("127.0.0.1", self.server.server_port))]
        old_url = f"http://example.invalid:{self.server.server_port}/old-301"
        new_url = f"http://example.invalid:{self.server.server_port}/new"
        with patch("migration_audit.socket.getaddrinfo", return_value=answer):
            result = audit_one(old_url, new_url, allow_private_hosts=True)
        self.assertEqual(result.outcome, "PASS")
        self.assertEqual(result.redirect_statuses, "301")

    def test_audit_blocks_private_hosts_before_request(self):
        result = audit_one("http://127.0.0.1:8000/old", "http://127.0.0.1:8000/new")
        self.assertEqual(result.outcome, "ERROR")
        self.assertIn("BLOCKED_PRIVATE_OR_UNRESOLVABLE_HOST", result.flags)
        self.assertEqual(result.final_status, "")

    def test_https_to_http_downgrade_is_reported(self):
        mocked = [
            (301, {"Location": "http://new.example/page"}, "https://old.example/page", "HEAD"),
            (200, {}, "http://new.example/page", "HEAD"),
        ]
        with patch("migration_audit.resolve_destination_ip", return_value="93.184.216.34"), \
             patch("migration_audit._request_once", side_effect=mocked):
            result = audit_one(
                "https://old.example/page", "http://new.example/page", allow_private_hosts=True
            )
        self.assertEqual(result.outcome, "FAIL")
        self.assertIn("HTTPS_DOWNGRADE", result.flags)

    def test_rejects_non_http_scheme(self):
        with self.assertRaises(ValueError):
            normalized_url("ftp://example.com/a")

    def test_rejects_embedded_credentials(self):
        with self.assertRaises(ValueError):
            normalized_url("https://user:pass@example.com/")

    def test_permanent_redirect_passes(self):
        result = audit_one(self.base + "/old-301", self.base + "/new", allow_private_hosts=True)
        self.assertEqual(result.outcome, "PASS")
        self.assertEqual(result.redirect_statuses, "301")

    def test_temporary_redirect_fails(self):
        result = audit_one(self.base + "/old-302", self.base + "/new", allow_private_hosts=True)
        self.assertEqual(result.outcome, "FAIL")
        self.assertIn("NON_PERMANENT_REDIRECT", result.flags)

    def test_wrong_destination_fails(self):
        result = audit_one(self.base + "/old-301", self.base + "/wrong", allow_private_hosts=True)
        self.assertIn("WRONG_DESTINATION", result.flags)

    def test_missing_redirect_fails(self):
        result = audit_one(self.base + "/new", self.base + "/wrong", allow_private_hosts=True)
        self.assertIn("MISSING_REDIRECT", result.flags)

    def test_loop_is_detected(self):
        result = audit_one(self.base + "/loop-a", self.base + "/new", allow_private_hosts=True)
        self.assertIn("REDIRECT_LOOP", result.flags)

    def test_chain_is_reported_as_warning(self):
        result = audit_one(self.base + "/chain-a", self.base + "/new", allow_private_hosts=True)
        self.assertEqual(result.outcome, "WARNING")
        self.assertIn("REDIRECT_CHAIN", result.flags)

    def test_head_405_falls_back_to_get(self):
        result = audit_one(self.base + "/no-head", self.base + "/no-head", allow_private_hosts=True)
        self.assertEqual(result.outcome, "PASS")
        self.assertEqual(result.final_status, "200")

    def test_unhandled_three_hundred_status_is_not_a_success(self):
        result = audit_one(self.base + "/multiple-choices", self.base + "/multiple-choices", allow_private_hosts=True)
        self.assertIn("FINAL_HTTP_ERROR", result.flags)

    def test_invalid_url_is_reported_without_network_request(self):
        result = audit_one("ftp://invalid.example/path", "https://new.example/path")
        self.assertEqual(result.outcome, "ERROR")
        self.assertIn("INVALID_URL", result.flags)

    def test_redirect_without_location_is_reported(self):
        result = audit_one(self.base + "/no-location", self.base + "/new", allow_private_hosts=True)
        self.assertIn("REDIRECT_WITHOUT_LOCATION", result.flags)

    def test_max_redirects_is_enforced(self):
        result = audit_one(self.base + "/chain-a", self.base + "/new", max_redirects=1, allow_private_hosts=True)
        self.assertIn("TOO_MANY_REDIRECTS", result.flags)

    def test_conflicting_csv_mappings_are_not_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "map.csv"
            path.write_text(
                "old_url,new_url\nhttps://old.example/a,https://new.example/a\nhttps://old.example/a,https://new.example/b\n",
                encoding="utf-8",
            )
            rows = load_mappings(path)
            self.assertTrue(all(row[2] for row in rows))

    def test_exact_duplicate_csv_mapping_is_flagged(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "duplicate.csv"
            path.write_text(
                "old_url,new_url\nhttps://old.example/a,https://new.example/a\nhttps://old.example/a,https://new.example/a\n",
                encoding="utf-8",
            )
            rows = load_mappings(path)
            self.assertIsNone(rows[0][2])
            self.assertTrue(rows[1][2].startswith("DUPLICATE_MAPPING:"))

    def test_duplicate_csv_headers_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "duplicate_headers.csv"
            path.write_text(
                "old_url,new_url,old_url\nhttps://old.example/a,https://new.example/a,https://old.example/b\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "colonnes en double"):
                load_mappings(path)

    def test_empty_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.csv"
            path.write_text("old_url,new_url\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_mappings(path)

    def test_semicolon_delimited_french_csv_is_supported(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "mapping.csv"
            path.write_text(
                "old_url;new_url\nhttps://old.example/a;https://new.example/a\n",
                encoding="utf-8-sig",
            )
            rows = load_mappings(path)
            self.assertEqual(rows, [("https://old.example/a", "https://new.example/a", None)])

    def test_blank_csv_rows_are_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "mapping.csv"
            path.write_text(
                "old_url,new_url\nhttps://old.example/a,https://new.example/a\n,\n",
                encoding="utf-8",
            )
            rows = load_mappings(path)
            self.assertEqual(len(rows), 1)


    def test_five_hop_chain_fails(self):
        result = audit_one(self.base + "/long-a", self.base + "/new", allow_private_hosts=True)
        self.assertEqual(result.redirect_count, 5)
        self.assertEqual(result.outcome, "FAIL")
        self.assertIn("LONG_REDIRECT_CHAIN", result.flags)

    def test_four_hop_chain_remains_warning(self):
        result = audit_one(self.base + "/short-a", self.base + "/new", allow_private_hosts=True)
        self.assertEqual(result.redirect_count, 4)
        self.assertEqual(result.outcome, "WARNING")
        self.assertIn("REDIRECT_CHAIN", result.flags)
        self.assertNotIn("LONG_REDIRECT_CHAIN", result.flags)

    def test_cli_rejects_non_finite_timeout(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "mapping.csv"
            csv_path.write_text("old_url,new_url\nhttps://old.example/a,https://new.example/a\n", encoding="utf-8")
            for invalid_timeout in ("nan", "inf", "-inf"):
                with self.subTest(timeout=invalid_timeout), patch("sys.stderr"):
                    with self.assertRaises(SystemExit) as raised:
                        main([str(csv_path), "--timeout", invalid_timeout])
                    self.assertEqual(raised.exception.code, 2)

    def test_mixed_public_and_private_dns_answers_are_blocked(self):
        answers = [
            (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", ("93.184.216.34", 80)),
            (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", ("10.0.0.8", 80)),
        ]
        with patch("migration_audit.socket.getaddrinfo", return_value=answers):
            with self.assertRaisesRegex(ValueError, "non publique"):
                assert_public_destination("http://mixed.example/")

    def test_cli_writes_report_and_returns_success(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "mapping.csv"
            report_path = Path(temp) / "report.csv"
            csv_path.write_text(
                f"old_url,new_url\n{self.base}/old-301,{self.base}/new\n",
                encoding="utf-8",
            )
            code = main([str(csv_path), "--output", str(report_path), "--allow-private-hosts"])
            self.assertEqual(code, 0)
            self.assertTrue(report_path.exists())
            with report_path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle, delimiter=";"))
            self.assertEqual(rows[0]["outcome"], "PASS")

    def test_cli_refuses_to_overwrite_source_csv(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "mapping.csv"
            original = "old_url,new_url\nhttps://old.example/a,https://new.example/a\n"
            csv_path.write_text(original, encoding="utf-8")
            code = main([str(csv_path), "--output", str(csv_path)])
            self.assertEqual(code, 2)
            self.assertEqual(csv_path.read_text(encoding="utf-8"), original)

    def test_report_is_utf8_bom_and_semicolon_delimited(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.csv"
            result = audit_one(self.base + "/old-301", self.base + "/new", allow_private_hosts=True)
            write_report([result], path)
            raw = path.read_bytes()
            self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
            with path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle, delimiter=";"))
            self.assertEqual(rows[0]["outcome"], "PASS")


    def test_csv_extra_columns_are_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "extra.csv"
            path.write_text(
                "old_url,new_url\nhttps://old.example/a,https://new.example/a,unexpected\n",
                encoding="utf-8",
            )
            rows = load_mappings(path)
            self.assertEqual(len(rows), 1)
            self.assertIn("colonnes supplémentaires", rows[0][2])

    def test_malformed_csv_quoting_is_reported_as_value_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "malformed.csv"
            path.write_text(
                'old_url,new_url\n"https://old.example/a,https://new.example/a\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "CSV mal formé"):
                load_mappings(path)

    def test_report_neutralizes_formula_injection_cells(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.csv"
            result = AuditResult(
                old_url="=1+1", expected_url="+SUM(1,2)", outcome="PASS", flags="",
                redirect_count=1, redirect_statuses="301", final_status="200",
                final_url="@HYPERLINK(\"https://evil.example\")", chain="-cmd",
                detail="safe text",
            )
            write_report([result], path)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle, delimiter=";"))
            self.assertEqual(row["old_url"], "'=1+1")
            self.assertEqual(row["expected_url"], "'+SUM(1,2)")
            self.assertTrue(row["final_url"].startswith("'@"))
            self.assertEqual(row["chain"], "'-cmd")

    def test_report_neutralizes_formula_after_leading_whitespace(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.csv"
            result = AuditResult(
                old_url="  =1+1", expected_url="\t@SUM(A1)", outcome="PASS", flags="",
                redirect_count=0, redirect_statuses="", final_status="200",
                final_url="https://example.com/", chain="", detail="",
            )
            write_report([result], path)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle, delimiter=";"))
            self.assertEqual(row["old_url"], "'  =1+1")
            self.assertEqual(row["expected_url"], "'\t@SUM(A1)")

    def test_report_preserves_ordinary_text_cells(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.csv"
            result = AuditResult(
                old_url="https://old.example/", expected_url="https://new.example/", outcome="PASS", flags="",
                redirect_count=1, redirect_statuses="301", final_status="200",
                final_url="https://new.example/", chain="https://old.example/ -> https://new.example/",
                detail="contrôle normal",
            )
            write_report([result], path)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle, delimiter=";"))
            self.assertEqual(row["detail"], "contrôle normal")

    def test_cli_rejects_python_below_supported_minimum(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "mapping.csv"
            csv_path.write_text("old_url,new_url\nhttps://old.example/a,https://new.example/a\n", encoding="utf-8")
            with patch("migration_audit.sys.version_info", (3, 10, 99)), patch("sys.stderr"):
                with self.assertRaises(SystemExit) as raised:
                    main([str(csv_path)])
            self.assertEqual(raised.exception.code, 2)


    def test_cli_refuses_to_overwrite_source_through_hard_link(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "mapping.csv"
            hard_link = Path(temp) / "report.csv"
            original = "old_url,new_url\nhttps://old.example/a,https://new.example/a\n"
            csv_path.write_text(original, encoding="utf-8")
            try:
                os.link(csv_path, hard_link)
            except (OSError, NotImplementedError):
                self.skipTest("hard links are not supported in this environment")
            with patch("sys.stderr"):
                self.assertEqual(main([str(csv_path), "-o", str(hard_link)]), 2)
            self.assertEqual(csv_path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
