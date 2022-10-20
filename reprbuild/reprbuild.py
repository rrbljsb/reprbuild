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
from typing import Optional
import numpy as np

from .constants import REPRLISTATTRIBUTE, MAXRECURSION

class ReprError(Exception):
    """Base class for errors raised while processing a representation."""

    def __init__(self, *message):
        """Set the error message."""
        super().__init__(" ".join(message))
        self.message = " ".join(message)

    def __str__(self):
        """Return the message."""
        if not isinstance(self.message, str):
            return repr(self.message)
        else:
            return self.message


def _get_summary(source):
    _summary = f"class: {source.__class__.__name__}"
    _src_name = getattr(source, "name", None)
    if _src_name is not None:
        _summary += f",name: {_src_name}"

    return _summary


def build_attribute_dict(
    source,
    attribute,
    depth=1,
    detailed=True,
    deepdive=False,
    recursion=0,
):
    """
    Args:
        source (Unknown)    : Object to be built into a dictionary
        attribute (Unknown) : Name of the source's attribute to include
        depth (int)         : if == 0 : return object summary only as string
                              if != 1 : return list[ object summary, dict{ attribute :,repr to depth -1]
                                       a starting depth -1 will fully expand all atrributes
        detailed(boolean)   : if not True only the attribute summary is included  regardless of depth
        deepdive (boolean)  : if True append attributes returned from dir() to list
        recursion (int)     : prevent unlimited recursion in case of circular references
    Raises:
        ValueError: invalid value
    Returns:
        String: Representation string of source.cur_member
    Raises:
    Additional Information:
        Each attribute entry willl eval to a list
            attr_dict[0]: Summary of the attribute, class fothe attribute
            attr_dict[1]: Representation of a dictionary for members of the attribute
                                listed in repr_list for its class
    """
    if attribute is None:
        attr = source
    else:
        attr = getattr(source, attribute, None)
    attr_repr = [_get_summary(attr), None]
    if attr is None:
        attr_repr = None
    elif isinstance(attr, str):
        attr_repr = attr
    elif isinstance(attr, (int, float, complex)):
        attr_repr[1] = (repr(attr), attr.__class__.__name__)
    elif isinstance(attr, (np.integer, np.floating, np.complexfloating, np.ndarray)):
        attr_repr[1] = (repr(attr), attr.__class__.__name__)
    elif depth != 0:
        if hasattr(attr, REPRLISTATTRIBUTE):
            cur_repr = build_object_dict(
                attr,
                getattr(attr, REPRLISTATTRIBUTE),
                depth=depth - 1,
                detailed=detailed,
                deepdive=deepdive,
                recursion=recursion + 1,
            )
            attr_repr[1] = cur_repr
        elif isinstance(attr, (list, tuple, set)):
            repr_list = []
            if len(attr) > 0:
                for cur_attr in attr:
                    if cur_attr is None:
                        pass
                    elif hasattr(cur_attr, REPRLISTATTRIBUTE):
                        cur_repr = build_object_dict(
                            cur_attr,
                            getattr(attr, REPRLISTATTRIBUTE),
                            depth=depth - 1,
                            detailed=detailed,
                            deepdive=deepdive,
                            recursion=recursion + 1,
                        )
                    elif isinstance(cur_attr, (list, tuple, set, dict)):
                        cur_repr = build_attribute_dict(
                            cur_attr,
                            None,
                            depth=depth - 1,
                            detailed=detailed,
                            deepdive=deepdive,
                            recursion=recursion + 1,
                        )
                    else:
                        cur_repr = repr(cur_attr)
                    repr_list.append(cur_repr)
            if isinstance(attr, tuple):
                repr_list = tuple(repr_list)
            elif isinstance(attr, set):
                repr_list = set(repr_list)
            attr_repr[1] = repr_list
        elif isinstance(attr, dict):
            repr_list = {}
            if len(attr) > 0:
                repr_list = {}
                for cur_key, cur_attr in attr.items():
                    if cur_attr is None:
                        pass
                    elif hasattr(cur_attr, REPRLISTATTRIBUTE):
                        cur_repr = build_object_dict(
                            cur_attr,
                            getattr(attr, REPRLISTATTRIBUTE),
                            depth=depth - 1,
                            detailed=detailed,
                            deepdive=deepdive,
                            recursion=recursion + 1,
                        )
                    elif isinstance(cur_attr, (list, tuple, set, dict)):
                        list_dict = build_attribute_dict(
                            cur_attr,
                            None,
                            depth=depth - 1,
                            detailed=detailed,
                            deepdive=deepdive,
                            recursion=recursion + 1,
                        )
                        cur_repr = list_dict
                    else:
                        cur_repr = repr(cur_attr)
                    repr_list[cur_key] = cur_repr
            attr_repr[1] = repr_list
        else:
            attr_repr[1] = repr(attr)

    return attr_repr


def build_object_dict(
    source,
    attr_list=None,
    depth=1,
    detailed=True,
    deepdive=False,
    recursion=0,
):
    """Create a dictionary representation for the object
    Args:
        source (Unknown)    : Object to be built into a dictionary
        attr_list  (list)   : List of the object's attributes to include
        depth (int)         : if == 0 : return object summary only as string
                              if != 1 : return list[ object summary, dict{ attribute :,repr to depth -1]
                                       a starting depth -1 will fully expand all atrributes
        detailed(boolean)   : if not True only the attribute summary is included  regardless of depth
        deepdive (boolean)  : if True append attributes returned from dir() to list
        recursion (int)     : number of levels of recursion allowable for this representation
    Returns:
        str: repr() of the dictionary generated, eval of string results in a dictionary
    Raises:
        TypeError           : if member_list is not a list or dict

    Additional Information:
    """
    attr_depths = {}
    if isinstance(attr_list, dict):
        attr_depths = attr_list
    elif isinstance(attr_list, list):
        for cur_member in attr_list:
            attr_depths[cur_member] = depth
    elif attr_list is not None:
        raise TypeError("member_list not of type list or dict")
    if deepdive:
        attr_depths = _append_attributes(source, attr_depths, depth=depth)

    if recursion > MAXRECURSION:
        member_dict = f"<Recursion limit of {MAXRECURSION} exceeded>"
    else:
        member_dict = {}
        for cur_member, cur_depth in attr_depths.items():
            cur_dict = build_attribute_dict(
                source,
                cur_member,
                depth=cur_depth,
                detailed=detailed,
                deepdive=deepdive,
                recursion=recursion + 1,
            )
            if cur_dict is not None:
                member_dict[cur_member] = cur_dict

    return [_get_summary(source), member_dict]


def build_repr(source, **kwargs):
    """Create a dictionary representation for the object
    Args:
        source (Unknown)    : Object to be built into a dictionary
        **kwargs (params)   :
            attr_list  (list)   : List of the object's attributes to include
            depth (int)         : if == 0 : return object summary only as string
                                  if != 1 : return list[ object summary,
                                                         dict{ attribute :,repr to depth -1
                                                       ]
                                           a starting depth -1 will fully expand all atrributes
            detailed(boolean)   : if not True only the attribute summary is included  regardless of depth
            deepdive (boolean)  : if True append attributes returned from dir() to list
    Returns:
        str: repr() of the dictionary generated, eval of string results in a dictionary
    Raises:
        TypeError           : if member_list is not a list or dict

    Additional Information:
    """
    return repr(build_object_dict(source, **kwargs))


def parse_repr(obj_repr):
    """Parse off and return the embedded dictionary, if it exists
    Args:
        obj_repr (str): Object repr to be parsed
    Returns:
        dict:  class name, name
        list:  dictionary embedded inside representation
    Raises:

    Additional Information:
    """
    (summary, repr_dict) = (None, None)
    if isinstance(obj_repr, str):
        try:
            obj_repr = eval(obj_repr)  # pylint: disable=eval-used
        except:  # pylint: disable=bare-except
            obj_repr = None

    if isinstance(obj_repr, list) and len(obj_repr) == 2:
        if isinstance(obj_repr[0], str):
            summary_list = obj_repr[0].split(",")
            classname = summary_list[0]
            if classname.startswith("<class '"):
                summary = {}
                summary["class"] = classname
            elif classname.startswith("class: "):
                summary = {}
                summary["class"] = classname.split("class: ")[1]

            if summary is not None:
                repr_dict = obj_repr[1]
                summary["name"] = ""
                if len(summary_list) > 1:
                    name_list = summary_list[1].split("name: ")
                    if len(name_list) > 1 and name_list[1] is not None:
                        summary["name"] = name_list[1]

    return summary, repr_dict


def print_repr(repr_dict, indent=""):
    """Print a readable version of the representation dictionary
    Args:
        repr_dict (str): Object repr to be parsed
        indent (str):    Indentation level for the output
    Returns:
    Raises:

    Additional Information:
    """
    summary, custom_dict = parse_repr(repr_dict)
    obj_class = summary.get("class", "")
    if obj_class in ("str", "int", "float", "complex"):
        print(f"{indent}{custom_dict}")
    elif obj_class == "list":
        print(f"{indent}{summary.get('name','')} : {summary.get('class','Unknown')}")
        _print_repr_list(custom_dict, indent + "    ")
    elif obj_class in ("defaultdict", "dict"):
        print(f"{indent}{summary.get('name','')} : {summary.get('class','Unknown')}")
        _print_repr_dict(custom_dict, indent + "    ")
    elif isinstance(custom_dict, dict):
        print(f"{indent}{summary.get('name','')} : {summary.get('class','Unknown')}")
        _print_repr_dict(
            custom_dict,
            indent + "    ",
            name=summary.get("name", ""),
        )


def _builtin_repr(list_dict):
    is_builtin = (
        isinstance(list_dict, tuple)
        and (len(list_dict) == 2)
        and isinstance(list_dict[0], str)
        and isinstance(list_dict[0], str)
    )
    return is_builtin


def _print_repr_element(
    cur_obj, indent="", header: Optional = None, name: Optional = ""
):
    if isinstance(cur_obj, (str, int, float, complex)):
        print(f"{indent}{name} : {cur_obj}")
    elif isinstance(cur_obj, list):
        (summary, list_dict) = parse_repr(cur_obj)
        if (
            summary is not None
            and len(summary) == 2
            and summary.get("class", "None") not in ("None", "NoneType", "")
        ):
            if header is not None and not _builtin_repr(list_dict):
                print(header)
                indent += "    "
            _print_repr_dict(list_dict, indent, name=name)
        else:
            if header is not None:
                print(header)
                indent += "    "
            _print_repr_list(cur_obj, indent)
    elif isinstance(cur_obj, (tuple, set)):
        if header is not None:
            print(header)
            indent += "    "
        _print_repr_list(cur_obj, indent)
    elif isinstance(cur_obj, dict):
        if header is not None:
            print(header)
            indent += "    "
        _print_repr_dict(cur_obj, indent, name=name)
    else:
        print_repr(cur_obj, indent)


def _print_repr_dict(obj_dict, indent="", name: Optional = ""):
    if isinstance(obj_dict, str):
        print(f"{indent}{obj_dict}")
    elif isinstance(obj_dict, dict):
        for cur_name, cur_obj in obj_dict.items():
            _print_repr_element(
                cur_obj,
                indent,
                name=cur_name,
                header=f"{indent}{cur_name}: {cur_obj.__class__.__name__}",
            )
    elif isinstance(obj_dict, tuple):
        if _builtin_repr(obj_dict):
            print(f"{indent}{name} : {obj_dict[0]} : {obj_dict[1]}")
        else:
            for item in obj_dict:
                _print_repr_element(item, indent, name=name)
    elif isinstance(obj_dict, list):
        summary = parse_repr(obj_dict)[0]
        if (
            summary is not None
            and len(summary) == 2
            and summary.get("class", "None") not in ("None", "NoneType", "")
        ):
            print_repr(obj_dict, indent)
        else:
            # print(f"{indent}{name} : {obj_dict.__class__.__name__}")
            for item in obj_dict:
                # _print_repr_element(item, indent=indent + "    ")
                _print_repr_element(item, indent=indent + "    ")
    else:
        print(f"Type mismatch, expecting 'dict' got {type(obj_dict)}")


def is_valid_repr(obj_repr):
    """Determine if the input is a valid representation.  If a string attempt to convert it to a list
       before evaluation.
       If not a list or not convertible to a list or not valid representation list, return False
    Args:
        obj_repr (Union[list,str]): Object repr to be parsed
    Returns:
        Boolean: True if input can be converted to a valid representation
    Raises:

    Additional Information:
    """
    if isinstance(obj_repr, str):
        try:
            obj_repr = eval(obj_repr)  # pylint: disable=eval-used
        except:  # pylint: disable=bare-except
            obj_repr = None

    summary = parse_repr(obj_repr)[0]
    return (
        summary is not None
        and len(summary) == 2
        and summary.get("class", "None") not in ("None", "NoneType", "")
    )


def _print_repr_list(obj_dict, indent):
    (summary, list_dict) = parse_repr(obj_dict)
    if (
        summary is not None
        and len(summary) == 2
        and summary.get("class", "None") not in ("None", "NoneType", "")
    ):
        print(f"{indent}{summary.get('name','')} : {summary.get('class','Unknown')}")
        _print_repr_dict(list_dict, indent + "    ")
    elif isinstance(obj_dict, (tuple, set, list)):
        for cur_obj in obj_dict:
            _print_repr_element(cur_obj, indent)
    else:
        print(f"Type mismatch expecting 'list' go {type(obj_dict)}")


def _append_attributes(source, attr_depths, depth=1):
    __obj_dict__ = getattr(source, "__dict__", None)
    if __obj_dict__ is not None:
        for i in __obj_dict__:
            attr_depths[i] = depth
    for i in dir(source):
        attr_depths[i] = depth
    return attr_depths
