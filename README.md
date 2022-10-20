# reprbuild
## python3 library

Build recursive python representation without requiring modifcations to all class repr methods.

## Features

The goal of this library is to provide tools to build recursive representations that provide a single, unambiguous, authoritative representation of any variable within a system. Tools to build, parse, print and recreate an equivalent instance from the recursive representations are provided.

## Implementation
+ Define the class variable _repr_list as Union[list,dict] which defines the class attributes which are to be included in the representation. Optionally define _repr_list as a dict specify attribute namena maximum level. 
+ Update attribute name and maximum recursion level as desired
```
RECREATEMETHOD = "from_repr"
RECREATELIST + "_from_repr_map"
REPRLISTATTRIBUTE = "_repr_list"
MAXRECURSION = 200
```
+ Added the attributes to be included in the representation
```
   def __init__(self):
       ...
       self._repr_list = ["name","rank","serialnum"]
       self._from_repr_map = {
          "name" : NameClass.from_repr,
          "rank" : RankClass.from_repr,
          "serialnum" : SerialClass.from_repr
       }
```
+ Update or create method __repr__ to use build_repr method
```
def __repr__(self):
   return reprbuild.build_repr(self,self._repr_list)
```
+ Add the list of attributes to classes of any attributes included in the representation. The _repr_list is all that is required for the class to be included in the recursive representation.  The class' __repr__ method does not have to be modified/defined unless desired
+ Add the __str__ method if a nicely parsed and indented print of the representation is desired
## Print user readable representation
```
   def __str__(self):
      reprbuild.printrepr(build_repr(self)
```

## Build an equivalent instance from representation
+ Implement the from_repr() method for all attributes included in the recursive representation
+ Create a parser
+ If desired, add the from_repr() methods to the parser
```
   from reprbuild import ReprParser, parse_repr
   def from_repr(self,obj_repr)
       parser = ReprParse(obj_repr)
       parser.append_class_mapper(dict)
       parser.append_class_mapper(name,from_repr_method)
       
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
	   

	   attr_repr = parser.get_repr(name)
	   new_attr  = rebuild_method(attr_repr)

	   # If name to method map has been populated with 
	   #        append_class_mapper()
	   new_attr  = parser.rebuild(class_name,attr_repr)
	   ...
```
  