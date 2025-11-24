```
FUNCTION threePartitionSymmetric(nums):
    total = SUM(nums)
    IF total % 3 ≠ 0: RETURN FALSE

    target = total / 3
    n = LENGTH(nums)

    // 排序以便更好的剪枝
    SORT(nums, DESCENDING)

    dp = 2D_ARRAY[0..target][0..target] OF BOOLEAN
    INITIALIZE_ALL(dp, FALSE)
    dp[0][0] = TRUE

    current_sum = 0
    FOR EACH num IN nums:
        current_sum += num

        // 利用对称性：假设i <= j
        FOR i FROM MIN(target, current_sum) DOWNTO 0:
            FOR j FROM MIN(target, current_sum - i) DOWNTO i:  // j >= i
                IF dp[i][j]:
                    IF i + num <= target:
                        dp[i + num][j] = TRUE
                    IF j + num <= target:
                        dp[i][j + num] = TRUE
                    // 第三个子集自动确定
                END IF
            END FOR
        END FOR

        // 提前终止检查
        IF dp[target][target]:
            RETURN TRUE
    END FOR

    RETURN dp[target][target]
END FUNCTION
```
