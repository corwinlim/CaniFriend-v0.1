const API_URL = new URLSearchParams(location.search).get("api") || window.CANIFRIEND_API_URL || "";
const REQUEST = "I can't get home tonight. Make sure Pika gets dinner.";
let planId = "plan-pika-neighbor-a";
let traceVisible = true;

const labels = {
  home: "1 / 5 · Care Need",
  match: "2 / 5 · Smart Match",
  approval: "3 / 5 · Human Approval",
  mission: "4 / 5 · Care Mission",
  complete: "5 / 5 · Proof & Memory",
};

function addTrace(text) {
  const trace = document.getElementById("trace");
  const row = document.createElement("div");
  row.textContent = text;
  trace.appendChild(row);
  trace.scrollTop = trace.scrollHeight;
}

function showScreen(name) {
  document.querySelectorAll(".screen").forEach(el => el.classList.toggle("active", el.dataset.screen === name));
  document.getElementById("stepLabel").textContent = labels[name];
}

async function callApi(payload) {
  if (!API_URL) return null;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    document.getElementById("liveLabel").textContent = "Live AgentCore";
    return await response.json();
  } catch (error) {
    document.getElementById("liveLabel").textContent = "Demo fallback";
    addTrace(`Live endpoint unavailable · ${error.name || "error"}`);
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

async function findCare() {
  const request = document.getElementById("request").value.trim() || REQUEST;
  addTrace("Need understood · dinner care tonight");
  addTrace("get_pet_context · pet_id=pika");
  addTrace("find_trusted_carers · authorized + available");
  const result = await callApi({
    action: "agent",
    request_id: `judge-${Date.now()}`,
    pet_id: "pika",
    prompt: `${request} Current canonical pet_id: pika. Propose the safest trusted care handoff; do not approve it.`,
  });
  if (result?.care_plan?.plan_id) planId = result.care_plan.plan_id;
  addTrace("Neighbor A ranked highest · high familiarity · 8 tasks");
  addTrace("create_care_plan · PROPOSED · owner approval required");
  showScreen("match");
}

async function approveCare() {
  addTrace("HUMAN GATE · owner explicitly approved");
  await callApi({action: "approve", plan_id: planId, owner_id: "owner-corwin", approved: true});
  addTrace("Policy transition · PROPOSED → APPROVED");
  await callApi({action: "accept", plan_id: planId, carer_id: "neighbor-a"});
  addTrace("Neighbor A accepted care mission");
  showScreen("mission");
}

async function completeCare() {
  ["feed", "water", "condition"].forEach(id => document.getElementById(id).checked = true);
  addTrace("Physical care completed by Neighbor A");
  await callApi({
    action: "complete",
    plan_id: planId,
    proof: "photo://pika-dinner",
    observation: "Pika looks normal",
  });
  showScreen("complete");
  await recordOutcome();
}

async function recordOutcome() {
  addTrace("Proof validated · fed + water + condition normal");
  await callApi({
    action: "record_outcome",
    pet_id: "pika",
    plan_id: planId,
    outcome: "fed, water refreshed, condition normal",
  });
  document.getElementById("recordState").textContent = "Recorded ✓";
  addTrace("CAIOS CareEvent recorded · authoritative outcome");
}

function resetDemo() {
  planId = "plan-pika-neighbor-a";
  document.getElementById("request").value = REQUEST;
  ["feed", "water", "condition"].forEach(id => document.getElementById(id).checked = false);
  document.getElementById("recordState").textContent = "Recording…";
  document.getElementById("trace").innerHTML = "<div>Ready · waiting for owner request</div>";
  document.getElementById("liveLabel").textContent = API_URL ? "Live AgentCore" : "Recording Mode";
  showScreen("home");
}

function toggleTrace() {
  const trace = document.getElementById("trace");
  traceVisible = !traceVisible;
  trace.style.display = traceVisible ? "block" : "none";
}

window.findCare = findCare;
window.approveCare = approveCare;
window.completeCare = completeCare;
window.recordOutcome = recordOutcome;
window.resetDemo = resetDemo;
window.toggleTrace = toggleTrace;
window.showScreen = showScreen;
resetDemo();
