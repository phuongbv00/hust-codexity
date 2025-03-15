In C++, the `new` and `delete` operators are used for dynamic memory allocation and deallocation, respectively.

- **`new` Operator**: This operator allocates memory on the heap for a variable or an array of variables. When you use `new`, it returns a pointer to the beginning of the allocated memory block. For example:
  ```cpp
  int* p = new int; // Allocates memory for a single integer
  int* arr = new int[10]; // Allocates memory for an array of 10 integers
  ```

- **`delete` Operator**: This operator frees the memory that was previously allocated with `new`. It ensures that the allocated memory is returned to the system, preventing memory leaks. For single objects, you use `delete`, and for arrays, you use `delete[]`. For example:
  ```cpp
  delete p; // Deallocates memory for a single integer
  delete[] arr; // Deallocates memory for an array of integers
  ```

The `new` operator also calls the constructor of the object being allocated, if applicable, while the `delete` operator calls the destructor. Proper use of `new` and `delete` is essential for managing dynamic memory effectively, and failing to pair them correctly can lead to memory leaks or undefined behavior.