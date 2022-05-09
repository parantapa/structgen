from cffi import FFI
from hello_cffi_decl import CDEF_SOURCE, SET_SOURCE_C_HEADER_SOURCE

ffibuilder = FFI()
ffibuilder.cdef(CDEF_SOURCE)
ffibuilder.set_source("_hello", SET_SOURCE_C_HEADER_SOURCE, sources=["hello.c"])


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
