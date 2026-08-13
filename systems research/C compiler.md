# Research Note #1

## Question: How does a C while-loop translate into x86 assembly?

**Background:** Minimal understanding of compiler output.

**Methodology:**

1. Develop a simple loop that increments a counter from 0 to 9 in C.
2. Compile the program using MSVC and targeting x86 architecture.
3. Generate a Portable Executable (PE).
4. Disassemble the PE using Ghidra.
5. Identify loop-related instructions.
6. Reconstruct control flow.
7. Compare source constructs to assembly output.

**Observations:**


Questions Generated:

Why was the variable placed on the stack?
What changes under optimization?
