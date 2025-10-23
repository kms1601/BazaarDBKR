let currentLang = "en/kr";
let show = [];

const PROCESSED_ATTR = "bazaardbkr-processed";
const CARD = "._aj";
const DETAIL = "._aH"

// 표시 인덱스 설정
function showIndex() {
    const map = {
        "en": [0],
        "kr": [1],
        "en/kr": [0, 3],
        "kr/en": [1, 2],
    };
    show = map[currentLang] || [0, 3];
}

function getTypeFromCard(card) {
    if (card.querySelector("._aB")) return "Skill";
    else if (card.querySelectorAll("._b").length === 3) return "CombatEncounter";
    else if ([1, 2].includes(card.querySelectorAll("._bi").length) && card.querySelector("._aF")) return "EventEncounter";
    else if (card.querySelector("._aC")) return "EncounterStep";
    else return "Item";
}

function getTypeFromDetail(card) {
    if (card.querySelectorAll("h2")[1]?.textContent === "Monster InfoInferred") return "CombatEncounter";
    else if (card.querySelector("._aF")) return "EventEncounter";
    else if (card.querySelector("._aB")) return "Skill";
    else return "Item";
}

function safeText(node) {
    return node?.textContent?.trim() || "";
}

/* ---------- 공통 제목 처리 ---------- */
function setTitle(title, html, size) {
    title.innerHTML = html.replaceAll("__FONT_SIZE__", size);
    title.setAttribute(PROCESSED_ATTR, "1"); // 처리 완료 표시
    setVisible(title);
}

/* ---------- 카드 처리 ---------- */
function handleCard(card) {
    let title = card.querySelector("._an");
    if (!title) title = card.querySelector("h3 span");
    if (!title) return;

    // 원본 텍스트 저장
    let originalText = title.getAttribute("data-original-text");
    if (!originalText) {
        originalText = safeText(title);
        title.setAttribute("data-original-text", originalText);
    }

    const key = `${originalText}_${getTypeFromCard(card)}`;
    const data = DATA[key];
    if (!data) return;

    // 이미 처리된 경우는 setVisible만 수행
    if (title.hasAttribute(PROCESSED_ATTR)) {
        setVisible(title);
    } else {
        setTitle(title, data.title, "12px");
        title.setAttribute(PROCESSED_ATTR, "1");
    }
}

function handleDetailCard(card, data) {
    const cardTitle = card.querySelector("span");
    setTitle(cardTitle, data.title, "12px");
}

function handleDetail(detail) {
    const title = detail.querySelector("h1");
    if (!title) return;

    // 원본 텍스트 저장 및 불러오기
    let originalText = title.getAttribute("data-original-text");
    if (!originalText) {
        originalText = safeText(title);
        title.setAttribute("data-original-text", originalText);
    }

    const key = `${originalText}_${getTypeFromDetail(detail)}`;
    const data = DATA[key];
    if (!data) return;

    // 이미 처리된 경우 → setVisible만
    if (title.hasAttribute(PROCESSED_ATTR)) {
        setVisible(title);
    } else {
        setTitle(title, data.title, "20px");
        title.setAttribute(PROCESSED_ATTR, "1");
    }

    // 세부 카드 처리
    const card = detail.querySelector("._d");
    if (card) {
        handleDetailCard(card, data);
    }
}


/* ---------- 표시 토글 ---------- */
function setVisible(item) {
    Array.from(item.children).forEach((child, i) => {
        child.style.display = show.includes(i) ? "block" : "none";
    });
}

/* ---------- 전체 처리 ---------- */
function processAllOnce() {
    document.querySelectorAll(CARD).forEach(handleCard);
    document.querySelectorAll(DETAIL).forEach(handleDetail);
}

/* ---------- Mutation Observer ---------- */
const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
        // 새로 추가된 노드 처리
        mutation.addedNodes?.forEach((node) => {
            if (node.nodeType !== 1) return;
            node.querySelectorAll?.(CARD).forEach(handleCard);
            node.querySelectorAll?.(DETAIL).forEach(handleDetail);
        });
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true,
});

/* ---------- Storage 변경 감지 ---------- */
chrome.storage.sync.get("selectedOption", (data) => {
    currentLang = data.selectedOption || "en/kr";
    showIndex();
    processAllOnce();
});

chrome.storage.onChanged.addListener((changes, area) => {
    if (area === "sync" && changes.selectedOption) {
        currentLang = changes.selectedOption.newValue;
        showIndex();

        document.querySelectorAll(CARD).forEach(handleCard);
        document.querySelectorAll(DETAIL).forEach(handleDetail);
    }
});

/* ---------- SPA 이동 감지 ---------- */
function reprocessAfterNavigation() {
    setTimeout(processAllOnce, 50);
}

window.addEventListener("popstate", reprocessAfterNavigation);

(function (history) {
    const wrap = (method) =>
        function (...args) {
            const ret = method.apply(this, args);
            reprocessAfterNavigation();
            return ret;
        };
    history.pushState = wrap(history.pushState);
    history.replaceState = wrap(history.replaceState);
})(window.history);

/* ---------- 초기 실행 ---------- */
setTimeout(processAllOnce, 50);
