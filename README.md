# reprbuild
## python3 library

Build recursive python representation without requiring modifcations to all class repr methods.

## Features

The goal of this library is to provide tools to build recursive representations that provide a single, unambiguous, authoritative representation of any variable within a system. Tools to build, parse, print and recreate an equivalent instance from the recursive representations are provided.

## Implementation
+ Define the class variable _repr_attrs as Union[list,dict] which defines the class attributes which are to be included in the representation. Optionally define _repr_list as a dict specify attribute namena maximum level. 
+ Update the constants for list name, rebuild method and maximum recursion as desired 
```
REPRATTRIBUTES = "_repr_attrs"
MAXRECURSION = 200
REBUILDER = "rebuild"

```
+ Added the attributes to be included in the representation
```
   def __init__(self):
       ...
       self._repr_attrs = ["name","rank","serialnum"]
       
   @classmethod
   def get_build_map():
      return {
          "name" : NameClass.rebuild,
          "rank" : RankClass.rebuild,
          "serialnum" : SerialClass.rebuild
       }
      
```
+ Update or create method __repr__ to use build_repr method
```
def __repr__(self):
   return reprbuild.build_repr(self,self._repr_attrs)
```
+ Add the list of attributes to classes of any attributes included in the representation. The _repr_list is all that is required for the class to be included in the recursive representation.  The class' __repr__ method does not have to be modified/defined unless desired
+ Add the __str__ method if a nicely parsed and indented print of the representation is desired
## Print user readable representation
```
   def __str__(self):
      reprbuild.print_repr(build_repr(self)
```

## Build an equivalent instance from representation
+ Implement the rebuild() method for all attributes included in the recursive representation
+ Create a parser
+ If desired, add the rebuild() methods to the parser
```
   from reprbuild import ReprParser
   def rebuild(self,obj_repr)
       parser = ReprParse(obj_repr, cls.get_build_map()       
       ....
         Code to retrieve neccessary attributes and build an
         equivalent instance
       
	   int_attr     = parser.get_int(name,default)
	   float_attr   = parser.get_float(name,default)
	   complex_attr = parser.get_complex(name,default)
	   string_attr  = parser.get_str(name,default)
 	   set_attr     = parser.get_set(name,default)
	   dict_attr    = parser.get_dict(name,default)
	   list_attr    = parser.get_list(name,default)
	   tuple_attr   = parser.get_tuple(name,default)
	   attr_repr    = parser.get_repr(name)
	   
	   new_attr  = parser.get_parser(attr_repr).rebuild()

	   # If name to method map has been populated with 
	   #        append_class_mapper()
	   new_attr  = parser.get_parser(class_name,attr_repr).rebuild()
	   ...
```
  