Since the number of test files is large, this section briefly introduces each `.csv` result. For full details, see the report.




#### `dfs.csv`

- **`n`**: Number of elements (problem size)
- **`dfs_time`**: Runtime of the DFS algorithm (seconds)
- **`dfs_check`**: Correctness indicator (e.g., `Correct` or `"Correct(Output no, maybe wrong)"`)

In this test, **the number of elements `n` is varied**, while other conditions (algorithm implementation, hardware environment, input type, etc.) are kept fixed to observe DFS pruning performance at different scales.


#### `dp_fixedn_results.csv`

- **`n`**: Number of elements (problem size)
- **`total_sum`**: Total sum of the input array
- **`dp_time`**: Runtime of the dynamic programming algorithm (seconds)
- **`correct`**: Correctness indicator (True/False)

In this test, **the problem size is fixed at `n = 50`**, and the total sum `total_sum` is varied. All other conditions are kept the same to study how runtime changes with different total sums.

#### `dp_fixedsum_results.csv`

- **`n`**: Number of elements (problem size)
- **`total_sum`**: Total sum of the input array
- **`dp_time`**: Runtime of the dynamic programming algorithm (seconds)
- **`correct`**: Correctness indicator (True/False)

In this test, **the total sum `total_sum` is fixed**, and the problem size `n` is varied. Other conditions remain unchanged to observe how runtime scales with larger inputs.

#### `dpbase100.csv`

- **`n`**: Number of elements (problem size)
- **`sum`**: Total sum of the input array
- **`dp_time`**: Runtime of the dynamic programming algorithm (seconds)
- **`correct`**: Correctness indicator (True/False)

In this test, **each element is generated to be roughly around `base ≈ 100`**, while the problem size `n` varies. Other conditions remain fixed. The dataset is also used to **fit and verify the theoretical time complexity** of the DP algorithm.


#### `saBasetoBig.csv`

Records the performance of `./sa` on large inputs generated from base constructions.
If the solution is correct, the restart count is recorded; otherwise, `-1` is used.

#### `saGreedyFix.csv`

Records the performance of `./sa` on large inputs constructed using the greedy fill-in method.
If the solution is correct, the restart count is recorded; otherwise, `-1` is used.

