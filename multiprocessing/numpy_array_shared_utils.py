import time

import numpy as np
from numpy import ndarray

from multiprocessing.shared_memory import SharedMemory

# 전역으로 공유 메모리 유지
# tmp_List에 넣는건 자동할당해제 되지 않도록 위함 (참조 카운트 유지)
# 원래 이 딕셔너리도 공유 변수로 하는게 더 나아보이지만 임시로 이렇게 해놓음
tmp_dict = dict()

def make_shared_memory(name: str, numpy_shape: tuple, dtype: np, element_type_size: int):
    np_zero_likes_frame = np.zeros(numpy_shape, dtype=dtype)
    n_bytes = np_zero_likes_frame.nbytes
    from multiprocessing.shared_memory import SharedMemory
    shared_memory: SharedMemory = SharedMemory(name=name, size=n_bytes, create=True)
    tmp_dict[name] = shared_memory
    return shared_memory

def set_flag_bit(shared_memory_name: str, idx: int, flag: int | bool):
    """
    flag비트를 설정하는 함수
    :param shared_memory_name:
    :return:
    """


    if flag == True:
        flag = 1
    elif flag == False:
        flag = 0

    shared_memory = SharedMemory(shared_memory_name)
    shared_memory.buf[idx] = flag
    global tmp_dict
    tmp_dict[shared_memory_name] = shared_memory


def get_flag_bit(shared_memory_name: str, idx: int):
    """
    flag비트를 가져오는 함수
    :param shared_memory_name:
    :return:
    """

    shared_memory = SharedMemory(shared_memory_name)
    global tmp_dict
    tmp_dict[shared_memory_name] = shared_memory
    return shared_memory.buf[idx]


s_time_before_print = time.time()
def copy_ndarray_to_shared_memory(shared_memory_name: str, numpy_array : ndarray, element_type_size: int):
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

    global s_time_before_print
    if time.time()-s_time_before_print > 1:
        print("복사할 ndarray shape : ",numpy_array.shape)
        s_time_before_print = time.time()

    from multiprocessing.shared_memory import SharedMemory
    # shared_memory = SharedMemory(shared_memory_name)
    shared_memory = SharedMemory(shared_memory_name)
    global tmp_dict
    tmp_dict[shared_memory_name] = shared_memory
    shared_memory.buf[:numpy_array.nbytes] = numpy_array.flatten()

def get_numpy_array_from_shared_memory(shared_memory_name: str, numpy_array_shape: tuple,dtype):
    """
    !!! shape에서 height가 앞으로 와야되는 것 주의 !!
    :param numpy_array_shape : (height,width,channel)
    :return:
    """
    shared_memory = SharedMemory(shared_memory_name)
    global tmp_dict
    tmp_dict[shared_memory_name] = shared_memory
    shape_length = 1
    for i in numpy_array_shape:
        shape_length *= i
    rt_array = np.reshape(shared_memory.buf[:shape_length],newshape=numpy_array_shape)
    return rt_array
