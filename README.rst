StructGen: Generate Data Structures for HPC Applications
========================================================

StructGen provides a language
to specify data structures at a high level.

Based on this specification it can generate:

1. C code to specify memory layout of the data structures,
2. Python helper routines for reading and writing these structures,
3. Java helper routines for reading and writing these structures,
4. MPI helper routines to move the data across MPI ranks,
5. OpenMP helper routines to move the data across NUMA nodes, and
6. CUDA helper routines to move the data to and from GPUs.

