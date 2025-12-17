EXEC = main

$(EXEC): src/main.cpp
	g++ -o $@ $^



install-deps:
	mkdir -p lib

	curl 
.PHONY: install-deps




clean:
	rm -f $(EXEC)
.PHONY: clean
