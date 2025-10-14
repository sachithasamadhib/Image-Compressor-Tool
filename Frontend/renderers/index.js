const { jsPDF } = window.jspdf;
const Chart = window.Chart;
const html2canvas = window.html2canvas;

const imageInput = document.getElementById("imageInput");
const compressBtn = document.getElementById("compressBtn");
const progressDiv = document.getElementById("progress");
const progressBar = document.getElementById("progressBar");
const resultsDiv = document.getElementById("results");
const historyTable = document.getElementById("historyTable").querySelector("tbody");
const previewDiv = document.getElementById("preview");
const originalImg = document.getElementById("originalImg");
const compressedImg = document.getElementById("compressedImg");
const themeToggle = document.getElementById("themeToggle");
const sidebarItems = document.querySelectorAll('.sidebar nav li');
const uploadSection = document.getElementById('uploadSection');
const historySection = document.getElementById('historySection');
const settingsSection = document.getElementById('settingsSection');

let history = [];
let historyChart = null;

sidebarItems.forEach(item => {
  item.addEventListener('click', () => {
    sidebarItems.forEach(i => i.classList.remove('active'));
    item.classList.add('active');

    uploadSection.classList.add('hidden');
    historySection.classList.add('hidden');
    settingsSection.classList.add('hidden');

    const sectionName = item.querySelector('span').textContent.trim().toLowerCase();
    if (sectionName === 'upload') uploadSection.classList.remove('hidden');
    if (sectionName === 'history') historySection.classList.remove('hidden');
    if (sectionName === 'settings') settingsSection.classList.remove('hidden');
  });
});


function animateSection(sectionId) {
  const el = document.getElementById(sectionId);
  if (el) {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    setTimeout(() => {
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    }, 50);
  }
}

// Theme toggle

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");

  if (document.body.classList.contains("dark")) {
    themeToggle.textContent = "☀️ Light Mode";
    localStorage.setItem("theme", "dark");
  } else {
    themeToggle.textContent = "🌙 Dark Mode";
    localStorage.setItem("theme", "light");
  }

  console.log("Theme toggled. Current classes:", document.body.className);
  console.log("bg-color:", getComputedStyle(document.body).getPropertyValue("--bg-color"));
});

compressBtn.addEventListener("click", async () => {
  if (!imageInput.files.length) {
    alert("Please select at least one image!");
    return;
  }

  const fileNames = [...imageInput.files].map(f => f.name).join(", ");
  const formData = new FormData();
  for (let file of imageInput.files) {
    formData.append("images", file);
  }

  progressDiv.classList.remove("hidden");
  animateSection("progress");
  progressBar.value = 20;

  const result = await window.api.compressImage(formData);

  progressBar.value = 100;

  if (result.error) {
    resultsDiv.innerHTML = `<p style="color:red;">Error: ${result.error}</p>`;
    resultsDiv.classList.remove("hidden"); // show error message
    previewDiv.classList.add("hidden");
  } else {
    resultsDiv.innerHTML = `
      <h3>Compression Results</h3>
      <p>Original Size: ${result.original_size} KB</p>
      <p>Compressed Size: ${result.compressed_size} KB</p>
      <p>Ratio: ${result.ratio}%</p>
      <p>Processing Time: ${result.time}s</p>
    `;
    resultsDiv.classList.remove("hidden");
    animateSection("results");

    // Show previews
    const originalFile = imageInput.files[0];
    originalImg.src = URL.createObjectURL(originalFile);
    compressedImg.src = "data:image/png;base64," + result.compressed_preview;
    previewDiv.classList.remove("hidden");
    animateSection("preview");

    // Save to history
    const entry = {
      files: fileNames,
      original_size: result.original_size,
      compressed_size: result.compressed_size,
      ratio: result.ratio,
      time: result.time
    };
    history.push(entry);
    updateHistoryTable();
    animateSection("history");
  }
});

const resetBtn = document.getElementById("resetBtn");

resetBtn.addEventListener("click", () => {
  // Hide progress, results, and preview
  progressDiv.classList.add("hidden");
  resultsDiv.classList.add("hidden");
  previewDiv.classList.add("hidden");

  // Clear contents
  resultsDiv.innerHTML = "";
  originalImg.src = "";
  compressedImg.src = "";

  // Reset file input
  imageInput.value = "";

  // Reset progress bar
  progressBar.value = 0;
});





function updateHistoryTable() {
  let html = `
    <thead>
      <tr>
        <th>File(s)</th>
        <th>Original (KB)</th>
        <th>Compressed (KB)</th>
        <th>Ratio (%)</th>
        <th>Time (s)</th>
      </tr>
    </thead>
    <tbody>
  `;

  for (let entry of history) {
    html += `
      <tr>
        <td>${entry.files}</td>
        <td>${entry.original_size}</td>
        <td>${entry.compressed_size}</td>
        <td>${entry.ratio}</td>
        <td>${entry.time}</td>
      </tr>
    `;
  }

  html += `</tbody>`;
  historyTable.innerHTML = html;

  // Update chart
  updateHistoryChart();
}

function updateHistoryChart() {
  const labels = history.map((h, i) => `Run ${i + 1}`);
  const ratios = history.map(h => h.ratio);
  const originalSizes = history.map(h => h.original_size);
  const compressedSizes = history.map(h => h.compressed_size);

  if (historyChart) {
    historyChart.destroy();
  }

  const ctx = document.getElementById("historyChart").getContext("2d");

  historyChart = new Chart(ctx, {
    data: {
      labels: labels,
      datasets: [
        {
          type: "line",
          label: "Compression Ratio (%)",
          data: ratios,
          borderColor: "rgba(52, 152, 219, 1)",
          backgroundColor: "rgba(52, 152, 219, 0.2)",
          yAxisID: "y1",
          tension: 0.3,
          pointRadius: 5,
          pointHoverRadius: 7,
          fill: true
        },
        {
          type: "bar",
          label: "Original Size (KB)",
          data: originalSizes,
          backgroundColor: "rgba(231, 76, 60, 0.7)",
          borderColor: "rgba(231, 76, 60, 1)",
          borderWidth: 1,
          yAxisID: "y"
        },
        {
          type: "bar",
          label: "Compressed Size (KB)",
          data: compressedSizes,
          backgroundColor: "rgba(46, 204, 113, 0.7)",
          borderColor: "rgba(46, 204, 113, 1)",
          borderWidth: 1,
          yAxisID: "y"
        }
      ]
    },
    options: {
      responsive: true,
      interaction: {
        mode: "index",
        intersect: false
      },
      plugins: {
        legend: { position: "top" },
        tooltip: { enabled: true }
      },
      scales: {
        y: {
          type: "linear",
          position: "left",
          title: { display: true, text: "File Size (KB)" }
        },
        y1: {
          type: "linear",
          position: "right",
          title: { display: true, text: "Compression Ratio (%)" },
          grid: { drawOnChartArea: false }
        },
        x: {
          title: { display: true, text: "Compression Runs" }
        }
      }
    }
  });
}

// Download CSV
document.getElementById("downloadCSV").addEventListener("click", () => {
  if (history.length === 0) {
    alert("No history to export!");
    return;
  }

  let csvContent = "File(s),Original Size (KB),Compressed Size (KB),Ratio (%),Time (s)\n";
  history.forEach(row => {
    csvContent += `${row.files},${row.original_size},${row.compressed_size},${row.ratio},${row.time}\n`;
  });

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "compression_history.csv";
  a.click();
  URL.revokeObjectURL(url);
});

// Download PDF (table + chart snapshot)
document.getElementById("downloadPDF").addEventListener("click", async () => {
  if (history.length === 0) {
    alert("No history to export!");
    return;
  }

  const pdf = new jsPDF("p", "mm", "a4");

  // Title
  pdf.setFontSize(18);
  pdf.text("Image Compression Report", 14, 20);

  // Add table text
  let startY = 30;
  pdf.setFontSize(12);
  history.forEach((row, i) => {
    pdf.text(
      `${i + 1}. ${row.files} | Orig: ${row.original_size} KB | Comp: ${row.compressed_size} KB | Ratio: ${row.ratio}% | Time: ${row.time}s`,
      14,
      startY
    );
    startY += 8;
  });

  // Add chart snapshot
  const chartCanvas = document.getElementById("historyChart");
  const chartImage = await html2canvas(chartCanvas);
  const chartData = chartImage.toDataURL("image/png");
  pdf.addImage(chartData, "PNG", 14, startY + 10, 180, 100);

  // Save PDF
  pdf.save("compression_report.pdf");
});

document.addEventListener("DOMContentLoaded", () => {
  lucide.createIcons(); // replaces all <i data-lucide="...">
});
