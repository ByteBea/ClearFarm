const backend = "http://localhost:8000";

async function plantPlot() {
  const species = document.getElementById("species").value;
  const organic = document.getElementById("organic").checked;
  const tokenUri = document.getElementById("tokenUri").value;

  try {
    const res = await fetch(`${backend}/plant_plot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ species, organic_cert: organic, token_uri: tokenUri })
    });
    const data = await res.json();
    document.getElementById("result").textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    document.getElementById("result").textContent = err;
  }
}

async function waterPlot() {
  const plot_id = parseInt(document.getElementById("waterPlotId").value);
  const amount = parseInt(document.getElementById("amount").value);

  try {
    const res = await fetch(`${backend}/water_plot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plot_id, amount })
    });
    const data = await res.json();
    document.getElementById("result").textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    document.getElementById("result").textContent = err;
  }
}

async function getPlot() {
  const plot_id = parseInt(document.getElementById("getPlotId").value);

  try {
    const res = await fetch(`${backend}/get_plot/${plot_id}`);
    const data = await res.json();
    document.getElementById("result").textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    document.getElementById("result").textContent = err;
  }
}
