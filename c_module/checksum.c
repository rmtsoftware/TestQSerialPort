#include "checksum.h"

unsigned char 
calculateChecksum(char *sentence){
    unsigned char checksum = 0;
    int i;
    for (i = 2; sentence[i] != '*'; i++) {
        checksum ^= sentence[i];
    }
    return checksum;
}
