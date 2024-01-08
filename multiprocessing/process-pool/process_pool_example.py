"""
SharedMemory 없이 ProcessPoolExecutor로 멀티프로세스
executor을 전역으로 생성해서 어떤 함수가 반복 실행될 때마다 executor 안만들게 되어 있음
"""

import concurrent.futures
import time

def sub_task(x):
    print(f"Subprocess {x} working")
    time.sleep(1)
    return f"Result from subprocess {x}"

# Create a persistent pool of workers
executor = concurrent.futures.ProcessPoolExecutor()

def test_func():
    sTime = time.time()
    futures = [executor.submit(sub_task, i) for i in range(5)]
    print(time.time()-sTime)
    results = [future.result() for future in futures]
    return results

def main():
    for _ in range(3):
        result = test_func()
        print(f"test_func returned: {result}")

    # Shutdown the executor when it's no longer needed
    executor.shutdown()

if __name__ == "__main__":
    main()
