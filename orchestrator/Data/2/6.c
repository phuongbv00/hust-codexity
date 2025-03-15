The `new` and `delete` operators in C++ are used for dynamic memory allocation and deallocation. 

- **`new` Operator**: This operator is used to allocate memory on the heap for a variable or an array of variables at runtime. When you use `new`, it returns a pointer to the allocated memory. The memory allocated remains until it is explicitly released using `delete`.

  Example:
  ```cpp
  int* ptr = new int; // Allocates memory for a single integer
  int* arr = new int[10]; // Allocates memory for an array of 10 integers
  ```

- **`delete` Operator**: This operator is used to deallocate memory that was previously allocated using `new`. It's important to use `delete` to free up memory to prevent memory leaks.

  Example:
  ```cpp
  delete ptr; // Deallocates memory for a single integer
  delete[] arr; // Deallocates memory for an array of integers
  ```

Dynamic memory management with `new` and `delete` allows for more flexible memory use, as the size of the data can be determined at runtime, but it also requires careful management to avoid leaks and dangling pointers.