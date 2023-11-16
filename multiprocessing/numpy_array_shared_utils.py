import time

import numpy as np
from numpy import ndarray

from multiprocessing.shared_memory import SharedMemory

"""
멀티프로세스를 사용해서 프로세스별 사용법

1. 중복 실행 되거나 중복 import가 될 가능성이 없는 시작 py파일에서 공유 메모리 영역 생성 (make_shared_memory() 호출)
2. numpy_array를 공유할 경우, 공유 메모리 영역에 데이터를 넣을 때는 copy_ndarray_to_shared_memory() 호출하고
    공유 메모리 영역에서 데이터를 가져올 때는 get_numpy_array_from_shared_memory() 호출해서 사용
3. 단순하게 flag를 공유하고 싶다면,
    set_flag_bit() 호출해서 flag를 설정하고
    get_flag_bit() 호출해서 flag를 가져오면 됨  
 
"""

# 전역으로 공유 메모리 유지

def make_shared_memory(name: str, numpy_shape: tuple, dtype: np, element_type_size: int):
    np_zero_likes_frame = np.zeros(numpy_shape, dtype=dtype)
    n_bytes = np_zero_likes_frame.nbytes
    from multiprocessing.shared_memory import SharedMemory
    shared_memory: SharedMemory = SharedMemory(name=name, size=n_bytes, create=True)
    print(f"공유 메모리 생성 : {name} : {shared_memory.buf.nbytes}")
    return shared_memory
    # shared_memory.close()

def set_flag_bit(shared_memory: SharedMemory, idx: int, flag: int | bool):
    """
    flag비트를 설정하는 함수
    :param shared_memory_name:
    :return:
    """


    if flag == True:
        flag = 1
    elif flag == False:
        flag = 0

    # shared_memory = SharedMemory(shared_memory_name)
    shared_memory.buf[idx] = flag
    # shared_memory.close()


def get_flag_bit(shared_memory: SharedMemory, idx: int):
    """
    flag비트를 가져오는 함수
    :param shared_memory_name:
    :return:
    """

    # shared_memory = SharedMemory(shared_memory_name)
    rt = shared_memory.buf[idx]
    # shared_memory.close()
    return rt


s_time_before_print = time.time()
def copy_ndarray_to_shared_memory(shared_memory: SharedMemory, numpy_array : ndarray, element_type_size: int):
    """
    참고
                            # print("shared_memory.buf.nbytes : ",shared_memory.buf.nbytes)
                        # data_frame = np.frombuffer(shared_memory.buf, dtype=np.uint8)
                        # data_frame[:] = self.frame_with_ts[0].flatten()
    :param shared_memory_name:
    :param numpy_array:
    :param element_type_size:
    :return:
    """

    # global s_time_before_print
    # if time.time()-s_time_before_print > 1:
    #     print("복사할 ndarray shape : ",numpy_array.shape)
    #     s_time_before_print = time.time()

    from multiprocessing.shared_memory import SharedMemory
    # shared_memory = SharedMemory(shared_memory_name)
    # shared_memory = SharedMemory(shared_memory_name)
    shared_memory.buf[:numpy_array.nbytes] = numpy_array.flatten()
    # shared_memory.close()

def get_numpy_array_from_shared_memory(shared_memory: SharedMemory, numpy_array_shape: tuple,dtype):
    """
    !!! shape에서 height가 앞으로 와야되는 것 주의 !!
    :param numpy_array_shape : (height,width,channel)
    :return:
    """
    # shared_memory = SharedMemory(shared_memory_name)
    shape_length = 1
    for i in numpy_array_shape:
        shape_length *= i
    rt_array = np.reshape(shared_memory.buf[:shape_length],newshape=numpy_array_shape)
    # shared_memory.close()

    return rt_array
