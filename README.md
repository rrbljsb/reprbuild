# reprbuild
## python3 library

Build recursive python repr without requiring modifcations to super-class repr method.

## Features

The goal of this library is to provide tools to build recursive representations that provide a single, unambiguous, authoritative representation of any variable within a system.

## Implementation
+ Define the class hidden variable _repr_list as Union[list,dict] which defines the class attributes which are to be included in the representation and optionally, using a dict, the maximum level of recursion for representation of the attribute. Recursion level of -1 is theoretically unlimited but has a maximum system level recursion currently set to 200 in the library.