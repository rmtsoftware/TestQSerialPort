#ifndef _TEST_H_
#define _TEST_H_

#ifdef  __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <string.h>
#include <unistd.h>

unsigned char calculateChecksum(char *val);

#ifdef  __cplusplus
}
#endif

#endif  /* _TEST_H_ */