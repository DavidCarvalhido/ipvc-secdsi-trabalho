async function loadExecutive() {
    const r = await fetch("/reports/executive")
    const d = await r.json()
    document.getElementById("incidents").innerHTML = d.incidents
    document.getElementById("risk").innerHTML = d.risk
    document.getElementById("compliance").innerHTML = d.compliance
    document.getElementById("evidence").innerHTML = d.evidence
    document.getElementById("audit").innerHTML = d.audit
}


async function loadCompliance() {
    const r = await fetch("/dashboard/compliance")
    const d = await r.json()

    new Chart(
        document.getElementById("complianceChart"), {
        type: "doughnut",
        data: {
            labels: ["Compliant", "Violation"],
            datasets: [{
                data: [d.compliant, d.violations]
            }]
        }
    }
    )
}


async function loadRisk() {
    const r = await fetch("/dashboard/risk-distribution")
    const d = await r.json()

    new Chart(
        document.getElementById("riskChart"), {
        type: "bar",
        data: {
            labels:
                d.map(x => x.risk_level),
            datasets: [{
                data: d.map(x => x.count)
            }
            ]
        }
    }
    )
}


loadExecutive()
loadCompliance()
loadRisk()