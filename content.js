let currentLang = "en/kr";
let show = [];
const PROCESSED_ATTR = "bdbkr-processed";

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

function safeText(node) {
    return node?.textContent?.trim() || "";
}

/* ---------- 공통 제목 처리 함수 ---------- */
function addTitleGeneric(item, key, size, addEN = false) {
    const titleKRText = DATA[key];
    if (!titleKRText) {
        // console.log(`${key}에 해당하는 값이 없음`);
        return;
    }

    // 중복 방지
    if (item.hasAttribute(PROCESSED_ATTR)) return;

    // 이미 같은 구조가 들어가 있으면 추가하지 않음
    if (Array.from(item.children).some((c) => safeText(c) === titleKRText)) return;

    // 영어 원본
    if (addEN) {
        const titleEN = document.createElement("span");
        titleEN.textContent = key;
        item.appendChild(titleEN);
    }

    // 한국어 큰 제목
    const titleKR = document.createElement("span");
    titleKR.textContent = titleKRText;

    // 영어 작은 제목
    const titleENSmall = document.createElement("span");
    titleENSmall.textContent = key;
    titleENSmall.style.opacity = "50%";
    titleENSmall.style.fontSize = size;

    // 한국어 작은 제목
    const titleKRSmall = document.createElement("span");
    titleKRSmall.textContent = titleKRText;
    titleKRSmall.style.opacity = "50%";
    titleKRSmall.style.fontSize = size;

    // 추가
    item.append(titleKR, titleENSmall, titleKRSmall);

    // 기존 텍스트 노드 제거
    Array.from(item.childNodes).forEach((node) => {
        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() !== "") {
            node.remove();
        }
    });

    item.setAttribute(PROCESSED_ATTR, "1");
    setVisible(item);
}

/* ---------- 요소별 처리 ---------- */
function handleH1(item) {
    const key = safeText(item);
    if (!key) return;
    addTitleGeneric(item, key, "20px", true);
}

function handleCard(item) {
    const key = safeText(item.children[0]);
    if (!key) return;
    addTitleGeneric(item, key, "12px");
}

function handleFhSpan(item) {
    const key = safeText(item);
    if (!key) return;
    addTitleGeneric(item, key, "12px", true);
}

/* ---------- 표시 토글 ---------- */
function setVisible(item) {
    Array.from(item.children).forEach((child, i) => {
        child.style.display = show.includes(i) ? "block" : "none";
    });
}

/* ---------- 전체 처리 ---------- */
function processAllOnce() {
    document.querySelectorAll("h1").forEach(handleH1);
    document.querySelectorAll("._an").forEach(handleCard);

    const fh = document.querySelector("._b._d");
    if (fh?.children[0]) handleFhSpan(fh.children[0]);
}

/* ---------- Mutation Observer ---------- */
const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
        // 새로 추가된 노드 처리
        mutation.addedNodes?.forEach((node) => {
            if (node.nodeType !== 1) return;

            if (node.tagName === "H1") handleH1(node);
            node.querySelectorAll?.("h1").forEach(handleH1);
            node.querySelectorAll?.("._an").forEach(handleCard);

            const fh = node.querySelector("._b._d");
            if (fh?.children[0]) handleFhSpan(fh.children[0]);
        });

        // 텍스트 변경 감지 → 부모 재처리
        if (mutation.type === "characterData") {
            const parent = mutation.target.parentNode;
            if (parent?.tagName === "H1") {
                parent.removeAttribute(PROCESSED_ATTR);
                handleH1(parent);
            }
        }

        // 속성 변경 감지
        if (mutation.type === "attributes") {
            const target = mutation.target;
            if (target?.tagName === "H1") {
                target.removeAttribute(PROCESSED_ATTR);
                handleH1(target);
            }
        }
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
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

        document.querySelectorAll("._an, h1").forEach(setVisible);

        const fh = document.querySelector("._b._d");
        if (fh?.children[0]) setVisible(fh.children[0]);
    }
});

/* ---------- SPA 이동 감지 ---------- */
function reprocessAfterNavigation() {
    document.querySelectorAll("h1, ._an").forEach((el) =>
        el.removeAttribute(PROCESSED_ATTR)
    );
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
