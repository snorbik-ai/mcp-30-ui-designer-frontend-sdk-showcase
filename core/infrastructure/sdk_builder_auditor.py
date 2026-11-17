"""Assembleur Dynamique du SDK Frontend V2.0 (React N1-N5 + ACP + Google ADK + ChatKit + Delta Custom) & Auditeur < 350L."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Any, List


def _safe_path(p: Path) -> Path:
    resolved = str(p.resolve())
    if os.name == "nt" and not resolved.startswith("\\\\?\\"):
        return Path("\\\\?\\" + resolved)
    return p


class SdkBuilderAndAuditor:
    """Matérialise physiquement les pièces de la Banque ET les pièces sur-mesure du plan dans N1-N5."""

    def __init__(self, tool_root: Path | None = None):
        self.tool_root = tool_root or Path(__file__).resolve().parents[2]
        self.sessions_dir = self.tool_root / "output" / "sessions"
        self.templates_dir = self.tool_root / "bank" / "templates"

    def materialize_frontend_sdk(self, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id", "ui-sess-default")
        s_dir = self.sessions_dir / session_id
        raw_root = Path(params["target_dir"]) if params.get("target_dir") else (s_dir / "sdk")
        target_root = _safe_path(raw_root)
        src_dir = target_root / "src"

        levels = ["01-primitives", "02-features", "03-sections", "04-shell", "05-pages"]
        for lvl in levels:
            (src_dir / "presentation" / lvl).mkdir(parents=True, exist_ok=True)
        (src_dir / "sdk" / "acp").mkdir(parents=True, exist_ok=True)
        (src_dir / "sdk" / "google-adk").mkdir(parents=True, exist_ok=True)

        generated_files: List[str] = []

        def _write_root(rel_path: str, content: str) -> None:
            p = target_root / rel_path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content.strip() + "\n", encoding="utf-8")
            generated_files.append(rel_path)

        def _write(rel_path: str, content: str) -> None:
            p = src_dir / rel_path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content.strip() + "\n", encoding="utf-8")
            generated_files.append(f"src/{rel_path}")

        # 1. Manifestes package.json (ChatKit, assistant-ui, ACP, ADK) & components.json (shadcn MCP / Magic UI)
        _write_root(
            "package.json",
            json.dumps(
                {
                    "name": "@snorbik/generated-frontend-ui-sdk",
                    "version": "2.0.0",
                    "private": True,
                    "dependencies": {
                        "react": "^19.0.0",
                        "react-dom": "^19.0.0",
                        "@openai/chatkit-react": "^1.0.0",
                        "@assistant-ui/react": "^0.7.0",
                        "@ag-ui/client": "^1.0.0",
                        "lucide-react": "^0.460.0",
                    },
                },
                indent=2,
            ),
        )
        _write_root(
            "components.json",
            json.dumps(
                {
                    "$schema": "https://ui.shadcn.com/schema.json",
                    "style": "new-york",
                    "tsx": True,
                    "aliases": {
                        "primitives": "@/presentation/01-primitives",
                        "features": "@/presentation/02-features",
                        "sections": "@/presentation/03-sections",
                        "shell": "@/presentation/04-shell",
                        "sdk": "@/sdk",
                    },
                },
                indent=2,
            ),
        )

        # 1.5 Copie du Design System Stitch (tokens.css) dans src/styles/tokens.css
        session_tokens = s_dir / "tokens.css"
        if session_tokens.exists():
            _write("styles/tokens.css", session_tokens.read_text(encoding="utf-8"))

        # 2. Copie des connecteurs protocolaires ACP & Google ADK depuis la Banque
        for tpl_src, dst_rel in [
            ("acpClient.ts", "sdk/acp/acpClient.ts"),
            ("googleAdkBridge.ts", "sdk/google-adk/googleAdkBridge.ts"),
            ("useAcpPilotController.ts", "presentation/02-features/acp-pilot-panel/useAcpPilotController.ts"),
            ("AcpPilotPanel.tsx", "presentation/02-features/acp-pilot-panel/AcpPilotPanel.tsx"),
        ]:
            tpl_file = self.templates_dir / tpl_src
            if tpl_file.exists():
                _write(dst_rel, tpl_file.read_text(encoding="utf-8"))

        _write(
            "sdk/index.ts",
            "export * from './acp/acpClient';\nexport * from './google-adk/googleAdkBridge';\nexport * from '../presentation/02-features/acp-pilot-panel';",
        )

        # 3. Niveau 1 (01-primitives)
        _write(
            "presentation/01-primitives/Button.tsx",
            "import React from 'react';\nexport interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> { variant?: 'primary' | 'secondary' | 'ghost'; }\nexport const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, className = '', ...rest }) => (\n  <button className={`px-3 py-1.5 rounded-md font-medium text-sm ${className}`} data-variant={variant} {...rest}>{children}</button>\n);",
        )
        _write(
            "presentation/01-primitives/Badge.tsx",
            "import React from 'react';\nexport const Badge: React.FC<{ label: string; tone?: 'emerald' | 'cyan' | 'amber' }> = ({ label, tone = 'emerald' }) => (\n  <span className=\"px-2 py-0.5 text-xs rounded-full font-semibold\" data-tone={tone}>{label}</span>\n);",
        )
        _write("presentation/01-primitives/index.ts", "export * from './Button';\nexport * from './Badge';")

        # 4. Niveau 2 (02-features/acp-pilot-panel/partials + index.ts)
        _write(
            "presentation/02-features/acp-pilot-panel/partials/PilotHeaderBarPartial.tsx",
            "import React from 'react';\nimport { AgentTransportMode } from '../useAcpPilotController';\nexport const PilotHeaderBarPartial: React.FC<{ title: string; sessionId: string; transportMode: AgentTransportMode; onChangeTransport: (m: AgentTransportMode) => void; }> = ({ title, sessionId, transportMode, onChangeTransport }) => (\n  <header className=\"p-3 border-b border-slate-800 flex items-center justify-between\">\n    <div><h3 className=\"text-sm font-bold\">{title}</h3><span className=\"text-xs text-slate-400\">{sessionId}</span></div>\n    <select value={transportMode} onChange={(e) => onChangeTransport(e.target.value as AgentTransportMode)} className=\"bg-slate-800 text-xs rounded p-1\">\n      <option value=\"ACP\">ACP Protocol</option><option value=\"GOOGLE_ADK\">Google ADK</option><option value=\"OPENAI_CHATKIT\">OpenAI ChatKit</option>\n    </select>\n  </header>\n);",
        )
        _write(
            "presentation/02-features/acp-pilot-panel/partials/PilotMessageStreamPartial.tsx",
            "import React from 'react';\nimport { AcpMessage } from '../../../sdk/acp/acpClient';\nexport const PilotMessageStreamPartial: React.FC<{ messages: AcpMessage[]; isStreaming: boolean }> = ({ messages, isStreaming }) => (\n  <div className=\"flex-1 overflow-y-auto p-3 space-y-2\">\n    {messages.map((m) => (<div key={m.id} className=\"p-2 rounded bg-slate-800/70 text-xs\"><strong>{m.role}:</strong> {m.content}</div>))}\n    {isStreaming && <div className=\"text-xs text-cyan-400 animate-pulse\">Agent IA en cours...</div>}\n  </div>\n);",
        )
        _write(
            "presentation/02-features/acp-pilot-panel/partials/PilotInputQuickChipsPartial.tsx",
            "import React from 'react';\nexport const PilotInputQuickChipsPartial: React.FC<{ inputDraft: string; onChangeInput: (v: string) => void; onSend: (t?: string) => void; quickChips: string[]; disabled?: boolean; }> = ({ inputDraft, onChangeInput, onSend, quickChips, disabled }) => (\n  <footer className=\"p-3 border-t border-slate-800 space-y-2\">\n    <div className=\"flex flex-wrap gap-1\">{quickChips.map((chip) => (<button key={chip} type=\"button\" onClick={() => onSend(chip)} className=\"text-xs px-2 py-0.5 rounded bg-slate-800\">{chip}</button>))}</div>\n    <div className=\"flex gap-2\"><input value={inputDraft} onChange={(e) => onChangeInput(e.target.value)} className=\"flex-1 bg-slate-800 rounded px-2 py-1 text-xs\" /><button type=\"button\" disabled={disabled} onClick={() => onSend()} className=\"px-3 py-1 rounded bg-emerald-600 text-xs\">Envoyer</button></div>\n  </footer>\n);",
        )
        _write(
            "presentation/02-features/acp-pilot-panel/index.ts",
            "export * from './AcpPilotPanel';\nexport * from './useAcpPilotController';",
        )

        # 5. Génération DYNAMIQUE de tous les composants Sur-Mesure (CUSTOM_AI_TO_BUILD) du materialization_plan.json
        plan_file = s_dir / "materialization_plan.json"
        custom_built: List[str] = []
        if plan_file.exists():
            plan_data = json.loads(plan_file.read_text(encoding="utf-8"))
            for item in plan_data.get("items", []):
                if item.get("category") == "CUSTOM_AI_TO_BUILD":
                    comp_name = item["name"].strip("/").replace("Feature", "") or "CustomDomain"
                    folder = f"presentation/02-features/{comp_name}"
                    _write(
                        f"{folder}/use{comp_name}Controller.ts",
                        f"import {{ useState }} from 'react';\nexport function use{comp_name}Controller() {{\n  const [active, setActive] = useState<boolean>(true);\n  return {{ active, setActive }};\n}}",
                    )
                    _write(
                        f"{folder}/partials/{comp_name}BodyPartial.tsx",
                        f"import React from 'react';\nexport const {comp_name}BodyPartial: React.FC<{{ active: boolean }}> = ({{ active }}) => (\n  <div className=\"p-3 rounded border border-slate-700 text-xs\">Module Sur-Mesure {comp_name} ({'{'}active ? 'Actif' : 'Inactif'{'}'})</div>\n);",
                    )
                    _write(
                        f"{folder}/{comp_name}Feature.tsx",
                        f"import React from 'react';\nimport {{ use{comp_name}Controller }} from './use{comp_name}Controller';\nimport {{ {comp_name}BodyPartial }} from './partials/{comp_name}BodyPartial';\nexport const {comp_name}Feature: React.FC = () => {{\n  const ctrl = use{comp_name}Controller();\n  return <{comp_name}BodyPartial active={{ctrl.active}} />;\n}};",
                    )
                    _write(
                        f"{folder}/index.ts",
                        f"export * from './{comp_name}Feature';\nexport * from './use{comp_name}Controller';",
                    )
                    custom_built.append(comp_name)

        # 6. Niveaux 3, 4 et 5
        _write(
            "presentation/03-sections/SplitWorkbenchSection.tsx",
            "import React from 'react';\nimport { AcpPilotPanel } from '../02-features/acp-pilot-panel';\nexport const SplitWorkbenchSection: React.FC<{ children?: React.ReactNode }> = ({ children }) => (\n  <section className=\"grid grid-cols-12 h-full w-full\"><main className=\"col-span-8 p-4\">{children}</main><div className=\"col-span-4 h-full\"><AcpPilotPanel /></div></section>\n);",
        )
        _write(
            "presentation/04-shell/WorkbenchLayout.tsx",
            "import React from 'react';\nexport const WorkbenchLayout: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (\n  <div className=\"min-h-screen bg-slate-950 text-slate-100 flex flex-col\"><header className=\"h-12 px-4 border-b border-slate-800 flex items-center justify-between font-bold text-sm\">{title}</header><div className=\"flex-1\">{children}</div></div>\n);",
        )
        _write(
            "presentation/05-pages/DeclarativeWorkspacePage.tsx",
            "import React from 'react';\nimport { WorkbenchLayout } from '../04-shell/WorkbenchLayout';\nimport { SplitWorkbenchSection } from '../03-sections/SplitWorkbenchSection';\nexport const DeclarativeWorkspacePage: React.FC = () => (\n  <WorkbenchLayout title=\"Snorbik UI SDK Workspace V2.0 (ACP · Google ADK · ChatKit)\"><SplitWorkbenchSection><div className=\"p-4\">Zone Métier Configurée</div></SplitWorkbenchSection></WorkbenchLayout>\n);",
        )

        audit = self.audit_architecture({"session_id": session_id, "target_dir": str(raw_root)})
        return {
            "session_id": session_id,
            "sdk_root_dir": str(raw_root),
            "generated_files_count": len(generated_files),
            "custom_features_materialized": custom_built,
            "generated_files": generated_files,
            "architecture_audit": audit,
        }

    def audit_architecture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id", "ui-sess-default")
        raw_root = Path(params["target_dir"]) if params.get("target_dir") else (self.sessions_dir / session_id / "sdk")
        target_root = _safe_path(raw_root)
        pres_dir = target_root / "src" / "presentation"

        expected_levels = ["01-primitives", "02-features", "03-sections", "04-shell", "05-pages"]
        present_levels = [lvl for lvl in expected_levels if (pres_dir / lvl).exists()]

        violations: List[Dict[str, Any]] = []
        scanned_files = 0
        max_observed_lines = 0

        if target_root.exists():
            for f in target_root.rglob("*"):
                if f.is_file() and f.suffix in (".ts", ".tsx"):
                    scanned_files += 1
                    line_count = len(f.read_text(encoding="utf-8", errors="ignore").splitlines())
                    max_observed_lines = max(max_observed_lines, line_count)
                    if line_count > 350:
                        violations.append({
                            "file": str(f.relative_to(target_root)),
                            "lines": line_count,
                            "rule": "INV-02 Max 350 lines exceeded",
                        })

        # Vérification que chaque sous-dossier de 02-features possède index.ts et un hook use*Controller.ts
        features_dir = pres_dir / "02-features"
        n2_folders_checked = 0
        if features_dir.exists():
            for sub in features_dir.iterdir():
                if sub.is_dir():
                    n2_folders_checked += 1
                    if not (sub / "index.ts").exists():
                        violations.append({"file": str(sub.name), "rule": "Missing barrel export index.ts in N2 feature"})
                    hooks = list(sub.glob("use*Controller.ts"))
                    if not hooks:
                        violations.append({"file": str(sub.name), "rule": "Missing use*Controller.ts in N2 feature"})

        has_manifests = (target_root / "package.json").exists() and (target_root / "components.json").exists()
        compliant = (len(present_levels) == 5) and (len(violations) == 0) and has_manifests
        return {
            "compliant": compliant,
            "dpn_levels_present": present_levels,
            "n2_feature_folders_verified": n2_folders_checked,
            "manifests_present": has_manifests,
            "scanned_ts_files": scanned_files,
            "max_file_lines": max_observed_lines,
            "line_budget_ceiling": 350,
            "violations_count": len(violations),
            "violations": violations,
        }
