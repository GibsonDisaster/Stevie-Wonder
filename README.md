# Stevie-Wonder
A program for automatic file processing written in Python

## Flags
* -fe [file extension] (used to specify file extensions to watch)
```bash
-fe hs py c cpp
```
* -c [command] (used to specify the main command to run on input. Use %s as a substitute for file name)
```bash
 -c "ghc -o Example %s"
```
* -ce [extra commands] (used to specify setup commands for main command)
```bash
-ce "extra" "extra2" ...
```
* -jc [number] (used to specify specific number of times to react to inputs)
```bash
-jc 10
```
* -di (used to specify whether to delete input file when done process it)
```bash
-di
```