/**
 * CSVリストを取得し、セレクトボックスを更新する
 */
async function fetchCSVList() {
  try {
    const response = await fetch("/api/get_csv_list");
    const data = await response.json();
    populateSelectOptions(data, "csvSelect");
    populateSelectOptions(data, "viewCsvSelect");
  } catch (error) {
    console.error("CSVリストの取得に失敗:", error);
  }
}

/**
 * 認識を開始する
 */
async function startRecognition() {
  let mode = document.getElementById("csvMode").value;
  let filename =
    mode === "existing"
      ? document.getElementById("csvSelect").value
      : document.getElementById("newCsvName").value.trim();

  try {
    await fetch("/api/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename, mode }),
    });
    updateSessionStorage(true, filename);
    window.location.reload();
  } catch (error) {
    console.error("認識開始に失敗:", error);
  }
}

/**
 * 認識を停止する
 */
async function stopRecognition() {
  try {
    await fetch("/api/stop", { method: "POST" });
    updateSessionStorage(false);
    window.location.reload();
  } catch (error) {
    console.error("認識停止に失敗:", error);
  }
}

/**
 * 新しいCSVファイルを作成する
 */
async function createNewCsv() {
  let newCsvName = document.getElementById("newCsvName").value.trim();
  if (!newCsvName) {
    alert("ファイル名を入力してください");
    return;
  }

  try {
    const response = await fetch("/api/create_new_csv", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: newCsvName }),
    });
    const data = await response.json();
    if (data.success) {
      await fetchCSVList();
      document.getElementById("csvMode").value = "existing";
      toggleCsvSelection();
    } else {
      alert("CSVの作成に失敗しました");
    }
  } catch (error) {
    console.error("CSV作成エラー:", error);
  }
}

/**
 * 選択したCSVのデータを取得し、表示する
 */
async function loadCSVData() {
  let selectedCsv = document.getElementById("viewCsvSelect").value;

  if (!selectedCsv) {
    alert("CSVファイルを選択してください");
    return;
  }

  initializeEventSource(
    `/api/sse_csv_data?filename=${selectedCsv}`,
    updateCsvTable
  );
}
/**
 * 選択した行を削除する
 */
async function deleteSelectedRows() {
  let filename = document.getElementById("viewCsvSelect").value.trim();
  let selectedRows = Array.from(
    document.querySelectorAll("#csvTableBody input:checked")
  ).map((cb) => JSON.parse(cb.value));

  if (selectedRows.length === 0) {
    alert("削除する行を選択してください。");
    return;
  }

  try {
    const response = await fetch("/api/delete_selected_rows", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: filename, rows: selectedRows }),
    });
    const data = await response.json();
    if (data.success) {
      loadCSVData();
    }
  } catch (error) {
    console.error("行削除エラー:", error);
  }
}
