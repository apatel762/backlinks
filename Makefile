INFILES     := $(shell find . -name "*.md")
OUTFILES    := $(INFILES:.md=.html)
LINKFILES   := $(INFILES:.md=.bl)

.PHONY: all clean test
.PRECIOUS: $(LINKFILES)

all: $(OUTFILES)

# These need to be all made before the HTML is processed
%.bl: $(INFILES)
	@echo Creating backlinks
	@touch $(LINKFILES)
	@for m in $^; do go run backlinks.go $$m; done

%.html: %.md %.bl
	@echo Deps $^
	@cmark $^ > $@

test:
	@for i in *.html; do diff $$i test/$$i; done

clean:
	rm -f *.bl *.html
