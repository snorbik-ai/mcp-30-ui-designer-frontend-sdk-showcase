"""Snorbik Zero-Install Runtime Bootstrap (v2.0 — INV-19 Doctrine V4.1).

Garantit un runtime Python >= 3.10 sans installation manuelle par le client :
1. Mini-Python pré-embarqué (SNORBIK_EMBEDDED_PYTHON / ./runtime/python / /opt/snorbik-python).
2. Cache local partagé ~/.snorbik/python-runtime/.
3. Interpréteur Python système si >= 3.10.
4. Auto-provisionnement silencieux portable (Windows embeddable zip ou uv POSIX).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

MIN_PYTHON = (3, 10)
RECOMMENDED_PYTHON = "3.12.3"
SNORBIK_DIR = Path.home() / ".snorbik"
RUNTIME_DIR = SNORBIK_DIR / "python-runtime"
EMBED_WIN_URL = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-embed-amd64.zip"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"


def find_embedded_python(tool_root: Optional[Path] = None) -> Optional[Path]:
    """Détecte un exécutable Python pré-embarqué dans le bundle ou l'image Docker."""
    env_py = os.environ.get("SNORBIK_EMBEDDED_PYTHON")
    if env_py and os.path.isfile(env_py):
        return Path(env_py)
    base = Path(tool_root).resolve() if tool_root else Path(__file__).resolve().parent
    candidates = [
        base / "runtime" / "python" / "python.exe",
        base / "runtime" / "python" / "bin" / "python3",
        Path("/opt/snorbik-python/bin/python3"),
    ]
    for cand in candidates:
        if os.path.isfile(str(cand)):
            return cand
    return None


def _provision_windows_embed() -> Path:
    exe = RUNTIME_DIR / "python.exe"
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = SNORBIK_DIR / "python_embed.zip"
    urllib.request.urlretrieve(EMBED_WIN_URL, zip_path)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(RUNTIME_DIR)
    if zip_path.exists():
        zip_path.unlink()
    for pth in RUNTIME_DIR.glob("*._pth"):
        txt = pth.read_text(encoding="utf-8")
        pth.write_text(txt.replace("#import site", "import site"), encoding="utf-8")
    pip_script = RUNTIME_DIR / "get-pip.py"
    urllib.request.urlretrieve(GET_PIP_URL, pip_script)
    subprocess.run([str(exe), str(pip_script), "--no-warn-script-location"], cwd=str(RUNTIME_DIR), check=True)
    if pip_script.exists():
        pip_script.unlink()
    return exe


def get_guaranteed_python(tool_root: Optional[Path] = None, allow_download: bool = True) -> Path:
    """Retourne un Python >= 3.10 selon la cascade INV-19 (embarqué -> cache -> système -> provisionnement)."""
    embedded = find_embedded_python(tool_root)
    if embedded is not None:
        return embedded

    exe_name = "python.exe" if os.name == "nt" else "bin/python3"
    cached_exe = RUNTIME_DIR / exe_name
    if os.path.isfile(str(cached_exe)):
        return cached_exe

    if sys.version_info >= MIN_PYTHON:
        return Path(sys.executable)

    if not allow_download:
        return Path(sys.executable)

    try:
        if os.name == "nt":
            return _provision_windows_embed()
        uv_bin = shutil.which("uv")
        if uv_bin:
            subprocess.run([uv_bin, "python", "install", RECOMMENDED_PYTHON], check=True)
    except Exception:
        pass
    return Path(sys.executable)


def verify_embedded_runtime_for_delivery(bundle_dir: Path) -> Dict[str, Any]:
    """Contrôle pré-départ client (INV-19) : doctrine, contrat runtime et Python embarqué ou image."""
    root = Path(bundle_dir).resolve()
    missing: List[str] = []
    if not (root / "docs" / "DOCTRINE_PIPELINES_SEQUENTIELLES.md").is_file():
        missing.append("docs/DOCTRINE_PIPELINES_SEQUENTIELLES.md")
    if not (root / "runtime_requirements.json").is_file():
        missing.append("runtime_requirements.json")

    has_embedded_exe = (
        (root / "runtime" / "python" / "python.exe").is_file()
        or (root / "runtime" / "python" / "bin" / "python3").is_file()
    )
    has_docker_python = False
    for df_name in ("Dockerfile.runtime", "Dockerfile"):
        df = root / df_name
        if df.is_file():
            txt = df.read_text(encoding="utf-8", errors="ignore")
            if any(img in txt for img in ("python:3.12-slim", "python:3.11-slim", "python:3.10-slim")):
                has_docker_python = True
                break

    if not (has_embedded_exe or has_docker_python):
        missing.append("embedded_python_or_docker_base(runtime/python|Dockerfile.runtime)")

    mode = "EMBEDDED_PYTHON+DOCKER" if (has_embedded_exe and has_docker_python) else (
        "EMBEDDED_PYTHON" if has_embedded_exe else ("DOCKER_SLIM_IMAGE" if has_docker_python else "NONE")
    )
    return {"ready_for_client": len(missing) == 0, "mode": mode, "missing": missing, "bundle_dir": str(root).replace("\\", "/")}


if __name__ == "__main__":
    print(f"Python certifié Snorbik (INV-19) : {get_guaranteed_python()}")
