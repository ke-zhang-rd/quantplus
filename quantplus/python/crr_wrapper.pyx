# distutils: language = c++
import numpy as np
cimport numpy as np
# cimport csvd
cimport eigen


cdef np.ndarray Vector3dToNumpy(eigen.VectorXd cx):
    print('3')
    result = np.ndarray((cx.rows()))
    for i in range(cx.rows()):
        result[i] = cx[i]

    print('4')
    return result

cdef eigen.VectorXd NumpyToVector3d (np.ndarray[double, ndim=1, mode="c"] x):
    print('1')
    cdef eigen.VectorXd cx = eigen.VectorXd(3)
    print('2')
    for i in range(3):
        print('i: ', i)
        cx[i] = x[i]
    print('3')
    return cx

cpdef xyz(i):
    return Vector3dToNumpy(NumpyToVector3d(i))

def abc(s):
    print(s)
'''
cdef np.ndarray Matrix3dToNumpy(Matrix3d m):
    result = np.ndarray([3, 3])
    for i in range(3):
        for j in range(3):
            result[i, j] = m.coeff(i, j)
    return result




cdef ensure_positive_Z(np.ndarray u, np.ndarray, v):
    Mat3d  = numpy to eigen
    eigne_result = csvd.ensure_positive_Z(csvd.Mat3d)
    resut = eigen to numpy(eigen_result)
    return result
'''
