const PskillLvOptions = {
  expand: [1,2,3],
  chance: [1,2,3],
  enhance: [1,2],
  support:[1]
};

// 2. Pskill選択肢の変更イベントを監視する
const PskillSelect = document.getElementById('Pskill_name');
const PskillLvInput = document.getElementById('Pskill_Lv');

PskillSelect.addEventListener('change', (event) => {
  const selectedPskill = event.target.value;
  // 3. PskillLv選択肢を更新する
  PskillLvInput.min = Math.min(...PskillLvOptions[selectedPskill]);
  PskillLvInput.max = Math.max(...PskillLvOptions[selectedPskill]);
  PskillLvInput.value = PskillLvInput.min;
});

// 初期状態でPskillLv選択肢を更新する
const selectedPskill = PskillSelect.value;
PskillLvInput.min = Math.min(...PskillLvOptions[selectedPskill]);
PskillLvInput.max = Math.max(...PskillLvOptions[selectedPskill]);


// PskillLv選択肢の変更イベントを監視する
PskillLvInput.addEventListener('change', (event) => {
  // 選択されたPskillLvの値を取得する
  const selectedPskillLv = parseInt(event.target.value, 10);
  console.log(selectedPskillLv);
});

// Startボタンがクリックされたときの処理
function RunPython(){
  document.getElementById("result").style.display = "none";
  document.getElementById("loading").style.display = "block";
  document.getElementById("start_button").disabled = true;
  // input要素から値を取得
  var song_name = document.getElementById("song_name").value;
  var idol_number = document.getElementById("idol_number").value.split(",");
  var appeal = parseInt(document.getElementById("appeal").value);
  var Pskill_name = document.getElementById("Pskill_name").value;
  var Pskill_Lv = parseInt(document.getElementById("Pskill_Lv").value);
  var trial = parseInt(document.getElementById("trial").value);

  // Pythonコードに渡すためのデータを準備
  var data = {
    "song_name": song_name,
    "idol_number": idol_number,
    "appeal": appeal,
    "Pskill_name": Pskill_name,
    "Pskill_Lv":Pskill_Lv,
    "trial":trial
  };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function() {
    if (xhr.status === 200) {
      data_parse = JSON.parse(xhr.responseText);
      document.getElementById("result").innerHTML = data_parse;
      document.getElementById("result").style.display = "block";
      document.getElementById("loading").style.display = "none";
      document.getElementById("start_button").disabled = false;
    
    } else {
      console.error("Error:", xhr.statusText);
    }
  };
  xhr.onerror = function() {
    console.error("Error:", xhr.statusText);
  };
  xhr.send(JSON.stringify(data));
  };






