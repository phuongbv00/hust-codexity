In C++, the `new` and `delete` operators are used for dynamic memory allocation and deallocation, respectively.

1. **`new` Operator**: The `new` operator allocates memory on the heap for a single object or an array of objects and returns a pointer to the beginning of the newly allocated memory. It also calls the constructor of the object if it is a class type. The syntax can be as follows:
   - For a single object: `Type* ptr = new Type;`
   - For an array of objects: `Type* ptr = new Type[size];`

2. **`delete` Operator**: The `delete` operator is used to deallocate memory that was previously allocated with `new`. It also calls the destructor of the object if it is a class type. The syntax can be:
   - For a single object: `delete ptr;`
   - For an array of objects: `delete[] ptr;`

Dynamic memory management with `new` and `delete` allows for more flexible memory usage compared to static or automatic allocation, enabling the allocation of memory based on the program's needs during runtime. However, it is crucial to manage memory properly to avoid memory leaks, which occur when allocated memory is not deallocated.