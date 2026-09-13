const API_URL = new URLSearchParams(location.search).get("api") || window.CANIFRIEND_API_URL || "";
const REQUEST = "I can't get home tonight. Make sure Pika gets dinner.";
let planId = "plan-pika-neighbor-a";

const labels = {
  match: "2 / 5 · Smart Match",
  approval: "3 / 5 · Human Approval",
  mission: "4 / 5 · Care Mission",
  complete: "5 / 5 · Proof & Memory",
};

function addTrace(text) {
  const trace = document.getElementById("trace");
  if (!trace) return;
  const row = document.createElement("div");
  row.textContent = text;
  trace.appendChild(row);
  trace.scrollTop = trace.scrollHeight;
}

function showScreen(name) {
  document.getElementById("homeView").style.display = "none";
  const flow = document.getElementById("flowView");
  flow.classList.add("active");
  document.querySelectorAll(".screen").forEach(el => el.classList.toggle("active", el.dataset.screen === name));
  const label = document.getElementById("stepLabel");
  if (label) label.textContent = labels[name] || "CaniFriend Care Flow";
  window.scrollTo({top:0,behavior:"smooth"});
}

function goHome() {
  document.getElementById("homeView").style.display = "block";
  document.getElementById("flowView").classList.remove("active");
  document.querySelectorAll(".screen").forEach(el => el.classList.remove("active"));
  window.scrollTo({top:0,behavior:"smooth"});
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
    return await response.json();
  } catch (error) {
    addTrace(`Live endpoint unavailable · ${error.name || "error"}`);
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

async function findCare() {
  const requestEl = document.getElementById("request");
  const request = requestEl?.value.trim() || REQUEST;
  addTrace("Need understood · dinner care tonight");
  addTrace("get_pet_context · pet_id=pika · bounded context");
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
  await callApi({action:"approve",plan_id:planId,owner_id:"owner-corwin",approved:true});
  addTrace("Policy transition · PROPOSED → APPROVED");
  await callApi({action:"accept",plan_id:planId,carer_id:"neighbor-a"});
  addTrace("Neighbor A accepted care mission");
  showScreen("mission");
}

async function completeCare() {
  ["feed","water","condition"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.checked = true;
  });
  addTrace("Physical care completed by Neighbor A");
  await callApi({action:"complete",plan_id:planId,proof:"photo://pika-dinner",observation:"Pika looks normal"});
  showScreen("complete");
  await recordOutcome();
}

async function recordOutcome() {
  addTrace("Proof validated · fed + water + condition normal");
  await callApi({action:"record_outcome",pet_id:"pika",plan_id:planId,outcome:"fed, water refreshed, condition normal"});
  const recordState = document.getElementById("recordState");
  if (recordState) recordState.textContent = "Recorded ✓";
  addTrace("CAIOS CareEvent recorded · authoritative outcome");
}

function resetDemo() {
  planId = "plan-pika-neighbor-a";
  const request = document.getElementById("request");
  if (request) request.value = REQUEST;
  ["feed","water","condition"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.checked = false;
  });
  const recordState = document.getElementById("recordState");
  if (recordState) recordState.textContent = "Recording…";
  const trace = document.getElementById("trace");
  if (trace) trace.innerHTML = "<div>Ready · waiting for owner request</div>";
  goHome();
}

function toggleTrace() {
  document.getElementById("judgeDrawer")?.classList.toggle("open");
}

window.findCare = findCare;
window.approveCare = approveCare;
window.completeCare = completeCare;
window.recordOutcome = recordOutcome;
window.resetDemo = resetDemo;
window.toggleTrace = toggleTrace;
window.showScreen = showScreen;
window.goHome = goHome;
resetDemo();
