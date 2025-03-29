document.addEventListener("DOMContentLoaded", async function () {
  await fetchCSVList();
  updateCsvSelection();
  updateRecognitionButton();
  loadCSVData();
  switchTab("monitoringTab");
});
