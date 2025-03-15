In C++, the `new` and `delete` operators are used for dynamic memory allocation and deallocation. They manage memory on the heap, allowing for the creation and destruction of objects at runtime.

- **`new` Operator**: This operator allocates memory for an object or array of objects of a specified type and returns a pointer to the beginning of the allocated memory. It initializes the object by calling the constructor if it is a class type.

  Example:
  ```cpp
  int* ptr = new int;          // Allocates memory for a single integer
  int* arr = new int[10];     // Allocates memory for an array of 10 integers
  ```

- **`delete` Operator**: This operator deallocates memory that was previously allocated with `new`. It calls the destructor for class types if necessary and frees the memory, making it available for future allocations.

  Example:
  ```cpp
  delete ptr;                 // Deallocates memory for the single integer
  delete[] arr;              // Deallocates memory for the array of integers
  ```

When using `new` and `delete`, it's important to match each `new` with a corresponding `delete` to prevent memory leaks, which occur when memory is allocated but not freed.