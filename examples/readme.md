# Directory with examples
## All examples are for Black ops 2 zombies, tested on a 4.84 DEX PS3
---

 PyPS3 allows multiple formats of bytes and addresses, for example;
 - `Memory().memWrite(proc, ['1CAF0D8', '1CAF138', '1CAF198'], '49FFFF')`
 - `Memory().memWrite(proc, '0x1CAF0D8', '0x49 0xFF 0xFF')`
 - `Memory().memWrite(proc, '0X1CAF0D8', '0X490XFF0XFF')`
 - `Memory().memWrite(proc, '0x1CAF0D8', '0x49, 0xFF, 0xFF')`