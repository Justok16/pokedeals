import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "sans_autopatch_url: desactive l'autopatch de _url_photo_autorisee "
        "dans test_verification_photo.py, pour tester la vraie validation d'URL.",
    )
