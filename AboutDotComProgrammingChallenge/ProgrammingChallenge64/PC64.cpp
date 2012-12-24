// Problem Description: http://cplus.about.com/od/programmingchallenges/a/programming-challenge-64-Sum-Some-Numbers.htm

#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>

using namespace std;

void get_input(vector<int> &iv)
{
    ifstream ifs("Numbers.txt");
    int tmp_int = 0;

    for(int i = 0; i < 1000; i++)
    {
        ifs >> tmp_int;
        iv.push_back(tmp_int);
    }
}

void solve(const vector<int> &iv)
{
    int max_ending_here = 0;
    int max_so_far = 0;

    //These two integers correspond to max_so_far
    int max_start_pos = 0;
    int max_end_pos = 0;

    //This correspond to max_ending_here
    int max_start_pos_inclusive = 0;

    for(int i = 0; i < 1000; i++)
    {
        if(0 > (max_ending_here + iv[i]))
        {
            max_ending_here = 0;
            max_start_pos_inclusive = i;
        }
        else
        {
            max_ending_here = max_ending_here + iv[i];
        }

        if( max_so_far < max_ending_here)
        {
            max_so_far = max_ending_here;
            max_start_pos = max_start_pos_inclusive;
            max_end_pos =  i;
        }
    }

    cout << max_so_far << ", " << max_start_pos << ", " << max_end_pos << endl;
}

int main()
{
    vector<int> iv;
    iv.reserve(1000);

    get_input(iv);

    solve(iv);

    return 0;
}
