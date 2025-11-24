```
FUNCTION threePartitionWithChoice(nums):
    total = SUM(nums)

    IF total % 3 ≠ 0 THEN
        RETURN FALSE, [], [], []
    END IF

    target = total / 3
    n = LENGTH(nums)

    // DP表记录是否可达
    dp = 2D_ARRAY[0..target][0..target] OF BOOLEAN
    // 选择表记录最后一步的选择
    choice = 2D_ARRAY[0..target][0..target] OF TUPLE(prev_i, prev_j, num_index, subset)

    INITIALIZE_ALL(dp, FALSE)
    INITIALIZE_ALL(choice, (-1, -1, -1, -1))

    dp[0][0] = TRUE

    // 处理每个数字
    FOR idx FROM 0 TO n-1:
        num = nums[idx]
        // 从后往前更新
        FOR i FROM target DOWNTO 0:
            FOR j FROM target DOWNTO 0:
                IF dp[i][j] THEN
                    // 放入第一个子集
                    IF i + num <= target AND NOT dp[i+num][j] THEN
                        dp[i+num][j] = TRUE
                        choice[i+num][j] = (i, j, idx, 1)
                    END IF

                    // 放入第二个子集
                    IF j + num <= target AND NOT dp[i][j+num] THEN
                        dp[i][j+num] = TRUE
                        choice[i][j+num] = (i, j, idx, 2)
                    END IF
                END IF
            END FOR
        END FOR
    END FOR

    // 回溯重构解
    IF dp[target][target] THEN
        subset1 = []
        subset2 = []
        subset3 = []
        used = ARRAY[n] OF BOOLEAN, INITIALIZE_ALL(FALSE)

        i = target
        j = target

        // 通过choice表回溯找到分配到子集1和2的数字
        WHILE i != 0 OR j != 0:
            (prev_i, prev_j, idx, subset) = choice[i][j]

            IF subset == 1 THEN
                APPEND nums[idx] TO subset1
                used[idx] = TRUE
                i = prev_i
            ELSE IF subset == 2 THEN
                APPEND nums[idx] TO subset2
                used[idx] = TRUE
                j = prev_j
            END IF
        END WHILE

        // 剩余的数字放入子集3
        FOR idx FROM 0 TO n-1:
            IF NOT used[idx] THEN
                APPEND nums[idx] TO subset3
            END IF
        END FOR

        RETURN TRUE, subset1, subset2, subset3
    ELSE
        RETURN FALSE, [], [], []
    END IF
END FUNCTION
```
