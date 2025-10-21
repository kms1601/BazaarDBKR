const radios = document.querySelectorAll('input[name="option"]');

// 초기 상태 로드
chrome.storage.sync.get("selectedOption", ({ selectedOption }) => {
  if (selectedOption) {
    const radio = document.querySelector(`input[value="${selectedOption}"]`);
    if (radio) radio.checked = true;
  }
});

// 선택 변경 시 저장
radios.forEach(radio => {
  radio.addEventListener("change", () => {
    chrome.storage.sync.set({ selectedOption: radio.value });

  });
});
