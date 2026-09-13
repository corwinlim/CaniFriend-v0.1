from pathlib import Path


def test_judge_recording_mode_contract():
    html = Path("web/demo.html").read_text(encoding="utf-8")
    js = Path("web/demo.js").read_text(encoding="utf-8")

    # Judge-visible product and safety contract. Keep this focused on behavior
    # that must remain visible in the current production demo rather than on
    # obsolete labels from earlier recording-mode UI iterations.
    required_html = [
        "Pika needs dinner tonight.",
        "Find someone I trust",
        "Owner Approval Required",
        "CARE COMPLETE",
        "Agent trace",
        "Production runtime proof available",
        "Strands Agents SDK",
        "Amazon Bedrock AgentCore",
    ]
    for text in required_html:
        assert text in html

    required_js = [
        "I can't get home tonight. Make sure Pika gets dinner.",
        'pet_id: "pika"',
        "resetDemo",
        "approveCare",
        "completeCare",
        "recordOutcome",
    ]
    for text in required_js:
        assert text in js
