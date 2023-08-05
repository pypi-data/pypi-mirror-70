"""Reporting of QuEST states"""
# Copyright 2019 HQS Quantum Simulations GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing
from pyquest_cffi.questlib import quest, _PYQUEST, tquestenv, tqureg


class reportQuESTEnv(_PYQUEST):
    """
    Report the properties of the QuEST simulation environment to stdout

    Args:
        env: QuEST environment for which the parameter are reported

    """

    def call_interactive(self, env: tquestenv) -> None:
        """Call interactive Pyquest-cffi function"""
        return quest.reportQuESTEnv(env)

    @property
    def restype(self) -> str:
        """Return result type"""
        return "void"

    @property
    def argtype(self) -> typing.List[str]:
        """Return type of argument"""
        return ["QuESTEnv"]


class reportQuregParams(_PYQUEST):
    """
    Reports the parameters of a quantum register to stdout

    Args:
        qureg: Quantum register for which the parameter are reported

    """

    def call_interactive(self, qureg: tqureg) -> None:
        """Call interactive Pyquest-cffi function"""
        return quest.reportQuregParams(qureg)

    @property
    def restype(self) -> str:
        """Return result type."""
        return "void"

    @property
    def argtype(self) -> typing.List[str]:
        """Return argument type"""
        return ["Qureg"]


class reportState(_PYQUEST):
    """Report QuEST state"""

    def call_interactive(self, qureg: tqureg) -> None:
        """Call interactive Pyquest-cffi function"""
        return quest.reportState(qureg)

    @property
    def restype(self) -> str:
        """Return result type."""
        return "void"

    @property
    def argtype(self) -> typing.List[str]:
        """Return argument type."""
        return ["Qureg"]


class reportStateToScreen(_PYQUEST):
    """
    Report statevector or density matrix in a qureg to stdout

    Args:
        qureg: the quantum register
        env: the environment of the quantum register

    """

    def call_interactive(self, qureg: tqureg, env: tquestenv, a: int = 0) -> None:
        """Call interactive Pyquest-cffi function"""
        return quest.reportStateToScreen(qureg, env, a)

    @property
    def restype(self) -> str:
        """Return result type"""
        return "void"

    @property
    def argtype(self) -> typing.List[str]:
        """Return argument type."""
        return ["Qureg", "QuESTEnv", "int"]
