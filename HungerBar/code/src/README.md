
# Project 5: Three Partition - Code & Algorithms

## Project Overview

This project implements **3 different types of algorithms** to solve the **3-Partition Problem**. The goal is to determine if a set of $N$ integers can be partitioned into three subsets with equal sums.

### Files Description
* **`dfs.cpp`**: **Depth First Search** (Exact). Uses strong pruning strategies. Suitable for small $N$ ($N \le 60$) or specific hard cases.
* **`dp.cpp`**: **Dynamic Programming** (Exact). Runs in pseudo-polynomial time. Efficient for large $N$ but small numeric sums.
* **`sa.cpp`**: **Simulated Annealing** (Heuristic). A randomized algorithm with incremental computation and restart strategy. Best for large-scale data ($N=1000$) and high-dimensional variants (Bonus).



## Input/Output Format

The solvers support **File I/O**.

### Input Format (`input.txt` or `*.in`)
```text
5
1 2 3 4 5
````

  * Line 1: The total count of numbers $N$.
  * Line 2: The $N$ specific integers.

### Output Format (`output.txt` or `*.out`)

**Case 1: Solution Found**

```text
yes
1 4
2 3
5
```

  * Line 1: `yes`.
  * Lines 2-4: The numbers belonging to the three subsets (order does not matter).

**Case 2: No Solution**

```text
no
```

  * For **DFS/DP**: It strictly means no solution exists.
  * For **SA**: It means no solution was found within the time limit (though one might exist).

-----

## 4\. Compilation & Execution

We use standard `g++`. Please ensure you have a C++ compiler installed.

### Step 1: Compile

Run the following commands in your terminal:

**Windows:**

```powershell
g++ dfs.cpp -o dfs.exe -O2
g++ dp.cpp -o dp.exe -O2
g++ sa.cpp -o sa.exe -O2
```

**Mac / Linux:**

```bash
g++ dfs.cpp -o dfs -O2
g++ dp.cpp -o dp -O2
g++ sa.cpp -o sa -O2
```

*(Note: `-O2` optimization is highly recommended)*

### Step 2: Execution Modes

#### Default

Reads from `/testcase/1.in` and writes to `/testcase/1.out`.

Run the solver

    
    ./sa      # (or ./dfs, ./dp)
    

#### Testcase (`-test`)

Reads from a specific test case file and writes to the corresponding output file.
**Note:** The code assumes test cases are located in `../../testcase/`.

  * **Syntax**: `./solver -test <name>`
  * **Example**: To run test case `1`:
    ```bash
    ./sa -test 1
    ```
      * **Input Path**: `../../testcase/1.in`
      * **Output Path**: `../../testcase/1.out`




<!-- end list -->
