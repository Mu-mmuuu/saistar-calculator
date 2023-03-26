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


function runPythonScript() {
  // 他のinputから値を取得
  var input1_value = document.getElementById("song_name").value;
  var input2_value = document.getElementById("idol_number").value.split(',').map(function(item) {
    return parseInt(item, 10);
  });
  var input3_value = document.getElementById("appeal").value;
  var input4_value = document.getElementById("Pskill_name").value;
  var input5_value = document.getElementById("Pskill_Lv").value;
  var input6_value = document.getElementById("trial").value;

    // Pythonスクリプトに引数として渡すコマンドを作成
  var command = "python calculator.py " + input1_value + " " + input2_value + " " + input3_value + " " + input4_value + " " + input5_value + " " + input6_value;

  // コマンドを実行
  // var command = 'your-command'; // 実行するコマンドを指定する
  var xhr = new XMLHttpRequest();
  console.log(xhr)
  xhr.open('GET', '/execute-command?command=' + encodeURIComponent(command), true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      if (response.result) {
        updateResult(response.result);
      } else {
        updateResult(response.error);
      }
    } else {
      console.log('Request failed. Status code: ' + xhr.status);
    }
  };
  xhr.send();
}

function updateResult(result) {
  document.getElementById('result').innerHTML = result;
}


