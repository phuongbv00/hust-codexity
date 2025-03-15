In C++, the `new` and `delete` operators are used for dynamic memory allocation and deallocation, respectively. 

- **`new` Operator**: It allocates memory on the heap for a variable or array of variables. When you use `new`, it returns a pointer to the allocated memory. If you allocate memory for a single object, it constructs the object and returns a pointer to it. If you allocate memory for an array, it allocates enough space for the entire array and returns a pointer to the first element.

Example:
```cpp
int* ptr = new int; // Allocates memory for a single integer
int* arr = new int[10]; // Allocates memory for an array of 10 integers
```

- **`delete` Operator**: It is used to deallocate memory that was previously allocated with `new`. When you use `delete`, it destroys the object and frees the memory back to the system. There are two forms of `delete`: `delete` for single objects and `delete[]` for arrays.

Example:
```cpp
delete ptr; // Deallocates memory for the single integer
delete[] arr; // Deallocates memory for the array of integers
```

The `new` and `delete` operators manage dynamic memory allocation by allowing the programmer to control memory usage more flexibly than with automatic (stack) allocation. However, it is important to ensure that every `new` has a corresponding `delete` to prevent memory leaks, as memory allocated with `new` remains allocated until it is explicitly deallocated with `delete`.