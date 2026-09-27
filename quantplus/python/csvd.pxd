# cdef extern from "<Eigen/Dense>" namespace "Eigen":
cdef extern from "../include/cppTypes.h":
    cdef cppclass Matrix[T, U, V]:
        Matrix()
        T& operator()(int, int)
        T& operator()(int)

    # A matrix
    cdef cppclass MatrixXd:
        MatrixXd()
        MatrixXd(int, int)
        MatrixXd(const MatrixXd& other)
        void setZero()
        void setZero(int, int)
        float& operator()(int, int) # read access

    # a vector
    cdef cppclass VectorXd:
        Eigen::VectorXd()
        VectorXd(int)
        VectorXd(const VectorXd& other)
        int rows()
        int cols()
        double& operator[](int)
        void setZero()
        void setZero(int)

        float& operator()(int) # read access
