function showButton() {
            // 선택한 라디오 버튼의 값을 확인
            var radioButton = document.querySelector('input[name="radio"]:checked');
            if (radioButton && radioButton.value === 'date_button') {
                // 값이 "show"인 경우, 숨겨진 버튼을 보이도록 설정
              //  document.getElementById('hiddenButtonStart').style.display = 'block';
              //  document.getElementById('hiddenButtonEnd').style.display = 'block';
                document.getElementById('hiddenDateDiv').style.display = 'block';
            } else {
                // 다른 값이 선택되었거나 선택이 해제된 경우, 숨겨진 버튼을 다시 숨김
               // document.getElementById('hiddenButtonStart').style.display = 'none';
              //  document.getElementById('hiddenButtonEnd').style.display = 'none';
                document.getElementById('hiddenDateDiv').style.display = 'none';
            }
            if (radioButton && radioButton.value === 'genre_button') {
                // 값이 "show"인 경우, 숨겨진 버튼을 보이도록 설정
                document.getElementById('buttonlist').style.display = 'block';
            } else {
                // 다른 값이 선택되었거나 선택이 해제된 경우, 숨겨진 버튼을 다시 숨김
                document.getElementById('buttonlist').style.display = 'none';
            }
        }

         function showSelectedButton() {
            var selectElement = document.getElementById('buttonList');
            var selectedValue = selectElement.value;
            var buttonElement = document.getElementById(selectedValue);

            // 선택된 버튼을 보이거나 숨김
            var buttons = document.getElementsByTagName('button');
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].style.display = 'none';
            }
            buttonElement.style.display = 'block';
        }