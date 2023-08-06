CFLAGS := -I./include -Werror -Wall -fPIC -O2 $(CFLAGS)

ZLIB ?= y

ifneq ($(ZLIB),n)
    CFLAGS := -DCOMPRESSION $(CFLAGS)
    LDLIBS := -lz
endif

ifeq ($(SHARED),y)
    OS := $(shell uname -s)
    ifeq ($(OS),Darwin)
        CGADDAG := cgaddag.dylib
    else
        CGADDAG := cgaddag.so
    endif
else
    CGADDAG := cgaddag.a
endif

.PHONY: all
all: $(CGADDAG)

src/cgaddag.o: src/cgaddag.c include/cgaddag.h

cgaddag.a: src/cgaddag.o
	$(AR) -rcs $@ $^

cgaddag.so cgaddag.dylib: src/cgaddag.o
	$(CC) -shared $(LDFLAGS) -o $@ $^ $(LDLIBS)

example: src/example.o src/cgaddag.o
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

.PHONY: clean
clean:
	rm -f cgaddag.a cgaddag.so cgaddag.dylib src/cgaddag.o \
      example example.gdg example.gdg.gz src/example.o
