The `new` and `delete` operators in C++ are used for dynamic memory allocation and deallocation, respectively. They manage memory on the heap, allowing for the creation and destruction of objects at runtime. 

- **`new` Operator**: This operator allocates memory for an object or an array of objects of a specified type and returns a pointer to the beginning of the newly allocated memory. It also calls the constructor for the object if applicable. For example:
  ```cpp
  int* ptr = new int;         // Allocates memory for a single integer
  int* arr = new int[10];    // Allocates memory for an array of 10 integers
  ```

- **`delete` Operator**: This operator deallocates memory that was previously allocated with `new`. It also calls the destructor for the object if applicable. For example:
  ```cpp
  delete ptr;                // Deallocates memory for the single integer
  delete[] arr;              // Deallocates memory for the array of integers
  ```

Using `new` and `delete` is crucial for managing memory in C++ as it allows for more flexible memory usage compared to stack allocation. However, it's important to ensure that every call to `new` has a corresponding call to `delete` to prevent memory leaks.