#include <iostream>
#include <cstdlib>
#include <cmath>
#include <ctime>
#include <fstream>
#include <algorithm> 
#include <cstring>
#include <cstdio>  /

using namespace std;

// K=3 for the basic task; change to 4, 5... for the Bonus task
const int K = 3; 
const int MAX_N = 10005;

int N;
int numbers[MAX_N];
int belong_to[MAX_N];       // Records which bucket (0 ~ K-1) each number currently belongs to
long long bucket_sum[K];    // Current sum of each bucket
long long target;           // Target sum for each bucket (Total Sum / K)
bool found = false;         // Flag to indicate if a solution has been found

// Comparison function for descending sort
bool compare_desc(int a, int b) {
    return a > b;
}

// Calculate total difference (Energy/Cost) between all buckets and the target
long long get_diff() {
    long long diff = 0;
    for (int i = 0; i < K; i++) {
        long long d = bucket_sum[i] - target;
        diff += (d > 0 ? d : -d); // Accumulate absolute difference
    }
    return diff;
}

// Simulated Annealing core function
void sa(bool use_greedy) {
    // Reset bucket states
    for (int i = 0; i < K; i++) bucket_sum[i] = 0;

    // Initialize distribution
    if (use_greedy) {
        // This generates an initial state with very low energy (close to the solution)
        for (int i = 0; i < N; i++) {
            int min_idx = 0;
            // Find the bucket with the minimum sum
            for (int b = 1; b < K; b++) {
                if (bucket_sum[b] < bucket_sum[min_idx]) {
                    min_idx = b;
                }
            }
            belong_to[i] = min_idx;
            bucket_sum[min_idx] += numbers[i];
        }
    } else {
        // Even if greedy gets stuck in local optima, random initialization provides diversity through restarts
        for (int i = 0; i < N; i++) {
            belong_to[i] = rand() % K;
            bucket_sum[belong_to[i]] += numbers[i];
        }
    }

    // Annealing parameters
    double T = 5000.0;     // Initial temperature
    double alpha = 0.99;   // Cooling rate (larger means slower cooling)
    double end_T = 1e-4;   // End temperature

    // Calculate initial energy
    long long cur_diff = get_diff();

    // Annealing main loop
    while (T > end_T) {
        // If energy drops to 0, a perfect partition is found
        if (cur_diff == 0) {
            found = true;
            return;
        }

        // Randomly select a neighbor operation: Move(0) or Swap(1)
        int op = rand() % 2; 

        if (op == 0) { 
            // Randomly select a number and move it from the current bucket to another random bucket
            int idx = rand() % N;
            int old_b = belong_to[idx];
            int new_b = rand() % K;
            
            if (old_b == new_b) continue;

            long long old_e = abs(bucket_sum[old_b] - target) + abs(bucket_sum[new_b] - target);
            
            // Attempt to modify state
            bucket_sum[old_b] -= numbers[idx];
            bucket_sum[new_b] += numbers[idx];
            
            long long new_e = abs(bucket_sum[old_b] - target) + abs(bucket_sum[new_b] - target);
            
            // New total energy = Current total energy - Old partial energy + New partial energy
            long long next_diff = cur_diff - old_e + new_e;

            // Metropolis Criterion
            if (next_diff < cur_diff || exp((cur_diff - next_diff) / T) > (double)rand() / RAND_MAX) {
                cur_diff = next_diff;
                belong_to[idx] = new_b; // Confirm move
            } else {
                // Reject move, backtrack state
                bucket_sum[old_b] += numbers[idx];
                bucket_sum[new_b] -= numbers[idx];
            }
        } else {
            // Randomly select two numbers and swap their buckets
            int i1 = rand() % N;
            int i2 = rand() % N;
            if (belong_to[i1] == belong_to[i2]) continue;

            int b1 = belong_to[i1];
            int b2 = belong_to[i2];

            long long old_e = abs(bucket_sum[b1] - target) + abs(bucket_sum[b2] - target);

            // Attempt swap
            bucket_sum[b1] -= numbers[i1]; bucket_sum[b1] += numbers[i2];
            bucket_sum[b2] -= numbers[i2]; bucket_sum[b2] += numbers[i1];

            long long new_e = abs(bucket_sum[b1] - target) + abs(bucket_sum[b2] - target);
            long long next_diff = cur_diff - old_e + new_e;

            if (next_diff < cur_diff || exp((cur_diff - next_diff) / T) > (double)rand() / RAND_MAX) {
                cur_diff = next_diff;
                // Confirm swap, update ownership array
                int tmp = belong_to[i1];
                belong_to[i1] = belong_to[i2];
                belong_to[i2] = tmp;
            } else {
                // Backtrack state
                bucket_sum[b1] -= numbers[i2]; bucket_sum[b1] += numbers[i1];
                bucket_sum[b2] -= numbers[i1]; bucket_sum[b2] += numbers[i2];
            }
        }
        // Cool down
        T *= alpha;
    }
}

int main(int argc, char* argv[]) {
    // Seed random number generator with current time
    srand(time(NULL));

    // Default I/O paths
    char input_path[256] = "../../testcases/1.in";
    char output_path[256] = "../../testcases/1.out";

    // Parse command line argument -test
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-test") == 0) {
            if (i + 1 < argc) {
                // Modify path based on argument, e.g., -test 1 -> read ../../testcases/1.in
                sprintf(input_path, "../../testcases/%s.in", argv[i+1]);
                sprintf(output_path, "../../testcases/%s.out", argv[i+1]);
                i++; // Skip argument value
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

    // Pruning: If total sum is not divisible by K, no solution exists
    if (sum % K != 0) {
        fout << "no" << endl;
        fin.close(); fout.close();
        return 0;
    }

    target = sum / K;
    // Pruning: If any number is larger than target, no solution exists
    for(int i = 0; i < N; i++) {
        if(numbers[i] > target) {
            fout << "no" << endl;
            fin.close(); fout.close();
            return 0;
        }
    }

    // Preprocessing: Sort array in descending order, crucial for greedy initialization
    sort(numbers, numbers + N, compare_desc);

    int run_count = 0;
    while ((double)clock() / CLOCKS_PER_SEC < 0.9) {
        // Subsequent restarts use random initialization (use_greedy = false) for diversity
        sa(run_count == 0);
        
        if (found) {
            fout << "yes" << endl;
            // Output contents of K buckets
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
        run_count++;
    }

    // If no solution found within time limit, output no
    fout << "no" << endl;
    
    fin.close();
    fout.close();
    return 0;
}