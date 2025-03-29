/**
 * セレクトボックスにオプションを追加する
 */
function populateSelectOptions(data, elementId) {
  let select = document.getElementById(elementId);
  select.innerHTML = "";
  data.forEach((csv) => {
    let option = document.createElement("option");
    option.value = csv;
    option.textContent = csv;
    select.appendChild(option);
  });
}

/**
 * CSVの選択UIを切り替える
 */
function toggleCsvSelection() {
  let mode = document.getElementById("csvMode").value;
  document.getElementById("existingCsvSection").style.display =
    mode === "existing" ? "block" : "none";
  document.getElementById("newCsvSection").style.display =
    mode === "new" ? "block" : "none";
}

/**
 * CSVデータのテーブルを更新する
 */
function updateCsvTable(data) {
  let tableBody = document.getElementById("csvTableBody");
  tableBody.innerHTML = "";

  if (data.length === 0) {
    tableBody.innerHTML =
      "<tr><td colspan='7' class='text-center text-lg'>データなし</td></tr>";
    return;
  }

  data.slice(1).forEach((row, index) => {
    let tr = document.createElement("tr");

    // チェックボックス列
    let tdCheckbox = document.createElement("td");
    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = JSON.stringify(row);
    tdCheckbox.appendChild(checkbox);
    tdCheckbox.classList.add("text-center", "text-lg"); // 文字を大きくする
    tr.appendChild(tdCheckbox);

    // 各データ列
    row.forEach((cell) => {
      let td = document.createElement("td");
      td.textContent = cell;
      td.classList.add("text-center", "text-lg"); // 文字を大きくする
      tr.appendChild(td);
    });

    // 行の交互背景色
    if (index % 2 === 0) {
      tr.classList.add("bg-gray-100"); // 偶数行の背景色
    } else {
      tr.classList.add("bg-white"); // 奇数行の背景色
    }

    tableBody.appendChild(tr);
  });
}

/**
 * CSV選択セクションの表示を更新する
 */
function updateCsvSelection() {
  const csvModeSection = document.getElementById("csvModeSection");
  const recordedCsvSection = document.getElementById("recordedCsvSection");
  const recordedCsvNameSpan = document.getElementById("recordedCsvName");

  const isRecording = sessionStorage.getItem("isRecording") === "true";
  const currentCsvName = sessionStorage.getItem("currentCsvName");

  if (isRecording) {
    csvModeSection.style.display = "none";
    recordedCsvSection.style.display = "block";
    recordedCsvNameSpan.innerHTML = currentCsvName;
  } else {
    csvModeSection.style.display = "block";
    recordedCsvSection.style.display = "none";
    recordedCsvNameSpan.innerHTML = "";
  }
}

/**
 * ボタンの表示テキストを監視状態に応じて更新する
 */
function updateRecognitionButton() {
  const toggleRecognitionBtn = document.getElementById("toggleRecognitionBtn");
  const isRecording = sessionStorage.getItem("isRecording") === "true";

  if (isRecording) {
    toggleRecognitionBtn.textContent = "監視停止";
    toggleRecognitionBtn.classList.remove("bg-green-500", "hover:bg-green-600");
    toggleRecognitionBtn.classList.add("bg-red-500", "hover:bg-red-600");
  } else {
    toggleRecognitionBtn.textContent = "監視開始";
    toggleRecognitionBtn.classList.remove("bg-red-500", "hover:bg-red-600");
    toggleRecognitionBtn.classList.add("bg-green-500", "hover:bg-green-600");
  }
}

/**
 * 監視の開始/停止を切り替える
 */
function toggleRecognition() {
  const isRecording = sessionStorage.getItem("isRecording") === "true";

  if (isRecording) {
    stopRecognition();
  } else {
    startRecognition();
  }
}

/**
 * タブの切り替えを行う
 */
function switchTab(tabId) {
  const tabButtons = document.querySelectorAll(".tab-buttons button"); // 親要素 .tab-buttons 内のボタンのみを選択
  const defaultClass = ["inline-block", "p-4", "border-b-2", "rounded-t-lg"];
  const inactiveClass = [
    "text-gray-700",
    "border-transparent",
    "hover:text-gray-600",
    "hover:border-gray-300",
    "dark:hover:text-gray-300",
  ];
  const activeClass = [
    "text-blue-600",
    "border-blue-600",
    "active",
    "dark:text-blue-500",
    "dark:border-blue-500",
  ];

  // すべてのボタンにデフォルトクラスと非アクティブクラスを適用
  tabButtons.forEach((button) => {
    button.classList.remove(...button.classList);
    button.classList.add(...defaultClass, ...inactiveClass);
  });

  // クリックされたタブにアクティブクラスを追加
  const activeButton = Array.from(tabButtons).find(
    (button) => button.id === `${tabId}Btn`
  );
  if (activeButton) {
    activeButton.classList.remove(...inactiveClass); // 非アクティブクラスを削除
    activeButton.classList.add(...activeClass); // アクティブクラスを追加
  }

  // すべてのタブコンテンツを非表示に
  const tabs = document.querySelectorAll(".tab-content");
  tabs.forEach((tab) => tab.classList.add("hidden"));

  // 指定されたタブを表示
  document.getElementById(tabId).classList.remove("hidden");
}
