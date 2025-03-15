The `new` and `delete` operators in C++ are used for dynamic memory allocation and deallocation, respectively. 

1. **Purpose of `new`:** 
   - The `new` operator allocates memory on the heap for a variable or an array and returns a pointer to the beginning of that memory block. 
   - It can also invoke constructors for object types, ensuring that the objects are properly initialized.

2. **Purpose of `delete`:**
   - The `delete` operator deallocates memory that was previously allocated with `new`, freeing up that memory for future use.
   - It also invokes the destructor for object types, ensuring that any cleanup required is performed.

**Dynamic Memory Management:**
- When you use `new`, you can allocate memory whose lifetime is controlled manually. Unlike stack allocation, which is automatically managed, heap allocation persists until explicitly deallocated.
- If memory allocated with `new` is not freed with `delete`, it leads to memory leaks, which can exhaust the available memory over time.

**Example:**
```cpp
int* myArray = new int[10]; // Allocates an array of 10 integers
// Use the array
delete[] myArray; // Deallocates the memory
```

In this example, `new` allocates memory for an array of 10 integers, and `delete[]` is used to deallocate that memory. For single objects, you would use `new Type` and `delete` instead of `new[]` and `delete[]`.