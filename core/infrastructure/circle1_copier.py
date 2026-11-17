"""Copieur & Adaptateur Cercle 1 (Banque Interne) + Générateur de Pages N5 Qualifiées."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List
from core.infrastructure.path_utils import safe_path


def _pascal_name(raw: str) -> str:
    cleaned = "".join(w.capitalize() for w in raw.replace("-", " ").replace("_", " ").split())
    return cleaned or "GeneratedPage"


class Circle1AndPagesMaterializer:
    """Matérialise les pièces Cercle 1 depuis le patrimoine réel (si disponible) et les pages N5 qualifiées."""

    def __init__(self, tool_root: Path):
        self.tool_root = tool_root
        self.workspace_root = tool_root.parents[1] if len(tool_root.parents) > 1 else tool_root
        self.index_file = tool_root / "bank" / "06_internal_batihome_200_index.json"

    def _load_index_by_name(self) -> Dict[tuple[str, str], Dict[str, Any]]:
        if not self.index_file.exists():
            return {}
        data = json.loads(self.index_file.read_text(encoding="utf-8"))
        lookup: Dict[tuple[str, str], Dict[str, Any]] = {}
        for lvl, items in data.get("levels", {}).items():
            for it in items:
                lookup[(lvl, it["name"])] = it
        return lookup

    def copy_circle1_parts(self, plan_data: Dict[str, Any], src_dir: Path) -> List[str]:
        """Copie les pièces Cercle 1 trouvées sur disque (repli propre si exécuté hors monorepo)."""
        lookup = self._load_index_by_name()
        copied: List[str] = []
        for item in plan_data.get("items", []):
            if item.get("category") != "EXISTING_IN_BANK":
                continue
            lvl = item.get("dpn_level", "")
            asset_name = item.get("name", "")
            meta = lookup.get((lvl, asset_name))
            if not meta or not meta.get("path"):
                continue
            src_path = safe_path(self.workspace_root / meta["path"])
            if not src_path.exists():
                continue

            if src_path.is_file():
                lines = src_path.read_text(encoding="utf-8", errors="ignore").splitlines()
                if len(lines) <= 350:
                    dst = safe_path(src_dir / "presentation" / lvl / src_path.name)
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
                    copied.append(f"src/presentation/{lvl}/{src_path.name}")
            elif src_path.is_dir():
                folder_slug = asset_name.strip("/")
                dst_dir = safe_path(src_dir / "presentation" / lvl / folder_slug)
                dst_dir.mkdir(parents=True, exist_ok=True)
                for f in src_path.iterdir():
                    if f.is_file() and f.suffix in (".ts", ".tsx"):
                        lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
                        if len(lines) <= 350:
                            (dst_dir / f.name).write_text("\n".join(lines) + "\n", encoding="utf-8")
                            copied.append(f"src/presentation/{lvl}/{folder_slug}/{f.name}")
                if lvl == "02-features":
                    if not (dst_dir / "index.ts").exists():
                        (dst_dir / "index.ts").write_text("// Barrel export auto-généré par MCP #30\nexport {};\n", encoding="utf-8")
                        copied.append(f"src/presentation/{lvl}/{folder_slug}/index.ts")
                    if not any(dst_dir.glob("use*Controller.ts")):
                        ctrl = f"use{_pascal_name(folder_slug)}Controller.ts"
                        (dst_dir / ctrl).write_text("import { useState } from 'react';\nexport function useController() { const [ready] = useState(true); return { ready }; }\n", encoding="utf-8")
                        copied.append(f"src/presentation/{lvl}/{folder_slug}/{ctrl}")
        return copied

    def materialize_qualified_pages(self, state: Dict[str, Any], src_dir: Path) -> List[str]:
        """Génère les pages N5 qualifiées (05-pages/) et leur barrel export index.ts."""
        pages = state.get("qualification", {}).get("pages", [])
        if not pages:
            return []
        pages_dir = safe_path(src_dir / "presentation" / "05-pages")
        pages_dir.mkdir(parents=True, exist_ok=True)
        generated: List[str] = []
        exports: List[str] = ["export * from './DeclarativeWorkspacePage';"]

        for pg in pages:
            n5_list = pg.get("required_parts", {}).get("05-pages", [])
            comp_name = _pascal_name(n5_list[0] if n5_list else pg.get("name", "Page"))
            if not comp_name.endswith("Page"):
                comp_name += "Page"
            sections_hint = ", ".join(pg.get("content", ["Section principale"]))
            code = (
                "import React from 'react';\n"
                "import { WorkbenchLayout } from '../04-shell/WorkbenchLayout';\n"
                "import { SplitWorkbenchSection } from '../03-sections/SplitWorkbenchSection';\n\n"
                f"export const {comp_name}: React.FC = () => (\n"
                f"  <WorkbenchLayout title=\"{pg.get('name', comp_name)}\">\n"
                f"    <SplitWorkbenchSection>\n"
                f"      <div className=\"p-4 text-sm\">{sections_hint}</div>\n"
                f"    </SplitWorkbenchSection>\n"
                f"  </WorkbenchLayout>\n"
                ");\n"
            )
            (pages_dir / f"{comp_name}.tsx").write_text(code, encoding="utf-8")
            generated.append(f"src/presentation/05-pages/{comp_name}.tsx")
            exp = f"export * from './{comp_name}';"
            if exp not in exports:
                exports.append(exp)

        (pages_dir / "index.ts").write_text("\n".join(exports) + "\n", encoding="utf-8")
        generated.append("src/presentation/05-pages/index.ts")
        return generated
