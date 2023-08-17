import time
import ctypes
import ctypes.wintypes

# 현재 마우스 위치를 가져오는 함수
def get_mouse_position():
    pt = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


# 마우스 이동 함수
def mouse_move(x, y):
    # Windows에서는 좌표를 65535 범위로 정규화해야 함
    x = int(x * 65535 / ctypes.windll.user32.GetSystemMetrics(0))
    y = int(y * 65535 / ctypes.windll.user32.GetSystemMetrics(1))
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)


# 2차 베지어 곡선을 사용하여 마우스 움직임 함수
def bezier_mouse_move(end_x, end_y, control_x=None, control_y=None, duration=1.0):
    """
    
    :param end_x: 
    :param end_y: 
    :param control_x: 이걸 조정하면 마우스가 직선 형태로 움직이지 않고 곡선형태로 움직임 구현 가능 
    :param control_y: 이걸 조정하면 마우스가 직선 형태로 움직이지 않고 곡선형태로 움직임 구현 가능 
    :param duration: 
    :return: 
    """
    start_x, start_y = get_mouse_position()
    import random
    if control_x is None:
        control_x = (start_x + end_x) / 2
    if control_y is None:
        control_y = (start_y + end_y) / 2

    jitter = 1  # 떨림 정도 (높아지면 떨림 증가)
    steps = 400  # 움직임의 부드러움을 조절하는 스텝 수
    sleep_frequency = 4  # 몇번 움직일 때마다 sleep 할건지 -> 높을 수록 마우스 움직임이 더 빠름
    sleep_time = duration / steps

    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * start_x + 2 * (1 - t) * t * control_x + t ** 2 * end_x
        y = (1 - t) ** 2 * start_y + 2 * (1 - t) * t * control_y + t ** 2 * end_y
        # 이게 랜덤을 줘서 오히려 빗나갈 수도 있는데 테스트 해본결과 거의 수렴함
        # x += random.randint(-jitter, jitter) # x축 떨림 X
        y += random.randint(-jitter, jitter)
        mouse_move(x, y)
        if i % sleep_frequency == 0:
            time.sleep(sleep_time)

if __name__ == '__main__':
    # 윈도우 마우스 움직임 상수
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_ABSOLUTE = 0x8000
    # 예제 실행: 현재 위치에서 (500, 500)으로 2초 동안 부드럽게 이동
    bezier_mouse_move(100, 500, duration=0.5)
