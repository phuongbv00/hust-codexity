In C++, the `new` and `delete` operators are used for dynamic memory allocation and deallocation, respectively.

- **`new` Operator**: This operator allocates memory on the heap for a specified type and returns a pointer to the first byte of the allocated memory. It can also call the constructor of the object being created if the type is a class. The syntax is:

  ```cpp
  Type* ptr = new Type; // for a single object
  Type* arr = new Type[size]; // for an array of objects
  ```

- **`delete` Operator**: This operator deallocates the memory that was previously allocated with `new`. It also calls the destructor of the object if the type is a class. The syntax is:

  ```cpp
  delete ptr; // for a single object
  delete[] arr; // for an array of objects
  ```

Dynamic memory allocation allows for more flexible memory management than automatic (stack) allocation, as it enables developers to allocate memory at runtime based on the needs of the program. It's crucial to use `delete` to free memory allocated with `new` to prevent memory leaks.