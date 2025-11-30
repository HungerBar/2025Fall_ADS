#include <iostream>
#include <cstdlib>
#include <cmath>
#include <ctime>
#include <fstream>
#include <algorithm> 
#include <cstring> // for strcmp
#include <cstdio>  // for sprintf

using namespace std;

// 这里 K=3 做基础任务，改成 4, 5... 可以做 Bonus
const int K = 3; 
const int MAX_N = 10005;

int N;
int numbers[MAX_N];
int belong_to[MAX_N]; 
long long bucket_sum[K]; 
long long target;
bool found = false;

long long get_diff() {
    long long diff = 0;
    for (int i = 0; i < K; i++) {
        long long d = bucket_sum[i] - target;
        diff += (d > 0 ? d : -d);
    }
    return diff;
}

void sa() {
    // 重置桶的状态
    for (int i = 0; i < K; i++) bucket_sum[i] = 0;

    // 随机初始化
    for (int i = 0; i < N; i++) {
        belong_to[i] = rand() % K;
        bucket_sum[belong_to[i]] += numbers[i];
    }

    double T = 5000.0;     
    double alpha = 0.99;  
    double end_T = 1e-4;   

    long long cur_diff = get_diff();

    while (T > end_T) {
        if (cur_diff == 0) {
            found = true;
            return;
        }

        int op = rand() % 2; 

        if (op == 0) { 
            // 移动操作
            int idx = rand() % N;
            int old_b = belong_to[idx];
            int new_b = rand() % K;
            
            if (old_b == new_b) continue;

            long long old_e = abs(bucket_sum[old_b] - target) + abs(bucket_sum[new_b] - target);
            
            bucket_sum[old_b] -= numbers[idx];
            bucket_sum[new_b] += numbers[idx];
            
            long long new_e = abs(bucket_sum[old_b] - target) + abs(bucket_sum[new_b] - target);
            long long next_diff = cur_diff - old_e + new_e;

            if (next_diff < cur_diff || exp((cur_diff - next_diff) / T) > (double)rand() / RAND_MAX) {
                cur_diff = next_diff;
                belong_to[idx] = new_b;
            } else {
                bucket_sum[old_b] += numbers[idx];
                bucket_sum[new_b] -= numbers[idx];
            }
        } else {
            // 交换操作
            int i1 = rand() % N;
            int i2 = rand() % N;
            if (belong_to[i1] == belong_to[i2]) continue;

            int b1 = belong_to[i1];
            int b2 = belong_to[i2];

            long long old_e = abs(bucket_sum[b1] - target) + abs(bucket_sum[b2] - target);

            bucket_sum[b1] -= numbers[i1]; bucket_sum[b1] += numbers[i2];
            bucket_sum[b2] -= numbers[i2]; bucket_sum[b2] += numbers[i1];

            long long new_e = abs(bucket_sum[b1] - target) + abs(bucket_sum[b2] - target);
            long long next_diff = cur_diff - old_e + new_e;

            if (next_diff < cur_diff || exp((cur_diff - next_diff) / T) > (double)rand() / RAND_MAX) {
                cur_diff = next_diff;
                int tmp = belong_to[i1];
                belong_to[i1] = belong_to[i2];
                belong_to[i2] = tmp;
            } else {
                bucket_sum[b1] -= numbers[i2]; bucket_sum[b1] += numbers[i1];
                bucket_sum[b2] -= numbers[i1]; bucket_sum[b2] += numbers[i2];
            }
        }
        T *= alpha;
    }
}

int main(int argc, char* argv[]) {
    srand(time(NULL));

    // 默认路径
    char input_path[256] = "../../testcase/1.in";
    char output_path[256] = "../../testcase/1.out";

    // 解析命令行参数
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-test") == 0) {
            if (i + 1 < argc) {
                // 根据参考路径修改：../../testcase/x.in
                sprintf(input_path, "../../testcase/%s.in", argv[i+1]);
                sprintf(output_path, "../../testcase/%s.out", argv[i+1]);
                i++; // 跳过参数值
            } else {
                cerr << "Error: -test option requires an argument." << endl;
                return 1;
            }
        }
    }

    ifstream fin(input_path);
    ofstream fout(output_path);

    if (!fin.is_open()) {
        cerr << "Error: Cannot open input file: " << input_path << endl;
        return 1;
    }
    if (!fout.is_open()) {
        cerr << "Error: Cannot open output file: " << output_path << endl;
        return 1;
    }

    if (!(fin >> N)) return 0;

    long long sum = 0;
    for (int i = 0; i < N; i++) {
        fin >> numbers[i];
        sum += numbers[i];
    }

    if (sum % K != 0) {
        fout << "no" << endl;
        fin.close(); fout.close();
        return 0;
    }

    target = sum / K;
    for(int i = 0; i < N; i++) {
        if(numbers[i] > target) {
            fout << "no" << endl;
            fin.close(); fout.close();
            return 0;
        }
    }

    // 卡时技巧：只要时间不到0.9秒就一直重跑
    while ((double)clock() / CLOCKS_PER_SEC < 0.9) {
        sa();
        
        if (found) {
            fout << "yes" << endl;
            for (int b = 0; b < K; b++) {
                bool first = true;
                for (int i = 0; i < N; i++) {
                    if (belong_to[i] == b) {
                        if (!first) fout << " ";
                        fout << numbers[i];
                        first = false;
                    }
                }
                fout << endl;
            }
            fin.close(); fout.close();
            return 0;
        }
    }

    fout << "no" << endl;
    
    fin.close();
    fout.close();
    return 0;
}