#include <stdio.h>

#include "hello.h"

int main(int argc, char *argv[]) {
  struct soc_int si;
  soc_int_malloc(&si, 100);

  soc_int_zero(&si);
  for (size_t i = 0; i < si.capacity; i++) {
    si.pid[i] = i;
  }
  si.size = si.capacity;

  soc_int_write_csv(&si, stdout);

  soc_int_free(&si);
  return 0;
}
