# Research Note #1

## Question: How does a C while-loop translate into x86 assembly?

**Background:** Minimal understanding of compiler output.

# C Assembly Investigation Notes
## Source Code
```c
#include <stdio.h>
int counter = 0;
for (int i = 0; i < 9; i++)
{
    counter++;
}
printf("Counter: %d\n", counter);
```
## Initial Observations

There is far more within the assembly that was compiled. This must be everything that c does in the background. I have found my main function (that I did not put, it was automatically created from the file I made) and within it I see two symbols, local_14 and local_18. It looks like Ghidra takes the local variables and labels them as such. By default, the compiler appears to wrap the function in an int main function returning 0. This maintains the invoke main process while not producing additional unexpected output. It looks like right below the function is the MOV dword ptr [RSP ( return something pointer?) + local_14], 0x0. 

This instruction seems to be resetting the PTR to 0? Or no, it is the other way around? But this is a pointer, so it is not referring to the value of the variable, but the location of it. Why would I want to add some value to the address of a variable? This is done for both the local_14 and local_18 variables. Is it return stack pointer? Is this a stack pointer? Is this instruction adding these variables to the stack? So the values of variables don't get added to the stack, but the address does? Let's say the RSP is 0x00 and the ptr for local_14 is 0x50 the result of adding the two pointers together would provide me with the address for the local_14 variable, now let's do the same for local_18, now we have the ptr for each variable and it is stored on the stack. 

Right above the first MOV we see a SUB RSP, 0x38, I am unaware of the SUB instruction but it looks like substitute, maybe some kind of copy instruction and we are taking the stack pointer and copying the value of 0x38 to it? This seems strange, Our memory address is 1400007560, I wonder if 0x38 is significant to this address. 0x38 in hexadecimal is 56, intriguing, but the value shown is 560, maybe the endianness has a significance here. 

In any case, we have identified that the stack pointer has been established as 56 then at 7564 we see the first MOV instruction, there's no empty space between these two instructions in memory. I recognize that there are 4 values between the two addresses and would assume that each value or code identifies the instruction, type information, and action, potentially. The 4 values are 48 83 ec 38, 48 could signify SUB, 83 could signify the RSP register, ec could signify....i have no current hypothesis, but 38 is the value we are storing in the register as it appears. I will quickly scan for another SUB instruction...

I found another SUB instruction that is 48 83 ec 28, so maybe it is the word that identifies the instruction so not 48 but 48 83 or 83 48 in little endian (I believe), then ec is the RSP register and 28 is the value to store in the register. I just realized something very significant…I only ever declared one variable, so what is local_14? Local_18 appears to be my counter variable judging by the decompilation from Ghidra. 

## Understanding `MOV`, Stack Offsets, and Local Variables

The MOV instruction is very perplexing. Intuitively, moving involves two items having a location set. In this case, it doesn’t make sense for there to be a set location. By my understanding, this instruction: MOV dword ptr [RSP + local_14], 0x0 is saying to take the address of the local variable plus the beginning of the stack and move it from 0x0. 

I scrolled to the very top of the assembly and noticed that there is a peculiar line that states “assume DF – 0x0 (Default)” does this mean that the move instruction is much more like a “Change” rather than traditional definitions of “move”. If that is the case, it makes sense, although, this begs the question, why does the pointer need a default location? Why can’t it just pop into existence without that? This could very well be due to the CPU architecture or underlying processes that are far beyond me, but it is an interesting note. 

I also see the address range that is allocated for this PE, it starts at 1400000000 and the headers end at 14000003ff. Within this range, there are many null bytes, likely from optional headers and fields that are not used for this application. I navigated to the .data section and identified the pointer to the raw data as 9A200h but adding 9A200h to 00000h did not result in the offset shown. The offset where .data actually is, 9B000h this means that the offset begins not at 0000h but at 0E00h, since 0E00h + 9A200h is 9b000h. This is even stranger, I attempted to navigate to 140000E00h but the headers section ends at 1400003ff and then the .text section begins at 140001000h. 

This means there is a large chunk of addresses that is seemingly missing. 

Even more interesting is that the entire program seems to have a large jump from 1400aalffh to ff00000000 for the “tbd” some sort of table structure, it appears. Continuing down the assembly, .text seems to have “Thunk functions”. From what I can gather, it seems these thunk functions are helper functions to determine when to call the primary functions, that is what it appears to be. It looks like they capture calls and route those calls to the proper embedded functions. I just found the Thunk function for printf, so I think my hypothesis is fairly accurate, when the printf function is called, it is captured by this thunk function and then used to jump to the printf function where it is stored in memory. Interesting. 

This function comes from the studio.h library… this must be why you must include that library for every application…but if that is the case, why isn’t it included in all compiled binaries automatically, just like how the compiler automatically seemed to add the main function when the PE was built. Maybe it is for compiler compatibility, it would not make sense for all compilers to include all base libraries for all compiled languages, so this keeps the solution scalable. That makes sense. Around 1400072b4h we see the first true function of int_cdecl pre_c_initialization(void) which looks like the c language is initializing the environment to run the program. Just as I noticed before, this function does not return a significant value, so it is labeled as an int function and returns 0. Offset 140007560h is where we find our main function. 

## Mapping Local Variables in Ghidra

We already identified that local_18 is our counter...but wait, we do initialize two variables technically, counter and I for the for loop. This means that local_14 and local_18 could be counter and I respectively. However, within the Ghidra decompile window, I notice that the first initialized variable, which is counter in our code, is labeled as local_18 and I which is within the for loop conditional, is also labeled as local_18. 

This is interesting because I would expect both of those variables to be flagged differently if they existed as individual entities. Perhaps this is not a compilation issue, but an issue with decompilation routines, where two variables that are initialized with the same value become indeterminate when decompiling. If that is the case, I would expect to see a divergence as the instructions progress to clearly identify which is the counter variable and which is the I variable. 

## Following the Loop in Assembly

After the two initial MOV instructions, there is a JMP instruction to “LAB_140007580” and I just realized that LAB seems to be a particular section of code that is denoted by its offset “7580”. 

Navigating a few addresses down to this offset reveals a CMP instruction as: CMP dword ptr [RSP+local_18], 0x9. Ah, we are comparing the value of the pointer stored at the address RSP + local_18 that we established earlier as the location of the local_18 variable pointer, but this address stores the data instead it seems. 

We are comparing this data to 0x9 or 9d and determining if they match. Below this we see JGE LAB_140007593 or a jump if greater than or equal to 9. This is our for loop. If this fails, there is no JMP and the instructions continue as MOV EAX,dword ptr[RSP+local_14]. 

It looks like we are storing the current value of the variable into the EAX register. The next instruction is INC EAX (presumably increment EAX), we then push that new value to the stack using the instruction MOV dword ptr [RSP+local_14],EAX taking the value of EAX and storing it on the stack at the pointer of our local_18 variable. This reveals that local_14 is actually the counter variable. 

Since we are within our for loop, we now need to return to the beginning and the instruction JMP LAB_140007576 does exactly that. This process continues until the instruction CMP dword ptr [RSP+local_18],0x9 evaluates to true and the JGE instruction is activated to jump to LAB_140007593. 

This jumps us past the remaining instructions and into a new routine. Here we have MOV EDX, dword ptr [RSP+local_14], now understanding the structure better, we are moving the value of local_14 located at ptr RSP+local_14 into the EDX register. This is the counter variable, and we can assume that we have moved onto the printf statement. 

The next instruction is LEA RCX, [s_Counter:%d_140084f40] and it has me utterly lost. 

I do not know the LEA instruction and the new RCX register is also confusing. I do see an offset in this instruction, so I will navigate to 140084f40h and see what is stored there. 

I located the offset and see ds “Counter: %d\n” so it appears the s at the beginning of s_Counter… is a string designator and the ds tag must also denote a string. From this, I am assuming that LEA is used to store the address of a string? Into a register. From my understanding, I would imagine this could be done with MOV dword ptr […. oh, but this string does not seem to be stored on the stack, since it is not a variable and simply a string within the application…that must be the difference. 

This must be why LEA is necessary, because there is no offset that you can add to RSP to get this data, instead you have to find it directly. After this instruction is a CALL printf instruction. This CALL leads us to the Thunk function which then jumps to the actual printf function, why this is not a direct call is not understood at this moment. 

I attempted to follow the printf call and it led me to a labyrinth of more function calls and new registers, for now, I shall stay within the confines of my function. 

Printf will then take all the available information and register values and eventually call the system to print to the stdout. I am starting to realize that LAB is just a way to say, these instructions go together in some way and there are jumps to here and away from here. 

For now I will mentally model them as Local Area Bounds sections. This let’s me know the instructions remain in the area but there are boundaries to them. After the printf call, we then have XOR EAX, EAX, xoring a value against itself will always result in 0’s so we are clearing the EAX register. 

We then ADD RSP,0x38 and then return with RET. This reminds me of the beginning of the function with SUB RSP,0x38 in which case, we are not substituting but subtracting 0x38 from RSP and now that we are done, we are adding it back. When we subtracted 56 bytes from the stack pointer, we made space to store our new variables, now that we are done with our function and those variables are no longer needed, we add those bytes back so the other offsets in the application can be accurate. Interestingly enough, analyzing other functions, I see this same pattern, subtract a number of bytes from the stack pointer and then add them back after you are done executing. That is incredible, this means that once the function returns, the parent function will still be able to use its predefined offsets. 

## Instruction Encodings

I now know that a loop is based on JMP instructions and CMP instructions, instead of incrementing a value, a while loop would likely just finish its block and then CMP the register value again to determine if it takes a JNE instruction. I also know that while the main wrapper is not necessary when developing, it is necessary for the compiler to function and so it is added if it is not present. I now see that for the x86 architecture of Windows C++ the instructions:

```asm
MOV     	dword ptr [RSP + local_14], 0x0
MOV     	dword ptr [RSP + local_18], 0x0
JMP       	LAB_140007580
```

Can be represented in binary with:

```text
C7 44 24 24 00 00 00 00
C7 44 24 20 00 00 00 00
EB 0A
```

The subtract instruction seems to be associated with 48 83

The RSP is associated with EC

And 38 is the value to subtract

The MOV instruction is where things get interesting, we are no longer dealing with the direct value of registers, but the pointers to store data in offsets. For instance:

C7 44 seems to be associated with the MOV instruction, however, the same MOV instruction further down (not shown) is 8B 44 24 20 and another is 89 44 24 20, if we put them all in a column:

```asm
C7 44 24 20 00 00 00 00           MOV dword ptr [RSP + local_18],0x0
8B 44 24 20                       MOV EAX, dword ptr [RSP + local_18]
89 44 24 20                       MOV dword ptr [RSP + local_18], EAX
```

In the first two, the MOV was the same, and only the variable changed. In the last two, the MOV was the same and the variables were the same, just flipped. If we analyze the two instructions, we see that what stayed the same was the 44 24 20 where as the first byte went from 8B to 89, this is very strange, because it appears from our perspective that two items changed in the instruction, but only one byte changed. Continuing down we see another set of instructions:

```asm
89 44 24 24    MOV dword ptr [RSP + local_14], EAX
```

Two things I noticed, since we are now dealing with local_14, there has been another change. The two instructions now end in 24, not 20 but maintain the 44 24 designations. I kept digging and found the following instruction:

```asm
B9 01 00 00 00		MOV ECX, 0x1
```

This instruction does not follow any of the conventions we were observing in the other instructions. There must be something I am missing. In this instruction we seem to be able to store both the instruction and the register within B9 or 10111001. It seems that the first byte is the instruction designation, but it might not be as simple as byte-level and may be bit-level. I will take all of the previous instructions and convert them to binary in a column:

```text
8B -> 10001011
89 -> 10001001
B9 -> 10111001
```

These all represent the MOV instruction but the only bit that is the same in all of them is the first bit.

Continuing my search, I found the following instruction:

```asm
41 8B 49 0C 		MOV param_1+0x4, dword ptr [R9 + 0xC]
```

Which again does not follow the first bit convention we were establishing. This is very interesting, either I am looking in the wrong spot or the instruction set is far more complicated than I first thought. 

## Conclusion

I will end this investigation here, I have successfully followed the assembly through execution of a basic for loop and print statement, I now have a deeper understanding of how the application achieves this in compiled form. 

