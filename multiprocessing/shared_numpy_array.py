import multiprocessing

import numpy
import numpy as np
from numpy import ndarray


def add_num(start,end):

    TYPE_SIZE = 4  # numpy.int32
    from multiprocessing.shared_memory import SharedMemory
    sm = SharedMemory('NewMemory')
    # data = ndarray((sm.size//TYPE_SIZE,), dtype=numpy.int32, buffer=sm.buf)
    data = np.frombuffer(sm.buf, dtype=np.int32)
    for i in range(start,end+1):
        data[i] = i

if __name__ == '__main__':

    main_array_origin =np.zeros((10, 10, 3), dtype=np.int32)
    print(f"main_array.shape : {main_array_origin.shape}")
    print(f'main_array.nbytes : {main_array_origin.nbytes}')

    from multiprocessing.shared_memory import SharedMemory
    # n = 180
    # n_bytes = n * 4
    n_bytes = main_array_origin.nbytes
    n = n_bytes // 4

    sm = SharedMemory('NewMemory',size=n_bytes,create=True)
    data = ndarray((n,), dtype=numpy.int32, buffer=sm.buf)

    ps = []

    for num in range(1,8):
        p = multiprocessing.Process(target=add_num, args=(num*10,num*20))
        ps.append(p)
        p.start()

    for job in ps:
        job.join()

    print(data)
