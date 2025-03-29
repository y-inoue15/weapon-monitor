/**
 * sessionStorageの値を更新する
 */
function updateSessionStorage(isRecording, filename = "") {
  if (isRecording) {
    sessionStorage.setItem("isRecording", "true");
    sessionStorage.setItem("currentCsvName", filename);
  } else {
    sessionStorage.removeItem("isRecording");
    sessionStorage.removeItem("currentCsvName");
  }
}
