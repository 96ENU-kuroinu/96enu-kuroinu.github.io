/**
 * data-img属性に基づいてすべてのspan要素のテキスト内容を更新する関数
 */
function updateSpanText() {
    // Select all span elements with the class 'hover-text'
    const spanElements = document.querySelectorAll('.hover-text');

    // Loop through each span element and update its text content
    spanElements.forEach(spanElement => {
        // Get the data-img attribute value for the current span element
        const dataImage = spanElement.getAttribute('data-img');

        // Conditional logic to change text based on the data-img value
        let newText = '';
        switch (dataImage) {
            // BaconJam
            case '../imgs/bj/display-server-select.png':
                newText = 'Misskeyサーバー選択画面';
                break;
            case '../imgs/bj/display-setting.png':
                newText = '設定画面';
                break;
            case '../imgs/bj/display-playlist-detail.png':
                newText = 'プレイリスト詳細画面';
                break;
            case '../imgs/bj/display-playlists-2.png':
                newText = 'プレイリスト一覧画面';
                break;
            case '../imgs/bj/display-playlists-1.png':
                newText = 'プレイリスト一覧画面';
                break;
            case '../imgs/bj/display-main.png':
                newText = 'ホーム画面';
                break;
            case '../imgs/bj/display-drawer.png':
                newText = 'ドロワー';
                break;
            case '../imgs/bj/display-channel-select-2.png':
                newText = '投稿先チャンネル検索画面';
                break;
            case '../imgs/bj/display-channel-select-1.png':
                newText = '投稿先チャンネル検索画面';
                break;
            case '../imgs/bj/display-app-about.png':
                newText = 'アプリについての画面';
                break;
            case '../imgs/bj/display-sample-mfm.png':
                newText = '作例画面';
                break;
            // TidyDrive
            case '../imgs/td/display-initial.png':
                newText = '初回起動時に表示されるウィンドウ';
                break;
            case '../imgs/td/display-select-server.png':
                newText = 'サーバー一覧画面';
                break;
            case '../imgs/td/display-select-alternative-server.png':
                newText = 'サーバー一覧に掲載されていないサーバーの選択用ウィンドウ';
                break;
            case '../imgs/td/display-setting.png':
            case '../imgs/td/display-setting-no-auth.png':
                newText = '設定画面';
                break;
            case '../imgs/td/display-main.png':
                newText = 'ホーム画面';
                break;
            case '../imgs/td/display-drawer.png':
                newText = 'ドロワー';
                break;
            case '../imgs/td/display-app-about.png':
                newText = 'アプリについての画面';
                break;
            case '../imgs/td/display-tag-manage.png':
                newText = 'タグ管理画面';
                break;
            default:
                newText = '対応する画面名が定義されていません！'
                break;
        }

        // Update the text content of the current span element
        spanElement.textContent = newText;
    });
}

// Call the function to update the span texts on page load
window.onload = updateSpanText;