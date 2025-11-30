// dynamic programming solution
#include <iostream>
#include <cstdlib>
#include <fstream>

using namespace std;

int main() {
    ifstream fin("input.txt");
    ofstream fout("output.txt");

    if (!fin.is_open() || !fout.is_open()) return 1;

    int N;
    if (!(fin >> N)) return 0;

    int* numbers = new int[N + 1]; 
    int sum = 0;
    
    for (int i = 1; i <= N; i++) {
        fin >> numbers[i];
        sum += numbers[i];
    }

    if (sum % 3 != 0) {
        fout << "no" << endl;
        fin.close(); fout.close();
        delete[] numbers;
        return 0;
    }

    int target = sum / 3;

    // Dynamic allocation of 3D array
    char*** path = new char**[N + 1];
    bool** dp = new bool*[target + 1]; // Current DP state

    for (int i = 0; i <= target; i++) {
        dp[i] = new bool[target + 1];
        for (int j = 0; j <= target; j++) {
            dp[i][j] = false;
        }
    }

    for (int k = 0; k <= N; k++) {
        path[k] = new char*[target + 1];
        for (int i = 0; i <= target; i++) {
            path[k][i] = new char[target + 1];
            // Initialize with 0
            for(int j = 0; j <= target; j++) path[k][i][j] = 0;
        }
    }

    // Initialization
    dp[0][0] = true; 

    // DP Transitions
    for (int k = 1; k <= N; k++) {
        int val = numbers[k];      
        bool** next_dp = new bool*[target + 1];
        for(int i=0; i<=target; i++) {
            next_dp[i] = new bool[target+1];
            for(int j=0; j<=target; j++) next_dp[i][j] = false;
        }

        for (int i = 0; i <= target; i++) {
            for (int j = 0; j <= target; j++) {
                if (dp[i][j]) { // If previous state was reachable
                    
                    // Option 1: Put into Bucket 1
                    if (i + val <= target) {
                        next_dp[i + val][j] = true;
                        path[k][i + val][j] = 1; 
                    }

                    // Option 2: Put into Bucket 2
                    if (j + val <= target) {
                        next_dp[i][j + val] = true;
                        path[k][i][j + val] = 2;
                    }

                    // Option 3: Put into Bucket 3
                    next_dp[i][j] = true; 
                    path[k][i][j] = 3;
                }
            }
        }
        
        // Update dp table for next iteration
        for(int i=0; i<=target; i++) {
            for(int j=0; j<=target; j++) {
                dp[i][j] = next_dp[i][j];
            }
            delete[] next_dp[i];
        }
        delete[] next_dp;
    }

    // Check result
    if (dp[target][target]) {
        fout << "yes" << endl;
        
        // Reconstruct solution
        int* out1 = new int[N]; int c1 = 0;
        int* out2 = new int[N]; int c2 = 0;
        int* out3 = new int[N]; int c3 = 0;

        int curr_i = target;
        int curr_j = target;

        for (int k = N; k >= 1; k--) {
            int choice = path[k][curr_i][curr_j];
            int val = numbers[k];
            
            if (choice == 1) {
                out1[c1++] = val;
                curr_i -= val;
            } else if (choice == 2) {
                out2[c2++] = val;
                curr_j -= val;
            } else {
                out3[c3++] = val;
                // curr_i and curr_j do not change
            }
        }

        // Output Bucket 1
        for(int i=0; i<c1; i++) fout << (i==0?"":" ") << out1[i]; fout << endl;
        // Output Bucket 2
        for(int i=0; i<c2; i++) fout << (i==0?"":" ") << out2[i]; fout << endl;
        // Output Bucket 3
        for(int i=0; i<c3; i++) fout << (i==0?"":" ") << out3[i]; fout << endl;

        delete[] out1; delete[] out2; delete[] out3;

    } else {
        fout << "no" << endl;
    }

    // Cleanup memory
    for (int i = 0; i <= target; i++) delete[] dp[i];
    delete[] dp;
    
    for (int k = 0; k <= N; k++) {
        for (int i = 0; i <= target; i++) delete[] path[k][i];
        delete[] path[k];
    }
    delete[] path;
    delete[] numbers;

    fin.close();
    fout.close();

    return 0;
}