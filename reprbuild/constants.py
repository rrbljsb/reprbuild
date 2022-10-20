# This code is part of reprbuild
#
# (C) Copyright LJSB Enterprises, LLC 2022
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
Build a representation such that eval(repr(A)) is a dictionary which can be
unambiguous enough that we can build a class method such that cls(A).build_repr(eval(A))
is equivalent to A for most reasonable definitions of equivalence.
"""

REPRLISTATTRIBUTE = "_repr_list"
MAXRECURSION = 200
