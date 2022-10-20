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
A parser to work with a representation created with qiskit.utils.build_repr.build_repr()
"""
from typing import Optional
from .reprbuild import parse_repr, is_valid_repr, ReprError, _builtin_repr
from .constants import RECREATEMETHOD


class ReprParser:
    """class to parse a representation string

    Args:
        obj_repr (str): string representation of the dictionary produced
                        by calls to myClass.__repr__()

    Raises:
        ReprError: if the representation is not a valid dictionary

    Additional Information:
    """

    def __init__(self, obj_repr):
        # Validate and create the string representation and the list representation
        if isinstance(obj_repr, str):
            self._repr_str = obj_repr
            try:
                obj_repr = eval(obj_repr)  # pylint: disable=eval-used
            except Exception as error:
                raise ReprError(
                    "ReprParser argument is invalid representation "
                ) from error
        else:
            obj_repr = repr(obj_repr)
            self._repr_str = obj_repr

        if not is_valid_repr(obj_repr):
            raise ReprError("ReprParser argument is invalid representation ")

        self._repr_str = obj_repr
        (self._summary, self._obj_dict) = parse_repr(self._repr_str)
        self._name = self._summary.get("name", "")
        self._class_name = self._summary.get("class", "")
        self._from_repr_name_mapping = {}

    def __repr__(self):
        return f"ReprParse for {self._class_name}  {self._name}"

    def get(self, name):
        """Get item in the dictionary of type unknown
        Args:
            name (str): Item to be parsed
        Returns:
            str: name of class of item
        Raises:

        Additional Information:
        """
        return parse_repr(self._obj_dict.get(name))

    def get_complex(self, name, default: [Optional] = None):
        """Get item in the dictionary of type complex
        Args:
            name (str): Item to be parsed
            default (class): return value if name is not found

        Returns:
            complex: Item value
        Raises:

        Additional Information:
        """
        complex_dict = parse_repr(self._obj_dict.get(name))[1]
        if _builtin_repr(complex_dict) and complex_dict[1] == "complex":
            return complex(complex_dict[0])
        else:
            return default

    def get_dict(self, name, default: [Optional] = None):
        """Get item in the dictionary and return as a dictionary
        Args:
            name (str): Item to be parsed
            default (dict): Default value to return if item is not present in the dictionary
        Returns:
            dict: Item value
        Raises:

        Additional Information:
        """
        summary, item_dict = parse_repr(self._obj_dict.get(name))
        if summary is not None and summary.get("class", "") in ("dict", "defaultdict"):
            # TODO: recursion on getting the dictionary to support calibrations
            return item_dict
        else:
            return default

    def get_float(self, name, default: [Optional] = None):
        """Get item in the dictionary of type complex
        Args:
            name (str): Item to be parsed
            default (class): return value if name is not found
        Returns:
            float: Item value
        Raises:

        Additional Information:
        """
        item_dict = parse_repr(self._obj_dict.get(name))[1]
        if (
            item_dict is not None
            and _builtin_repr(item_dict)
            and item_dict[1] == "complex"
        ):
            return float(item_dict[0])
        else:
            return default

    def get_int(self, name, default: [Optional] = None):
        """Get item in the dictionary of type complex
        Args:
            name (str): Item to be parsed
            default (class): return value if name is not found
        Returns:
            int: Item value
        Raises:

        Additional Information:
        """
        item_dict = parse_repr(self._obj_dict.get(name, None))[1]
        if item_dict is not None and _builtin_repr(item_dict) and item_dict[1] == "int":
            return int(item_dict[0])
        return default

    def get_list(self, name, default: [Optional] = None):
        """Get item in the dictionary and return as a list
        Args:
            name (str): Item to be parsed
            default (list): Default value to return if item is not present in the dictionary
        Returns:
            list: Item value
        Raises:

        Additional Information:
        """
        item_list = self._obj_dict.get(name, None)
        if item_list is None or not isinstance(item_list, (list, set, tuple)):
            item_list = default

        return item_list

    def get_set(self, name, default: [Optional] = None):
        """Get item in the dictionary and return as a list
        Args:
            name (str): Item to be parsed
            default (list): Default value to return if item is not present in the dictionary
        Returns:
            list: Item value
        Raises:

        Additional Information:
        """
        summary, item_dict = parse_repr(self._obj_dict.get(name))
        if summary is not None and summary.get("class", "") == "set":
            return set(item_dict)
        else:
            return default

    def get_tuple(self, name, default: [Optional] = None):
        """Get item in the dictionary and return as a list
        Args:
            name (str): Item to be parsed
            default (list): Default value to return if item is not present in the dictionary
        Returns:
            list: Item value
        Raises:

        Additional Information:
        """
        summary, item_dict = parse_repr(self._obj_dict.get(name))
        if summary is not None and summary.get("class", "") == "tuple":
            return tuple(item_dict)
        else:
            return default

    def get_string(self, name, default: [Optional] = None):
        """Return a string element from the parsed representation
        Args:
            name (str): Item to be parsed
            default (class): return value if name is not found
        Returns:
            str:  the string value for name
        """
        str_dict = self._obj_dict.get(name, None)
        if isinstance(str_dict, str):
            return str_dict
        return default

    @property
    def obj_dict(self):
        """Return a string element from the parsed representation
        Args:

        Returns:
            dict:  the representation as a dictionary
        """
        return self._obj_dict

    @property
    def class_name(self):
        """Return the class of the object that generated the representation
        Args:

        Returns:
            str:  the class of the object
        """
        return self._class_name

    @property
    def name(self):
        """Return the name of the object that generated the representation
        Args:

        Returns:
            str:  the object name
        """
        return self._class_name

    def get_repr(self, name):
        """Return the method registered by the add_class_mapper calls
        Args:
            name (str): Attribute class name as string
        Returns:
            method:  The method to rebuild an instance from the representation registed in
                    previous add_class_mapper calls
        """
        pass

    def rebuild(self, name, obj_repr):
        """Return the method registered by the add_class_mapper calls
        Args:
            name (str): Attribute class name as string
            obj_repr(str): The string representation of the object to be instantiated
        Returns:
            object:  The newly instantiated object instance defined in the representation
        Raises:
            ReprError: if the mapping is invalid
        """
        mapper = self._from_repr_name_mapping.get(name, None)
        if mapper is None:
            raise ReprError(f"No {RECREATEMETHOD} method found for {name}")
        if not is_valid_repr(obj_repr):
            raise ReprError(f"Invalid representation for {name}")
        summary = parse_repr(obj_repr)[0]
        if summary.get("class", "") != name:
            raise ReprError(
                f"Class repr mismatch expecting {name}, got {summary.get('class','')}"
            )
        return mapper(obj_repr)

    def _add_from_repr_mapping(self, class_name, class_mapper):
        self._from_repr_name_mapping[class_name] = class_mapper

    def _append_class_to_mapper(self, obj_class):
        if hasattr(obj_class, RECREATEMETHOD):
            class_name = obj_class.__class_name__
            repr_mapper = getattr(obj_class, RECREATEMETHOD)
            self._add_from_repr_mapping(class_name, repr_mapper)
        else:
            raise ReprError(f"No from_repr method in {obj_class.__class_name__}")

    def append_class_mapper(self, class_mapper):
        """Register a  the method used to rebuild from the recursive representation
        Args:
            class_mapper (Union[list, dict, class]): A list of class to be registered, or a dictionary
                    of names,methods to be registered or a single class to be registered
        Returns:
            method:  The method to rebuild an instance from the representation registered in
                    previous add_class_mapper calls
        Raises:
            ReprError: if the mapping is invalid
        """
        if isinstance(class_mapper, list):
            for cur_class in class_mapper:
                self._append_class_to_mapper(cur_class)
        elif isinstance(class_mapper, dict):
            for class_name, mapper in class_mapper.items():
                self._add_from_repr_mapping(class_name, mapper)
        else:
            self._append_class_to_mapper(class_mapper)
