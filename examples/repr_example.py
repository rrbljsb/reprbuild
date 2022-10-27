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
from getopt import getopt, GetoptError
from typing import Optional
from reprbuild import build_repr, is_valid_repr, ReprParser

USAGE = """custom_repr.p -e <eval> -o <object>
         eval   : If set, rebuild from returned representation and compare to original
         object : Default is all
              all         : Run all the example objects
              example1    : Run object 1
              example2    : Run object 2
     """

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
        self._repr_attrs = ["_name"]

    def __repr__(self) -> str:
        """to create a recursive repr() for myClass invoke build_repr
        as shown"""

        return build_repr(
            self, attr_list=self._repr_attrs, depth=-1, deepdive=False
        )

    def __str__(self):
        from reprbuild import format_repr

        return format_repr(build_repr(self, attr_list=self._repr_attrs))

    def __eq__(self, other) -> bool:
        if not isinstance(other, myClass):
            return False
        else:
            return self._name == other._name

    @classmethod
    def rebuild(cls, class_repr=None):
        """Return an instance of myClass based on the input dictionary

        Args:
            class_repr(string): string representation of the repr dictionary

        Returns:
            myClass: The object equivalent to the instance generating the repr

        Raises:
            ReprBuildError: if the dictionary is not valid

        Additional Information:
        """
        parser = ReprParser(class_repr)

        return myClass(name=parser.get_string("_name", "None"))


def _get_cmdline(argv):

    try:
        opts, args = getopt(  # pylint: disable=unused-variable
            argv, "heo:", ["object=", "eval"]
        )
    except GetoptError:
        print(USAGE)
        sys.exit(2)
    # Set default values
    _options = {}
    _options["object"] = "all"
    _options["eval"] = False
    for opt, arg in opts:
        if opt == "-h":
            print(USAGE)
            sys.exit()
        elif opt in ("-o", "--object"):
            _options["object"] = arg
        elif opt in ("-e", "--eval"):
            _options["eval"] = True
    return _options


def _get_example1():
    return myClass(name="example1")

def _get_example2():
    return myClass(name="example2")


examples_dict = {
    "example1": _get_example1,
    "example2": _get_example2,
}

def _check_repr( cur_obj, eval_repr=False):

    attr_rebuilders = {
        "myClass", myClass.rebuild
    }

    source_obj = examples_dict[cur_obj]()
    obj_repr = repr(source_obj)
    if not is_valid_repr(obj_repr) and hasattr(source_obj, "_repr_attrs"):
        obj_repr = build_repr(source_obj, attr_list=source_obj._repr_attrs)
    parser = ReprParser(obj_repr, attr_rebuilders)
    print(f"-------------  {cur_obj} ---------------")
    print(source_obj)
    print(f"------------- parser({cur_obj}).print ---------------")
    parser.print()
    if eval_repr:
        try:
            new_obj = parser.rebuild(parser.class_name,obj_repr)
            if new_obj == source_obj:
                print(f"New Object {cur_obj} is equivalent(==) to Original")
            else:
                print(
                    f"------ New Object {cur_obj} fails equivalence(==) test ---------"
                )
            print(f"------------- print( New {cur_obj} )---------------")
            print(new_obj)
            new_repr = repr(new_obj)
            if not is_valid_repr(new_repr) and hasattr(new_obj, "_repr_attrs"):
                new_repr = build_repr(new_obj, attr_list=new_obj._repr_attrs)
            print(f"------------- parser( New {cur_obj}).print ---------------")
        except Exception as error:  # pylint: disable=bare-except
            print(f"---- Unable to rebuild {cur_obj} to perform equivalence(==) test ----")
            print(f"Returned Exception{error}")

def main():
    """Create specific instances and print out the representations for them
    Args:

    Returns:

    Raises:

    Additional Information:
    """

    options = _get_cmdline(sys.argv[1:])
    disp_obj = options["object"]
    if disp_obj == "all":
        disp_list = examples_dict
    else:
        disp_list = disp_obj.split(",")
    for cur_obj in disp_list:
        _check_repr(cur_obj,options["eval"])

if __name__ == "__main__":
    main()
