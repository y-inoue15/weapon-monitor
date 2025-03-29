let eventSource = null;
let lastData = null;

/**
 * 汎用的な SSE（Server-Sent Events）の接続を行う
 * @param {string} endpoint - APIのエンドポイント（例: `/api/sse_csv_data?filename=xxx.csv`）
 * @param {function} onDataReceived - データ受信時のコールバック関数
 */
function initializeEventSource(endpoint, onDataReceived) {
  if (!endpoint) {
    console.error("エンドポイントが指定されていません。");
    return;
  }

  // 既存の EventSource があれば閉じる
  if (eventSource) {
    eventSource.close();
  }

  eventSource = new EventSource(endpoint);

  eventSource.onmessage = function (event) {
    const data = JSON.parse(event.data);

    // データが前回と同じなら更新しない
    if (JSON.stringify(data) === JSON.stringify(lastData)) {
      return;
    }

    lastData = data;
    onDataReceived(data); // コールバック関数を実行
  };

  eventSource.onerror = function (error) {
    console.error("SSE Error:", error);
    eventSource.close();
  };
}
