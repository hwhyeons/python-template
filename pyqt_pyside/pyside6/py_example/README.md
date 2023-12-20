
사용법

1. Qt designer로 ui 파일 생성
2. 터미널 -> 해당 ui파일 경로로 이동 후
   `pyside6-uic ~~.ui -o ui_test_window.py`
3. 생성 된 ui_test_window.py를 로딩할 py파일을 하나 만들어서 로딩 (예시 파일에서는 gui_test.py)

   !! ui_test_window.py에다가 바로 main 함수 넣어서 gui 실행할 수 도 있지만,
   이렇게 하게 되면 나중에 ui파일 내용 변경되고 다시 py파일 만들 때마다 코드 수정해줘야됨
   -> 따라서 UI만을 구성하는 py파일과 실행 및 이벤트, 액션 함수를 구현하는 py파일 분리
