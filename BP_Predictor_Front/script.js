const BASE_URL = "http://127.0.0.1:5000";

// Predict Blood Pressure
document.getElementById("predict-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const workday = document.getElementById("workday").value;
  const stress_levels = document.getElementById("stress_levels").value;
  const sleep_quality = document.getElementById("sleep_quality").value;
  const tiredness = document.getElementById("tiredness").value;

  try {
    const response = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ workday, stress_levels, sleep_quality, tiredness }),
    });

    const result = await response.json();
    document.getElementById("result").style.display = "block";
    document.getElementById("result").innerText = `Predicted Upper BP: ${result.Upper_BP.toFixed(2)}, Predicted Lower BP: ${result.Lower_BP.toFixed(2)}`;
  } catch (error) {
    document.getElementById("result").style.display = "block";
    document.getElementById("result").innerText = `Error: ${error.message}`;
  }
});

// Add New Data
document.getElementById("add-data-form").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const upperBP = parseInt(document.getElementById("add-upper-bp").value, 10);
    const lowerBP = parseInt(document.getElementById("add-lower-bp").value, 10);
    const workday = parseInt(document.getElementById("add-workday").value, 10);
    const stress_levels = parseInt(document.getElementById("add-stress").value, 10);
    const sleep_quality = parseInt(document.getElementById("add-sleep").value, 10);
    const tiredness = parseInt(document.getElementById("add-tiredness").value, 10);
  
    console.log("Data to submit:", { workday, stress_levels, upperBP, lowerBP, sleep_quality, tiredness });
  
    const newData = [
      { Workday: workday, Stress_Levels: stress_levels, Upper_BP: upperBP, Lower_BP: lowerBP, Sleep_Quality: sleep_quality, Tiredness: tiredness },
    ];
  
    try {
      const response = await fetch(`${BASE_URL}/add_data`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newData),
      });
  
      const result = await response.json();
      document.getElementById("result").style.display = "block";
      document.getElementById("result").innerText = result.message || result.error;
    } catch (error) {
      document.getElementById("result").style.display = "block";
      document.getElementById("result").innerText = `Error: ${error.message}`;
    }
  });

  // Retrain Model
  document.getElementById("retrain-button").addEventListener("click", async function (e) {
    e.preventDefault();
  
    try {
      const response = await fetch(`${BASE_URL}/retrain`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      const result = await response.json();
      document.getElementById("result").style.display = "block";
      document.getElementById("result").innerText = result.message || result.error;
    } catch (error) {
      document.getElementById("result").style.display = "block";
      document.getElementById("result").innerText = `Error: ${error.message}`;
    }
  });