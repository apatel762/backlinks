# Naive when generating back links

Say `[page B](pageB.html)` is appended to pageC.mdwn. Currently `make` will look through all *.mdwn files. This is inefficient.
