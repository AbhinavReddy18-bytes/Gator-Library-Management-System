# Define the Python interpreter
PYTHON = python3

# Define the script and input file
SCRIPT = gator_library_code.py
INPUT = inputs.txt

# Default target
all: run

# Target to run the Python script
run: $(SCRIPT)
\t$(PYTHON) $(SCRIPT) < $(INPUT)


