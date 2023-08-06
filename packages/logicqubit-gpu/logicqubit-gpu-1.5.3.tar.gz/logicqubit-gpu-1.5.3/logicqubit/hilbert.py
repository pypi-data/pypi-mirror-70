#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

import sympy as sp
from sympy.physics.quantum import TensorProduct
import cupy as cp
# try:
#  import cupy as cp
# except Exception:
#  raise RuntimeError('CuPy is not available!')

from logicqubit.utils import *


class Hilbert():
    __cuda = True
    __first_left = True

    def ket(self, value, d=2):
        result = Matrix([[Utils.onehot(i, value)] for i in range(d)], Hilbert.__cuda)
        return result

    def bra(self, value, d=2):
        result = Matrix([Utils.onehot(i, value) for i in range(d)], Hilbert.__cuda)
        return result

    def getAdjoint(self, psi):
        result = psi.adjoint()
        return result

    def product(self, Operator, psi):
        result = Operator * psi
        return result

    def kronProduct(self, list):  # produto de Kronecker
        A = list[0]  # atua no qubit 1 que é o mais a esquerda
        for M in list[1:]:
            A = A.kron(M)
        return A

    def setNumberOfQubits(self, number):
        Hilbert.__number_of_qubits = number

    def getNumberOfQubits(self):
        return Hilbert.__number_of_qubits

    def setCuda(self, cuda):
        Hilbert.__cuda = cuda

    def getCuda(self):
        return Hilbert.__cuda

    def setFirstLeft(self, value):
        Hilbert.__first_left = value

    def isFirstLeft(self):
        return Hilbert.__first_left


class Matrix:

    def __init__(self, matrix, cuda=True):
        self.__matrix = matrix
        self.__cuda = cuda
        if isinstance(matrix, list):
            if self.__cuda:
                self.__matrix = cp.array(matrix)
            else:
                self.__matrix = sp.Matrix(matrix)
        else:
            self.__matrix = matrix

    def __add__(self, other):
        result = self.__matrix + other.get()
        return Matrix(result, self.__cuda)

    def __sub__(self, other):
        result = self.__matrix - other.get()
        return Matrix(result, self.__cuda)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            other = other.get()
            if self.__cuda:
                result = cp.dot(self.__matrix, other)
            else:
                result = self.__matrix * other
        else:
            result = self.__matrix * other
        return Matrix(result, self.__cuda)

    def __truediv__(self, other):
        result = self.__matrix * (1./other)
        return Matrix(result, self.__cuda)

    def __eq__(self, other):
        return self.__matrix == other.get()

    def __str__(self):
        return str(self.__matrix)

    def kron(self, other):  # Kronecker product
        if self.__cuda:
            result = cp.kron(self.__matrix, other.get())
        else:
            result = TensorProduct(self.__matrix, other.get())
        return Matrix(result, self.__cuda)

    def get(self):
        return self.__matrix

    def trace(self):
        result = self.__matrix.trace()
        return Matrix(result, self.__cuda)

    def adjoint(self):
        if self.__cuda:
            result = self.__matrix.transpose().conj()
        else:
            result = self.__matrix.transpose().conjugate()
        return Matrix(result, self.__cuda)
