const PskillLvOptions = {
  expand: [1,2,3],
  chance: [1,2,3],
  enhance: [1,2],
  else:[1]
};

// 2. Pskill選択肢の変更イベントを監視する
const PskillSelect = document.getElementById('Pskill_name');
PskillSelect.addEventListener('change', (event) => {

  // 3. PskillLv選択肢を更新する
  const selectedPskill = event.target.value;
  const PskillLvInput = document.getElementById('Pskill_Lv');
  PskillLvInput.min = Math.min(...PskillLvOptions[selectedPskill]);
  PskillLvInput.max = Math.max(...PskillLvOptions[selectedPskill]);
  PskillLvInput.value = PskillLvInput.min;
});

// 初期状態でPskillLv選択肢を更新する
const selectedPskill = PskillSelect.value;
const PskillLvInput = document.getElementById('Pskill_Lv');
PskillLvInput.min = Math.min(...PskillOptions[selectedPskill]);
PskillLvInput.max = Math.max(...PskillOptions[selectedPskill]);


// PskillLv選択肢の変更イベントを監視する
PskillLvInput.addEventListener('change', (event) => {
  // 選択されたPskillLvの値を取得する
  const selectedPskillLv = parseInt(event.target.value, 10);
  console.log(selectedPskillLv);
});
