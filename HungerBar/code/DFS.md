```
FUNCTION threePartitionDFS(nums):
    total = SUM(nums)

    IF total % 3 ≠ 0 THEN
        RETURN FALSE, [], [], []
    END IF

    target = total / 3
    n = LENGTH(nums)

    // 排序以便更好的剪枝
    SORT(nums, DESCENDING)

    subsets = [ [], [], [] ]  // 三个子集
    sums = [0, 0, 0]         // 三个子集的当前和

    // DFS搜索
    FUNCTION backtrack(idx):
        IF idx == n THEN
            // 检查是否满足条件
            IF sums[0] == target AND sums[1] == target AND sums[2] == target THEN
                RETURN TRUE
            ELSE
                RETURN FALSE
            END IF
        END IF

        // 尝试将当前数字放入三个子集之一
        FOR subset_idx FROM 0 TO 2:
            // 剪枝：如果放入后超过目标值，跳过
            IF sums[subset_idx] + nums[idx] > target THEN
                CONTINUE
            END IF

            // 剪枝：如果前一个子集的和与当前子集相同，跳过重复情况
            IF subset_idx > 0 AND sums[subset_idx] == sums[subset_idx-1] THEN
                CONTINUE
            END IF

            // 选择当前子集
            APPEND nums[idx] TO subsets[subset_idx]
            sums[subset_idx] += nums[idx]

            // 递归
            IF backtrack(idx + 1) THEN
                RETURN TRUE
            END IF

            // 回溯
            REMOVE_LAST(subsets[subset_idx])
            sums[subset_idx] -= nums[idx]
        END FOR

        RETURN FALSE
    END FUNCTION

    IF backtrack(0) THEN
        RETURN TRUE, subsets[0], subsets[1], subsets[2]
    ELSE
        RETURN FALSE, [], [], []
    END IF
END FUNCTION
```
