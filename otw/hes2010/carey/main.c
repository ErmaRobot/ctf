/* gcc -O0 -fno-stack-protector main.c */
#include <stdio.h>
#define ERRORFILE "/home/scott/bin/errormessage"

void showfile(char *file) {
    FILE *in;
    char buf[80];

    in = fopen(file, "r");
    if(!in) exit(1);

    while(fgets(buf, 80, in)) {
        printf("%s", buf);
    }

    fclose(in);
}

unsigned int master_canary;

struct canary_t {
    unsigned int _align;
    unsigned int canary;
};

int main(int argc, char **argv) {
    struct canary_t c;
    char *errorfile = ERRORFILE;
    unsigned int counter = 1000000000;
    char buffer[80];
    int i;
    FILE *in;

    /* setup some protection */
    if((in = fopen("/dev/urandom", "r"))) {
	fread(&master_canary, sizeof(master_canary), 1, in);
	fclose(in);
    } else {
	exit(1);
    }

    c.canary = master_canary;

    while(counter) {
        if(!gets(buffer)) return 0;

        if(master_canary != c.canary) {
            printf("Security breached !\n");
	    exit(1);
        }

	/* perform rot 13 */
	for(i = 0; i < sizeof(buffer); i++) {
	    if(buffer[i] >= 'a' && buffer[i] <= 'z') {
		buffer[i] = ((buffer[i] - 'a' + 13) % 26) + 'a';
	    }
	    if(buffer[i] >= 'A' && buffer[i] <= 'Z') {
		buffer[i] = ((buffer[i] - 'A' + 13) % 26) + 'A';
	    }
	}

	/* print coded text */
	buffer[sizeof(buffer) - 1] = '\0';

	if(!strcmp(buffer, "debug")) {
	    printf("%d %p %p %p %p\n", counter, buffer, &counter, &errorfile, errorfile);
	}
	printf("%s\n", buffer);

        //counter--; /* commented out, we don't want the loop to end */
    }

    /* if we get to this point, something went wrong so print a standard error message */
    showfile(errorfile);
    return 0;
}
