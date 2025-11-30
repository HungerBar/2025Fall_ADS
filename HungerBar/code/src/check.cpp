#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cctype>

#define MAX_N 10000
#define MAX_LINE_LEN 65536

int input_nums[MAX_N];
int output_nums[MAX_N];
int input_count = 0;
int output_count = 0;

int compare(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

int is_yes(const char* str) {
    return (str[0] == 'y' || str[0] == 'Y');
}
int is_no(const char* str) {
    return (str[0] == 'n' || str[0] == 'N');
}

int main() {
    FILE *fin = fopen("input.txt", "r");
    if (!fin) {
        printf("Error: input.txt missing\n");
        return 1;
    }

    int N;
    if (fscanf(fin, "%d", &N) != 1) return 1;

    long long input_sum = 0;
    for (int i = 0; i < N; i++) {
        fscanf(fin, "%d", &input_nums[i]);
        input_sum += input_nums[i];
    }
    input_count = N;
    fclose(fin);

    FILE *fout = fopen("output.txt", "r");
    if (!fout) {
        printf("Error: output.txt missing\n");
        return 1;
    }

    char buffer[MAX_LINE_LEN];
    // 读取第一行状态 
    if (fscanf(fout, "%s", buffer) != 1) {
        printf("Wrong (Empty)\n");
        return 0;
    }

    // 情况 A: 输出 no
    if (is_no(buffer)) {
        printf("Correct(Output no, maybe wrong)\n"); // 暂时认为 no 是对的
        fclose(fout);
        return 0;
    }

    // 情况 B: 输出 yes
    if (!is_yes(buffer)) {
        printf("Wrong (Format error)\n");
        fclose(fout);
        return 0;
    }

    // 如果 sum 不能被 3 整除，绝对不可能 Yes
    if (input_sum % 3 != 0) {
        printf("Wrong (Impossible Sum)\n");
        fclose(fout);
        return 0;
    }
    long long target = input_sum / 3;

    // 消耗掉 "yes" 后面的换行符，以便 fgets 能读到下一行
    fgets(buffer, MAX_LINE_LEN, fout); 

    // 读取接下来的 3 行
    int lines_read = 0;
    while (lines_read < 3 && fgets(buffer, MAX_LINE_LEN, fout)) {
        // 跳过只包含空白的行
        int is_empty = 1;
        for(int k=0; buffer[k]; k++) {
            if(!isspace(buffer[k])) { is_empty = 0; break; }
        }
        if(is_empty) continue;

        long long current_row_sum = 0;
        
        // 使用 strtok 切割空格
        char *token = strtok(buffer, " \t\r\n");
        while (token != NULL) {
            int val = atoi(token);
            current_row_sum += val;
            
            if (output_count < MAX_N) {
                output_nums[output_count++] = val;
            }
            token = strtok(NULL, " \t\r\n");
        }

        if (current_row_sum != target) {
            printf("Wrong (Row sum mismatch: Expected %lld, Got %lld)\n", target, current_row_sum);
            fclose(fout);
            return 0;
        }
        lines_read++;
    }

    fclose(fout);

    if (lines_read < 3) {
        printf("Wrong (Missing lines)\n");
        return 0;
    }

    // 核心校验：对比两个数组是否一致

    if (input_count != output_count) {
        printf("Wrong (Count mismatch)\n");
        return 0;
    }

    // 排序
    qsort(input_nums, input_count, sizeof(int), compare);
    qsort(output_nums, output_count, sizeof(int), compare);

    // 逐个比对
    for (int i = 0; i < input_count; i++) {
        if (input_nums[i] != output_nums[i]) {
            printf("Wrong (Numbers mismatch)\n");
            return 0;
        }
    }

    printf("Correct\n");
    return 0;
}