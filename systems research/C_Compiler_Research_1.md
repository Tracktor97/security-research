# Following a C Program into Assembly: An Exploratory Reverse-Engineering Study

*A personal investigation into how a simple loop and print statement become stack operations, jumps, registers, and runtime behavior.*
## Overview
This exploratory research began with a small C program and a much larger question: what actually happens after the code is compiled? I started with a simple counter loop and a print statement, expecting the compiled output to be straightforward. Instead, the assembly revealed stack setup, local variables, jump labels, thunk functions, register movement, and instruction encodings that made the program feel much larger than the source code suggested.
What I wanted to preserve in this investigation was not just the answer, but the process of discovery. A lot of the value came from asking imperfect questions, forming hypotheses, correcting them, and slowly building a mental model of how the C source translated into executable behavior.
## Starting Point: The Source Code
The source program was intentionally minimal:
```c
#include <stdio.h>
int counter = 0;
for (int i = 0; i < 9; i++)
{
    counter++;
}
printf("Counter: %d\n", counter);
```
At the source level, this program only declares a counter, runs a loop nine times, increments the counter, and prints the result. My expectation was that the compiled form would map closely to those steps. The assembly showed me that the compiled program includes much more structure than the source code immediately suggests.
## Research Questions
- How does a simple C loop appear in compiled x86-64 assembly?
- How are local variables represented on the stack?
- What do instructions like **SUB**, **MOV**, **CMP**, **JMP**, **JGE**, **LEA**, and **CALL** contribute to the program’s execution?
- Why does the compiled binary contain runtime setup, thunk functions, and other structures beyond the source code I wrote?
- How much can I infer from instruction bytes before needing a deeper understanding of the x86 instruction format?
## Method
I used Ghidra to inspect the compiled binary and followed the program from the decompiled view into the assembly listing. I focused on the function that corresponded to my source program, then traced the instructions from stack setup through the loop, the print call, and the function return.
My approach was intentionally exploratory. I wrote down what I thought each instruction meant, checked that interpretation against later instructions, and revised my assumptions when the assembly contradicted me. That mattered because the investigation was not only about identifying the correct answer; it was about learning how to reason through unfamiliar low-level behavior.
## Key Findings
### 1. The compiler creates a runtime context around the code
One of the first surprises was that the binary contained more than the small program I wrote. The compiled output included startup routines, initialization functions, thunk functions, and a structured entry point. I initially saw this as the compiler “adding” a main function, but the more important realization was that my source code exists inside a larger runtime environment that prepares the process, calls into my function, and handles library interactions.
The presence of thunk functions was especially interesting. When I followed the call to **printf**, I saw that it did not behave like a direct jump into a simple printing routine. Instead, it routed through additional layers. My working model became that these thunk functions help route calls to the appropriate imported function location. I may not have understood every layer yet, but identifying that indirection helped me stop expecting the binary to be a one-to-one expansion of my source code.
### 2. Stack space is reserved before local variables are used
A major turning point came from the instruction **SUB RSP, 0x38**. At first, I questioned whether “SUB” meant substitute or some kind of copy operation. Eventually, the matching **ADD RSP, 0x38** near the end of the function made the pattern clear: the function subtracts from the stack pointer to reserve stack space, then adds the same amount back before returning.
This was one of the most useful discoveries in the investigation. The stack pointer is not just an abstract register; it is part of how the function creates a temporary working area. Once the function is done, the stack pointer is restored so the caller’s expected layout remains intact.
### 3. Local variables appear as stack offsets
Ghidra labeled two locals as **local_14** and **local_18**. At first, this confused me because I had only explicitly declared one variable, **counter**. Then I realized that the loop variable **i** is also created by the source code, even though it appears inside the loop declaration. That helped explain why two local values appeared in the assembly.
The instructions using **[RSP + local_14]** and **[RSP + local_18]** showed me that the locals were being accessed through offsets from the stack pointer. Over time, I concluded that **local_14** corresponded to the counter and **local_18** corresponded to the loop index. This mattered because it showed how source-level variable names disappear during compilation and are reconstructed by analysis tools as stack locations.
### 4. The loop becomes comparison and jump logic
The for loop became much clearer once I identified the comparison and jump pattern. The instruction **CMP dword ptr [RSP + local_18], 0x9** compares the loop index against 9. The following **JGE** instruction jumps out of the loop when the index is greater than or equal to 9. If the jump is not taken, execution continues through the body of the loop.
The body of the loop reads the counter value from the stack, increments it, writes it back, then updates the loop index and jumps back to the comparison. That sequence changed how I understood loops. At the source level, a loop feels like a single language construct. At the assembly level, it is a combination of comparison, conditional jump, mutation, and unconditional jump.
### 5. The print statement uses registers and an imported function call
After the loop condition succeeds, execution moves into the print setup. I observed the counter value being moved into **EDX**, followed by an **LEA RCX** instruction that referenced the string **"Counter: %d\n"**. This helped me understand that the format string was not treated like a stack variable. It existed elsewhere in the binary, and the program loaded its address before calling **printf**.
I did not fully chase the complete internals of **printf**, because following that call quickly led into a much larger set of runtime and library functions. For this investigation, I intentionally stayed within the boundary of my own function and treated the print call as the point where my code handed work off to the runtime environment.
### 6. Instruction bytes are more complex than a direct one-byte mapping
I also began comparing machine-code bytes to assembly instructions. For example, I saw patterns like:
- **48 83 EC 38** for **SUB RSP, 0x38**
- **C7 44 24 24 00 00 00 00** for moving 0 into one stack local
- **8B 44 24 20** and **89 44 24 20** for moving between memory and a register
- **B9 01 00 00 00** for **MOV ECX, 0x1**
At first, I wanted to find a simple byte-level rule, as if one byte always represented the instruction and another byte always represented the register. That assumption broke down quickly. Several instructions were all displayed as **MOV**, but their byte patterns were different depending on the operands, direction, addressing mode, and register usage. This was an important limit to discover: the instruction set is not simple enough to infer from one repeated pattern.
## Reflections
The strongest part of this investigation was the process of repeatedly being wrong in useful ways. I misread **SUB**, questioned the purpose of stack offsets, confused pointer-like notation with the value being stored, and tried to reduce instruction bytes into a pattern that was too simple. Each incorrect assumption forced me to look at nearby instructions and revise the model.
By the end, I had a clearer understanding of several core ideas: stack allocation, local-variable offsets, loop control through jumps, register use for function calls, and the existence of runtime layers around imported functions. More importantly, I gained confidence in my ability to navigate unfamiliar assembly without needing to understand every symbol immediately.
This is the part of the work that feels most portfolio-worthy to me: it shows not only what I learned, but how I learn. I approached the binary with curiosity, documented my uncertainty, tested hypotheses against evidence, and refined my understanding through close reading of the compiled output.
## Takeaway
A simple C program can produce a surprisingly rich compiled structure. What appears as a counter, a loop, and a print statement at the source level becomes stack-frame setup, memory offsets, register movement, comparisons, conditional jumps, imported function calls, and cleanup. Following that transformation gave me a more concrete understanding of how high-level code becomes executable behavior.
I am ending this phase of the investigation with a better mental model of the compiled program and a clearer sense of what I still need to study next: x86-64 instruction encoding, calling conventions, PE file layout, and the runtime path behind imported functions such as **printf**. The investigation did not answer every question, but it gave me a stronger foundation for asking better ones.
