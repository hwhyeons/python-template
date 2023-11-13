import numpy as np
from numpy import ndarray

def make_shared_memory(numpy_shape: tuple, dtype: np ,element_type_size: int):
    np_zero_likes_frame = np.zeros(numpy_shape, dtype=dtype)
    n_bytes = np_zero_likes_frame.nbytes
    from multiprocessing.shared_memory import SharedMemory
    shared_screen_memory: SharedMemory = SharedMemory('ScreenFrameMemory', size=n_bytes, create=True)
    return shared_screen_memory

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
    print("복사할 ndarray shape : ",numpy_array.shape)

    from multiprocessing.shared_memory import SharedMemory
    shared_memory = SharedMemory(shared_memory_name)
    shared_memory.buf[:numpy_array.nbytes] = numpy_array.flatten()

def get_numpy_array_from_shared_memory(shared_memory_name: str, numpy_array_shape: tuple,dtype, element_type_size: int):
    """
    :param numpy_array_shape : 이미지 예시 -> (height,width,channel)
    :return:
    """

    from multiprocessing.shared_memory import SharedMemory
    shared_memory = SharedMemory(shared_memory_name)
    # 만약 크키 오류가 난다면 공유 메모리를 만든 상황의 type과 현재 받아오는 타입 불일치인 것
    shape_length = 1
    for i in numpy_array_shape:
        shape_length *= i
    rt_array = np.reshape(shared_memory.buf[:shape_length],newshape=numpy_array_shape)
    return rt_array
