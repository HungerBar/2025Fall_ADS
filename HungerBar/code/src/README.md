
The three files `dfs.cpp`, `dp.cpp`, and `sa.cpp` correspond to solutions implemented using the **DFS algorithm**, **DP algorithm**, and **Simulated Annealing algorithm**, respectively. `check.cpp` is a correctness verification file; it checks whether the output in `output.txt` is valid, but it cannot determine if a feasible solution exists when none is found.

## Input/Output Format

We use File I/O: the program reads from `input.txt` and writes to `output.txt`.

The format of `input.txt` is as follows:
```
5
1 2 3 4 5
```
The first line is the total count of numbers, and the second line contains the specific numbers.

`output.txt` is the output file, which has two possible formats:

```
no
```

Or:

```
yes
1 4
2 3
5
````

**Note:** If the output is `yes`, it means a feasible solution has been found. If the output is `no`:
* For **DFS** and **DP** implementations, it means **no solution exists**.
* For the **Simulated Annealing** implementation, it means **no solution exists** OR **no solution was found within the time limit** (it does not necessarily imply the problem is unsolvable).

## Compilation and Execution Guide 

### Step 1: Compile all files

Please run the following commands in your terminal/command line:

**Windows:**

```bash
g++ dfs.cpp -o dfs.exe -O2
g++ dp.cpp -o dp.exe -O2
g++ sa.cpp -o sa.exe -O2
g++ check.cpp -o check.exe
````

**Mac / Linux:**

```bash
g++ dfs.cpp -o dfs -O2
g++ dp.cpp -o dp -O2
g++ sa.cpp -o sa -O2
g++ check.cpp -o check
```

*(Note: The `-O2` flag is used to enable optimization)*

### Step 2: Execution Flow

1.  **Generate Data**
    Manually create small test cases or use a program to generate large test cases in `input.txt`.

2.  **Run Solver (Choose one)**:
    The program will automatically read `input.txt` and generate `output.txt`.

<!-- end list -->

```bash
./dfs      # Run DFS

# OR

./dp       # Run DP

# OR

./sa       # Run Simulated Annealing
```

3.  **Verify Results**:
    The validator will check `input.txt` and `output.txt` to determine correctness.
    **Note:** If the output is `no`, the checker cannot judge whether the result is theoretically correct, as the original problem might have a solution that was simply not calculated within the limited time.

<!-- end list -->

```bash
./check
```

  * If it outputs `Correct`, the result is valid.
  * If it outputs `Wrong`, please check the content of `output.txt`.
  
**NOTE**:check.exe is just a simple program to check the correctness, for further test, refer to the test directory. 

<!-- end list -->
