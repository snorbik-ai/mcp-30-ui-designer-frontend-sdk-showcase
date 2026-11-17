"""Suite de Tests L4 V3.0 — MCP #30 Usine de Montage Voiture UI (18 Outils, 235+ Composants, Chasse 3 Cercles, Stitch, Zéro Maquette)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from canal_sdk_cli.sdk import UiDesignerFrontendSdkMcpSdk
from canal_mcp.mcp_server import handle_tool_call, TOOLS_METADATA


def test_door3_sdk_ping_and_4_pipelines():
    sdk = UiDesignerFrontendSdkMcpSdk()
    assert sdk.ping()["version"] == "3.0.0"
    pipes = sdk.get_recommended_pipelines()
    assert pipes["pipelines_count"] == 5
    assert "pipeline_zero_maquette_visual_prototyping" in pipes["pipelines"]
    assert len(pipes["pipelines"]["pipeline_usine_montage_voiture_e2e"]["sequence_exact_tools"]) == 11


def test_bank_has_over_200_ready_parts_and_presets():
    sdk = UiDesignerFrontendSdkMcpSdk()
    inv = sdk.list_bank_inventory()
    counts = inv["summary_counts"]
    assert counts["internal_batihome_real_parts"] == 200
    assert counts["total_ready_parts_in_bank"] >= 230
    assert counts["project_archetypes"] >= 5
    assert counts["stitch_presets"] >= 5


def test_car_assembly_workflow_hotel_and_ecommerce_3_circles(tmp_path: Path):
    sdk = UiDesignerFrontendSdkMcpSdk()

    # Scénario Réel : Plateforme Hôtelière avec Concierge IA
    sdk.init_session(
        session_id="test-hotel-v3",
        project_name="SnorbikHotelConcierge",
        vision_brief="Site web hotel avec reservation de chambres, calendrier et concierge IA ChatKit.",
        agent_protocols=["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT"],
        custom_features=["SpaBookingWidget"],
    )
    qual = sdk.qualify_and_plan_pages(session_id="test-hotel-v3")
    assert qual["archetype_id"] == "hotel_reservation"
    assert qual["pages_count"] >= 2
    assert Path(qual["spec_document_path"]).exists()

    ds = sdk.extract_design_system(session_id="test-hotel-v3")
    assert ds["preset"]["preset_id"] == "hotel_luxury_hospitality"
    assert Path(ds["tokens_css_path"]).exists()

    decomp = sdk.decompose_n1_to_n5(session_id="test-hotel-v3")
    assert decomp["total_required_parts"] >= 10

    hunt = sdk.hunt_parts_3_circles(session_id="test-hotel-v3")
    assert hunt["counts_by_circle"]["CIRCLE_1_INTERNAL_BANK"] >= 4
    assert hunt["counts_by_circle"]["CIRCLE_2_EXTERNAL_MCP_FREE"] >= 2
    assert hunt["ready_parts_reuse_percent"] >= 70.0

    doc = sdk.generate_materialization_doc(session_id="test-hotel-v3")
    assert Path(doc["markdown_report_path"]).exists()

    sdk_target = tmp_path / "hotel_sdk"
    mat = sdk.materialize_frontend_sdk(session_id="test-hotel-v3", target_dir=str(sdk_target))
    assert (sdk_target / "src" / "styles" / "tokens.css").exists()
    assert (sdk_target / "src" / "styles" / "index.css").exists()
    assert (sdk_target / "src" / "presentation" / "05-pages" / "index.ts").exists()
    assert len(mat["qualified_pages_materialized"]) >= 2
    assert (sdk_target / "package.json").exists()
    assert (sdk_target / "components.json").exists()
    assert mat["architecture_audit"]["compliant"] is True


def test_zero_maquette_ai_visual_prototyping_bio_atlas():
    sdk = UiDesignerFrontendSdkMcpSdk()
    sdk.init_session(
        session_id="test-bioatlas-nomockup",
        project_name="Bio-Atlas Medical",
        vision_brief="Plateforme de bioinformatique et d'analyse génomique VCF avec visualisation moléculaire 3D.",
    )
    p1 = sdk.generate_phase1_design_prompt(session_id="test-bioatlas-nomockup")
    assert p1["phase"] == "PHASE_1_AI_VISUAL_DESIGN"
    assert p1["screens_count"] == 6
    assert "2×3" in p1["ready_prompt_for_image_generator"]
    assert Path(p1["prompt_file_path"]).exists()

    p2 = sdk.generate_phase2_video_prompt(session_id="test-bioatlas-nomockup", duration_seconds=12)
    assert p2["phase"] == "PHASE_2_AI_VIDEO_PROTOTYPING"
    assert p2["storyboard_slots"] == 6
    assert "00–02 s" in p2["ready_prompt_for_video_generator"]
    assert Path(p2["prompt_file_path"]).exists()


def test_door1_mcp_18_tools_and_inv07_bipartition():
    assert len(TOOLS_METADATA) == 18
    for tool in TOOLS_METADATA:
        assert "PARTIE 1" in tool["description"]
        assert "PARTIE 2" in tool["description"]

    res = handle_tool_call("ui_designer_list_bank_inventory", {})
    assert res["status"] == "SUCCESS"
    assert res["payload"]["summary_counts"]["total_ready_parts_in_bank"] >= 230


def test_door2_cli_execution():
    cli_path = ROOT_DIR / "canal_sdk_cli" / "cli.py"
    proc = subprocess.run(
        [sys.executable, str(cli_path), "--action", "list_bank_inventory"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["status"] == "SUCCESS"


def test_door1_stdio_jsonrpc_subprocess():
    server_path = ROOT_DIR / "canal_mcp" / "mcp_server.py"
    payload = "\n".join([
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}),
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "ui_designer_frontend_sdk_mcp_ping", "arguments": {}}}),
    ]) + "\n"
    proc = subprocess.run(
        [sys.executable, str(server_path)],
        input=payload,
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [json.loads(l) for l in proc.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 3
    assert lines[0]["result"]["serverInfo"]["version"] == "3.0.0"
    assert len(lines[1]["result"]["tools"]) == 18
    ping_data = json.loads(lines[2]["result"]["content"][0]["text"])
    assert ping_data["status"] == "HEALTHY"
