//DFS solution
#include <iostream>
#include <cstdlib> 
#include <fstream>
#include <cstring> // for strcmp
#include <cstdio>  // for sprintf

using namespace std;

// Global variables
int N;
int* numbers;
int* bucket_sum;
int* belong_to; // record which bucket the i-th number belongs to
int target;

// Comparison function for qsort (Descending order)
int compare(const void* a, const void* b) {
    return (*(int*)b - *(int*)a);
}

// DFS function
bool dfs(int index) {
    // Base case: all numbers placed
    if (index == N) {
        return (bucket_sum[0] == target && bucket_sum[1] == target && bucket_sum[2] == target);
    }

    // Try to place the current number (numbers[index]) into one of the 3 buckets
    for (int i = 0; i < 3; i++) {
        // Pruning 1: Capacity Check
        if (bucket_sum[i] + numbers[index] > target) {
            continue;
        }

        // Action: Place number
        bucket_sum[i] += numbers[index];
        belong_to[index] = i + 1; // Store result 

        // Recursion
        if (dfs(index + 1)) {
            return true;
        }

        // Backtrack
        bucket_sum[i] -= numbers[index];
        belong_to[index] = 0;

        // Pruning 2: Symmetry Breaking for Empty Buckets
        if (bucket_sum[i] == 0) {
            break;
        }
    }

    return false;
}

int main(int argc, char* argv[]) {
    // Faster I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    char input_path[256] = "../../testcase/1.in";
    char output_path[256] = "../../testcase/1.out";

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-test") == 0) {
            if (i + 1 < argc) {
                sprintf(input_path, "../../testcase/%s.in", argv[i+1]);
                sprintf(output_path, "../../testcase/%s.out", argv[i+1]);
                i++; 
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

    // Manual memory allocation (No std::vector)
    numbers = new int[N];
    belong_to = new int[N];
    bucket_sum = new int[3];
    
    long long sum = 0;
    for (int i = 0; i < N; i++) {
        fin >> numbers[i];
        sum += numbers[i];
        belong_to[i] = 0;
    }

    // Basic checks
    if (sum % 3 != 0 || N < 3) {
        fout << "no" << endl;
        delete[] numbers; delete[] belong_to; delete[] bucket_sum;
        fin.close(); fout.close();
        return 0;
    }

    target = (int)(sum / 3);
    bucket_sum[0] = bucket_sum[1] = bucket_sum[2] = 0;

    // Optimization: Sort descending to prioritize large items
    qsort(numbers, N, sizeof(int), compare);

    // Optimization: If largest number > target, impossible
    if (numbers[0] > target) {
        fout << "no" << endl;
        delete[] numbers; delete[] belong_to; delete[] bucket_sum;
        fin.close(); fout.close();
        return 0;
    }

    if (dfs(0)) {
        fout << "yes" << endl;
        // Output the 3 parts
        for (int b = 1; b <= 3; b++) {
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
    } else {
        fout << "no" << endl;
    }

    // Cleanup
    delete[] numbers;
    delete[] belong_to;
    delete[] bucket_sum;
    
    fin.close();
    fout.close();

    return 0;
}