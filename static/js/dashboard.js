async function loadSummary() {

    const r =
        await fetch(
            "/dashboard/summary"
        );
    const data = await r.json();
    document.getElementById("events").innerText = data.events;
    document.getElementById("incidents").innerText = data.incidents;
    document.getElementById("risk").innerText = data.risk_assessments;
    document.getElementById("violations").innerText = data.policy_violations;

}


async function loadRisk() {
    const r = await fetch("/dashboard/risk-distribution");
    const data = await r.json();

    new Chart(document.getElementById("riskChart"),
        {
            type: "bar",
            data: {
                labels: data.map(x => x.risk_level),
                datasets: [{ data: data.map(x => x.count) }]
            }
        }
    );
}


async function loadCompliance() {
    const r = await fetch("/dashboard/compliance");
    const data = await r.json();

    new Chart(document.getElementById("complianceChart"),
        {
            type: "doughnut",
            data: {
                labels: ["OK", "Violation"],
                datasets: [{ data: [data.compliant, data.violations] }]
            }
        }
    );
}


async function loadAssets() {
    const r = await fetch("/dashboard/top-assets");
    const data = await r.json();
    const ul = document.getElementById("topAssets");

    data.forEach(
        a => {
            ul.innerHTML += `<li>${a.asset}(${a.incidents})</li>`
        }
    )
}


async function loadIncidentStatus() {
    const r = await fetch("/dashboard/incidents/status");
    const data = await r.json();

    new Chart(document.getElementById("incidentChart"),
        {
            type: "pie",
            data: {
                labels: data.map(x => x.status),
                datasets: [{
                    data: data.map(x => x.count)
                }]
            }
        }
    );
}


async function loadTimeline() {
    const r = await fetch("/dashboard/incidents/timeline")
    const d = await r.json()

    new Chart(
        document.getElementById("timelineChart"),
        {
            type: "line",
            data: {
                labels: d.map(x => x.date),
                datasets: [{
                    data: d.map(x => x.incidents)
                }]
            }
        }
    )
}


async function loadCritical() {
    const r = await fetch("/dashboard/incidents/critical");
    const data = await r.json();

    document.getElementById("critical").innerText = data.active_critical;
}


async function loadMTTR() {
    const r = await fetch("/dashboard/incidents/mttr");
    const data = await r.json();

    document.getElementById("mttr").innerText = data.mttr_hours + " h";
}


async function loadRecent() {
    const r = await fetch("/dashboard/incidents/recent");
    const data = await r.json();
    const table = document.getElementById("recentIncidents");

    data.forEach(
        i => {
            table.innerHTML +=
                `<tr>
                    <td>${i.id}</td>
                    <td>${i.status}</td>
                    <td>${i.risk}</td>
                    <td>${i.assigned}</td>
                </tr>`
        }
    );
}


async function loadCIA() {
    const r = await fetch("/dashboard/cia")
    const d = await r.json()

    document.getElementById("ciaC").innerHTML =d.confidentiality
    document.getElementById("ciaI").innerHTML =d.integrity
    document.getElementById("ciaA").innerHTML =d.availability

    new Chart(
        document.getElementById("ciaChart"),
        {
            type: "radar",
            data: {
                labels: [
                    "Confidentiality",
                    "Integrity",
                    "Availability"
                ],
                datasets: [{
                    data: [
                        d.confidentiality,
                        d.integrity,
                        d.availability
                    ]
                }]
            }
        }
    )
}


async function loadExecutive() {
    const r = await fetch("/reports/executive")
    const d = await r.json()

    document.getElementById("incidents").innerHTML = d.incidents
    document.getElementById("risk").innerHTML = d.risk
    document.getElementById("compliance").innerHTML = d.compliance
    document.getElementById("evidence").innerHTML = d.evidence
}


loadSummary()
loadRisk()
loadCompliance()
loadAssets()

loadIncidentStatus()
loadTimeline()
loadCritical()
loadMTTR()
loadRecent()
loadCIA()
loadExecutive()