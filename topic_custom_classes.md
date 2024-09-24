### 1. An instance of the Rectangle class requires length: int and width: int to be initialized.

### 2. We can iterate over an instance of the Rectangle class

### 3. When an instance of the Rectangle class is iterated over, we first get its length in the format {'length': <VALUE_OF_LENGTH>) followed by the width {width: <VALUE_OF_WIDTH>)

### Answer:
``` python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}
```
By using <mark>\_\_iter__</mark> method, we can iterate over an instance of Rectangle.
<mark>yield</mark> pauses the function after each call.

``` python
rectangle = Rectangle(5, 5)
for i in rectangle:
    print(i)
```

``` bash
# Output:
{'length': 5}
{'width': 5}
```
