# py_functions
Python library that takes in a list/tuple and returns a hash map with an element:count of element in the list/tuple as a key:value pair

<h1><a href="/">py_counter</a></h1>

<br><b>DESCRIPTION:</b><br>
<p>
py_counter is used to make element counting easier to perform duplicate element finding, or simply count of elements(integers or strings) in a list/tuple easier.
</p>


<br><b>USAGE:</b><br>
import package name <br>
Create an instance of the class and assign it to a variable<br>
Call the counter method referencing the variable instance that we created by passing a list or tuple as parameter. <br>

<br><b>SYNTAX:</b><br>
```
import py_counter
variable_name = py_counter.py_counter()
print(variable_name.counter([list])) (or)
print(variable_name.counter([list]))
```

<br><b>EXAMPLE CODE:</b><br>
  
```
import py_counter
word = py_counter.py_counter()
print(word.counter([1,2,3,4,5,5]))
```
