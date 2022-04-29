StructGen: Generate Data Structures for HPC Applications
========================================================

StructGen provides a language
to specify data structures at a high level.

Based on this specification it can generate:
a) C code to specify memory layout of the data structures,
b) Python helper routines for reading and writing these structures,
c) Java helper routines for reading and writing these structures,
d) MPI helper routines to move the data across MPI ranks,
e) OpenMP helper routines to move the data across NUMA nodes,
and f) CUDA helper routines to move the data to and from GPUs.

