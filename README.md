# reprbuild
## python3 library

Build recursive python representation without requiring modifcations to underlying \_\_repr\_\_ methods.

## Features

The goal of this library is to provide tools to build recursive representations that provide a single, unambiguous, authoritative representation of any variable within a system. Tools to build, parse, print and recreate an equivalent instance from the recursive representations are provided.

## Includes
+ **ReprParser(obj,rebuilder_map)**: class for parsing, printing and rebuilding from representations
+ **ReprParser().summary**: property holding the summary string for the object
+ **ReprParser().print()**: method for print a formatted version of the representation
+ **ReprParser().format_repr()**: method to return a formatted version of the representation
+ **ReprParser().build()**: method to recreate and return a new instance of the object specified (by representation, name, or self by default

+ **build_repr**: method for creating a recursive representation string
+ **print_repr**: method for printing a formatted version of the representation string

## Implementation
+ Update the constants for list name, rebuild method and maximum recursion as desired 
```
REPRATTRIBUTES = "_repr_attrs"
MAXRECURSION = 200
REBUILDER = "rebuild"

```
+ Configure _repr_attrs as Union[list,dict] to configure the attributes to be included in the representation. Optionally define _repr_list as a dict specify maximum recusion level by attribute. 
+ If desired, configure _repr_attrs for any recursively included classes.   The recursively included class method \_\_repr\_\_ does not have to be modified/defined unless desired

```
   def __init__(self):
       ...
       # Define a list with attribute names
       self._repr_attrs = ["name","rank","serialnum"]
       
       # to set specfic recursion levels define a dictionary
       self._repr_attrs = {"name":-1,"rank": 2, "serialnum": 1}
       
   @classmethod
   def get_build_map():
      # Define a dictionary mapping class name to rebuild methods if
      # object recreation is to be implemented
      return {
          "name" : NameClass.rebuild,
          "rank" : RankClass.rebuild,
          "serialnum" : SerialClass.rebuild
       }
      
```
+ Configure methods \_\_repr\_\_ and/or \_\_str\_\_ as desired
```
def __repr__(self):
   custom_summary = f"display at start of representation {my_attrs}
   return reprbuild.build_repr(self,self._repr_attrs,summary=custom_summary)
   
def __str__(self):
   return format_repr(reprbuild.build_repr(self,self._repr_attrs))

```

## Print an unformatted representation
```
   obj = myClass()
   obj
```

## Print user readable representation
```
   # If __str__ has been implemented
   obj = myClass()
   print(obj)
   
   # Without a configured __str__
   print_repr(obj)
   #     or
   ReprParser(obj).print()
   
   # Just the summary from the representation
   print(ReprParse(obj).summary)
```

## Build an equivalent instance from representation
+ Implement the rebuild() method for all attributes included in the recursive representation
+ Create a parser and pass it class_name to rebuild method dictionary
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
	   
	   
	   new_obj = parser.rebuild()
	   
	   # Rebuild specific attributes from their embedded representations
	   new_attr  = parser.rebuild(attr_repr)
	   
	   # Or rebuild specific attributes by name
	   new_attr  = parser.rebuild('name')
	   ...
```
  