from fortress.core.variables.local_variable import LocalVariable
from fortress.core.variables.state_variable import StateVariable

from fortress.core.declarations.solidity_variables import SolidityVariable

from fortress.slithir.variables.temporary import TemporaryVariable
from fortress.slithir.variables.constant import Constant
from fortress.slithir.variables.reference import ReferenceVariable
from fortress.slithir.variables.tuple import TupleVariable


def is_valid_rvalue(v):
    return isinstance(
        v,
        (
            StateVariable,
            LocalVariable,
            TemporaryVariable,
            Constant,
            SolidityVariable,
            ReferenceVariable,
        ),
    )


def is_valid_lvalue(v):
    return isinstance(
        v, (StateVariable, LocalVariable, TemporaryVariable, ReferenceVariable, TupleVariable,),
    )
