from pathlib import Path


def test_judge_recording_mode_contract():
    html = Path("web/demo.html").read_text(encoding="utf-8")
    js = Path("web/demo.js").read_text(encoding="utf-8")

    required_html = [
        "Pika needs dinner tonight.",
        "Find someone I trust",
        "Owner Approval Required",
        "CARE COMPLETE",
        "Reset Demo",
        "Live AgentCore",
        "Agent trace",
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
