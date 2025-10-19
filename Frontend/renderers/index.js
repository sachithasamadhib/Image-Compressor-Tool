const { jsPDF } = window.jspdf;
const Chart = window.Chart;
const html2canvas = window.html2canvas;

const imageInput = document.getElementById("imageInput");
const compressBtn = document.getElementById("compressBtn");
const progressDiv = document.getElementById("progress");
const progressBar = document.getElementById("progressBar");
const resultsDiv = document.getElementById("results");
const historyTable = document.getElementById("historyTable");
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

  const quality = document.getElementById('quality').value;
  const aspectRatio = document.getElementById('aspect').value;
  const maxSize = 5000000; // 5MB default max size

  const formData = new FormData();
  for (let file of imageInput.files) {
    formData.append("images", file);
  }

  progressDiv.classList.remove("hidden");
  animateSection("progress");
  progressBar.value = 20;

  const result = await window.api.compressImage(formData, quality, maxSize, aspectRatio);

  progressBar.value = 100;

  if (result.error) {
    resultsDiv.innerHTML = `<p style="color:red;">Error: ${result.error}</p>`;
    resultsDiv.classList.remove("hidden");
    previewDiv.classList.add("hidden");
  } else {
    let totalOriginal = 0;
    let totalCompressed = 0;
    let resultsHtml = '<h3>Compression Results</h3>';
    
    result.processed_files.forEach((file, index) => {
      if (file.error) {
        resultsHtml += `<p style="color:red;">${file.filename}: ${file.error}</p>`;
      } else {
        totalOriginal += file.original_size;
        totalCompressed += file.compressed_size;
        resultsHtml += `
          <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
            <strong>${file.filename}</strong><br>
            Original: ${formatFileSize(file.original_size)} (${file.original_dimensions[0]}×${file.original_dimensions[1]})<br>
            Compressed: ${formatFileSize(file.compressed_size)} (${file.final_dimensions[0]}×${file.final_dimensions[1]})<br>
            Compression: ${file.compression_ratio}%<br>
            Quality: ${quality} | Aspect: ${aspectRatio}
          </div>
        `;
      }
    });

    resultsHtml += `
      <div style="margin-top: 15px; padding: 10px; background: #f0f0f0; border-radius: 5px;">
        <strong>Total:</strong> ${formatFileSize(totalOriginal)} → ${formatFileSize(totalCompressed)} 
        (${((1 - totalCompressed / totalOriginal) * 100).toFixed(2)}% reduction)
      </div>
    `;

    resultsDiv.innerHTML = resultsHtml;
    resultsDiv.classList.remove("hidden");
    animateSection("results");

    // Show preview of first image
    if (result.processed_files.length > 0 && result.processed_files[0].compressed_data) {
      const originalFile = imageInput.files[0];
      originalImg.src = URL.createObjectURL(originalFile);
      compressedImg.src = "data:image/jpeg;base64," + result.processed_files[0].compressed_data;
      previewDiv.classList.remove("hidden");
      animateSection("preview");
    }

    // Refresh history from backend
    await loadHistoryFromBackend();
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





async function loadHistoryFromBackend() {
  try {
    const response = await window.api.getHistory();
    if (response.error) {
      console.error('Error loading history:', response.error);
      return;
    }
    history = response.history;
    updateHistoryTable();
  } catch (error) {
    console.error('Error loading history:', error);
  }
}

function updateHistoryTable() {
  let html = `
    <div style="margin-bottom: 10px;">
      <button id="sortByDate" style="margin-right: 5px;">Sort by Date</button>
      <button id="sortBySize" style="margin-right: 5px;">Sort by Size</button>
      <button id="sortByRatio" style="margin-right: 5px;">Sort by Ratio</button>
      <button id="clearHistory" style="margin-left: 10px; background: #e74c3c; color: white;">Clear History</button>
    </div>
    <thead>
      <tr>
        <th>Filename</th>
        <th>Date</th>
        <th>Original Size</th>
        <th>Compressed Size</th>
        <th>Compression %</th>
        <th>Quality</th>
        <th>Aspect Ratio</th>
      </tr>
    </thead>
    <tbody>
  `;

  for (let entry of history) {
    html += `
      <tr>
        <td>${entry.filename}</td>
        <td>${new Date(entry.timestamp).toLocaleString()}</td>
        <td>${formatFileSize(entry.original_size)}</td>
        <td>${formatFileSize(entry.compressed_size)}</td>
        <td>${entry.compression_ratio}%</td>
        <td>${entry.quality}</td>
        <td>${entry.aspect_ratio}</td>
      </tr>
    `;
  }

  html += `</tbody>`;
  historyTable.innerHTML = html;

  // Add event listeners for sorting buttons
  document.getElementById('sortByDate')?.addEventListener('click', () => sortHistory('date'));
  document.getElementById('sortBySize')?.addEventListener('click', () => sortHistory('size'));
  document.getElementById('sortByRatio')?.addEventListener('click', () => sortHistory('compression_ratio'));
  document.getElementById('clearHistory')?.addEventListener('click', clearHistoryConfirm);

  // Update chart
  updateHistoryChart();
}

async function sortHistory(sortBy) {
  try {
    const response = await window.api.getHistory(sortBy, 'desc');
    if (response.error) {
      console.error('Error sorting history:', response.error);
      return;
    }
    history = response.history;
    updateHistoryTable();
  } catch (error) {
    console.error('Error sorting history:', error);
  }
}

async function clearHistoryConfirm() {
  if (confirm('Are you sure you want to clear all compression history? This action cannot be undone.')) {
    try {
      const response = await window.api.clearHistory();
      if (response.error) {
        alert('Error clearing history: ' + response.error);
        return;
      }
      history = [];
      updateHistoryTable();
      alert('History cleared successfully!');
    } catch (error) {
      alert('Error clearing history: ' + error.message);
    }
  }
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
}

function updateHistoryChart() {
  if (history.length === 0) {
    if (historyChart) {
      historyChart.destroy();
      historyChart = null;
    }
    return;
  }

  const labels = history.map((h, i) => h.filename || `File ${i + 1}`);
  const ratios = history.map(h => h.compression_ratio);
  const originalSizes = history.map(h => h.original_size / 1024); // Convert to KB
  const compressedSizes = history.map(h => h.compressed_size / 1024); // Convert to KB

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

  let csvContent = "Filename,Date,Original Size (bytes),Compressed Size (bytes),Compression Ratio (%),Quality,Aspect Ratio\n";
  history.forEach(row => {
    const date = new Date(row.timestamp).toISOString();
    csvContent += `"${row.filename}","${date}",${row.original_size},${row.compressed_size},${row.compression_ratio},"${row.quality}","${row.aspect_ratio}"\n`;
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
  pdf.text("Image Compression History Report", 14, 20);

  // Add statistics
  try {
    const stats = await window.api.getStatistics();
    if (!stats.error) {
      pdf.setFontSize(12);
      pdf.text(`Total Files Processed: ${stats.total_files}`, 14, 35);
      pdf.text(`Total Original Size: ${formatFileSize(stats.total_original_size)}`, 14, 43);
      pdf.text(`Total Compressed Size: ${formatFileSize(stats.total_compressed_size)}`, 14, 51);
      pdf.text(`Average Compression Ratio: ${stats.average_compression_ratio}%`, 14, 59);
      pdf.text(`Best Compression Ratio: ${stats.best_compression_ratio}%`, 14, 67);
    }
  } catch (error) {
    console.error('Error getting statistics for PDF:', error);
  }

  // Add table text
  let startY = 80;
  pdf.setFontSize(10);
  history.forEach((row, i) => {
    const date = new Date(row.timestamp).toLocaleDateString();
    const text = `${i + 1}. ${row.filename} | ${date} | Orig: ${formatFileSize(row.original_size)} | Comp: ${formatFileSize(row.compressed_size)} | Ratio: ${row.compression_ratio}% | Quality: ${row.quality}`;
    
    // Handle text wrapping
    const lines = pdf.splitTextToSize(text, 180);
    pdf.text(lines, 14, startY);
    startY += lines.length * 5;
    
    if (startY > 250) { // Add new page if needed
      pdf.addPage();
      startY = 20;
    }
  });

  // Add chart snapshot if there's space or on a new page
  if (startY > 200) {
    pdf.addPage();
    startY = 20;
  }
  
  try {
    const chartCanvas = document.getElementById("historyChart");
    if (chartCanvas) {
      const chartImage = await html2canvas(chartCanvas);
      const chartData = chartImage.toDataURL("image/png");
      pdf.addImage(chartData, "PNG", 14, startY + 10, 180, 100);
    }
  } catch (error) {
    console.error('Error adding chart to PDF:', error);
  }

  // Save PDF
  pdf.save("compression_history_report.pdf");
});

document.addEventListener("DOMContentLoaded", () => {
  lucide.createIcons(); // replaces all <i data-lucide="...">
  
  // Load history from backend when page loads
  loadHistoryFromBackend();
  
  // Load theme preference
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark");
    themeToggle.textContent = "☀️ Light Mode";
  }
});
