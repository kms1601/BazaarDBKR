let currentLang = "en/kr";

// 초기 설정 가져오기
chrome.storage.sync.get("selectedOption", (data) => {
    currentLang = data.selectedOption || "en/kr";

    // 기존 DOM 처리
    document.querySelectorAll("._an").forEach(addTitleKR);
});

function addTitleKR(item) {
    // 이미 추가했으면 스킵
    if (item.querySelector(".kr")) return;

    const key = item.children[0]?.textContent?.trim();
    const titleKRText = DATA[key];

    if (!titleKRText) return; // DATA에 키가 없으면 종료

    if (currentLang === "en") {
        Array.from(item.children).forEach(child => {
            child.style.color = "";
            child.style.fontSize = "";
            child.style.display = "";
        });
    } else if (currentLang === "kr") {
        Array.from(item.children).forEach(child => {
            child.style.color = "";
            child.style.fontSize = "";
            child.style.display = "none";
        });

        const titleKR = document.createElement("span");
        titleKR.textContent = titleKRText;
        titleKR.className = "kr"; // 중복 방지용 클래스

        item.appendChild(titleKR);
    } else if (currentLang === "en/kr") {
        Array.from(item.children).forEach(child => {
            child.style.color = "";
            child.style.fontSize = "";
            child.style.display = "";
        });

        const titleKR = document.createElement("span");
        titleKR.textContent = titleKRText;
        titleKR.style.color = "gray";
        titleKR.style.fontSize = "12px";
        titleKR.className = "kr"; // 중복 방지용 클래스

        item.appendChild(titleKR);
    } else if (currentLang === "kr/en") {
        Array.from(item.children).forEach(child => {
            child.style.color = "gray";
            child.style.fontSize = "12px";
            child.style.display = "";
        });

        const titleKR = document.createElement("span");
        titleKR.textContent = titleKRText;
        titleKR.className = "kr"; // 중복 방지용 클래스


        item.prepend(titleKR);
    }
}

// MutationObserver로 이후 동적 생성되는 요소도 처리
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType !== 1) return; // element만 처리
            if (node.matches("._an")) {
                addTitleKR(node);
            }
            // node 안쪽에 _an 요소가 있는 경우
            node.querySelectorAll("._an").forEach(addTitleKR);
        });
    });
});
// body 전체 감시 (서브트리 포함)
observer.observe(document.body, {childList: true, subtree: true});

// chrome.storage 변경 감지
chrome.storage.onChanged.addListener((changes, area) => {
    if (area === "sync" && changes.selectedOption) {
        currentLang = changes.selectedOption.newValue;

        // 기존 .kr 제거 후 재적용
        document.querySelectorAll("._an .kr").forEach(span => span.remove());
        document.querySelectorAll("._an").forEach(addTitleKR);
    }
});
