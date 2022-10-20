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
Example showing how to create a custom representation
"""
import sys
from typing import Optional
from reprbuild.build_repr import build_repr, print_repr, parse_repr

_usage = "No program usage available"


class myClass:
    """class template compatible with recursive repr() generation and
        instantiation

    Args:
        from_repr (str): string representation of the dictionary produced
                    by calls to myClass.__repr__()
        name (str): myClass instance name (if it was output by repr())
    Raises:
        ValueError: if the representation is not a valid dictionary
    Additional Information:
        self._repr_list being defined is all that is reuired to allow
        the recursive algorithm include myClass in any class in
        which a myClass object is listed in the repr() without requiring
        changes to any existing __repr__ methods
        if repr_dict is passed in to __init__ it can be used to instiated
        a new instance of myClass equivialent to the instance which generated
        the representation
    """

    def __init__(
        self,
        name: Optional[str] = None,
    ):
        self._name = name
        self._repr_list = ["_name"]

    def __repr__(self) -> str:
        """to create a recursive repr() for myClass invoke build_repr
        as shown"""

        return build_repr(
            self, attr_list=self._repr_list, depth=-1, detailed=True, deepdive=False
        )

    def __str__(self) -> str:
        """optional text output for myClass instance
        print_repr will print a nicely formatted, indented, multi-line text
        representation of the instance of myClass"""
        print_repr(self.__repr__())

    def __eq__(self, other) -> bool:
        if not isinstance(other, myClass):
            return False
        else:
            return self._name == other._name

    @classmethod
    def from_repr(cls, class_repr=None):
        """Return a QuantumCircuit based on the input dictionary

        Args:
            class_repr(string): string representation of the repr dictionary

        Returns:
            myClass: The object equivalent to the instance generating the repr

        Raises:
            QiskitError: if the dictionary is not valid

        Additional Information:
            Create an instance as defined by the dictionary
            if needed to create instances of an attribute

            from qiskit.utils import ReprParser, parse_repr
            summary, attr_repr = parser.get_list('attrib')
            if summary is not None:
                from qiskit.utils import from_repr_mapper
                mapper = from_repr_mapper(summary.get('class',''))
                new_attr = mapper(attr_repr)
        """

        from qiskit.utils import ReprParser

        parser = ReprParser(class_repr)

        return myClass(name=parser.get_string("_name", "None"))


_custom_repr_list = ["_global_phase", "_base_name", "_data"]

def _get_myclass_object():

    return None


def _get_cmdline(argv):

    try:
        opts, args = getopt(  # pylint: disable=unused-variable
            argv, "heo:", ["object=", "eval"]
        )
    except GetoptError:
        print(_usage)
        sys.exit(2)
    # Set default values
    _options = {}
    _options["object"] = "all"
    _options["eval"] = False
    for opt, arg in opts:
        if opt == "-h":
            print(_usage)
            sys.exit()
        elif opt in ("-o", "--object"):
            _options["object"] = arg
        elif opt in ("-e", "--eval"):
            _options["eval"] = True
    return _options


_usage = """custom_repr.p -e <eval> -o <object>
         eval   : If set, evaluate returned repr and compareot original
         object : Default is custom
              all         : Run all the example objects
              example1    : Run object 1
              example2    : Run object 2
     """


def main():
    """Create specific instance and print out the representations for it
    Args:

    Returns:

    Raises:

    Additional Information:
    """

    options = _get_cmdline(sys.argv[1:])

    example_dict = {
        "example1", _get_example1,
        "example2", _get_example2,
    }

    disp_obj = options["object"]
    if disp_obj == "all":
        for cur_instance in example_dict:
            source_obj = example_dict[cur_instance]()
            obj_repr = repr(source_obj)
            print(f"-------------  {cur_instance} ---------------")
            print(source_obj)
            print_repr(obj_repr, indent="")
            if options["eval"]:
                new_summary = parse_repr(obj_repr)[0]
                if new_summary.get("class", "") == "QuantumCircuit":
                    new_obj = QuantumCircuit.from_repr(class_repr=obj_repr)
                    if new_obj == source_obj:
                        print(f"New Object {cur_instance} is equivalent(==) to Original")
                    else:
                        print(
                            f"---------- New Object {cur_instance} fails equivalence(==) test -------------"
                        )
                else:
                    print("Currently can only evaluate QuantumCircuits")
                new_repr = repr(new_obj)
                print_repr(new_repr)
    else:
        if disp_obj in circuit_dict.keys():
            source_obj = circuit_dict[disp_obj]()
            obj_repr = repr(source_obj)
        elif disp_obj == "custom":
            source_obj = _get_bell_circuit()
            try:
                obj_repr = build_repr(source_obj, attr_list=_custom_repr_list, depth=-1)
            except QiskitError as e:
                print("Exception during build from representation\n " + str(e))
        else:
            print(_usage)
            sys.exit()

        print(source_obj)
        print_repr(obj_repr, indent="")
        if options["eval"]:
            new_summary = parse_repr(obj_repr)[0]
            if new_summary.get("class", "") == "QuantumCircuit":
                new_obj = QuantumCircuit.from_repr(class_repr=obj_repr)
            if new_obj == source_obj:
                print(f"New Object {disp_obj} is equivalent(==) to Original")
            else:
                print(
                    f"---------- New Object {disp_obj} fails equivalence(==) test -------------"
                )
            new_repr = repr(new_obj)
            print_repr(new_repr)


if __name__ == "__main__":
    main()
