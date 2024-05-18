#include <iostream>
#include <vector>

using namespace std;

int test() {
  cout << "Yes";
  return 0;
}

int main() {
  vector<int> v;
  while (1) {
    v.push_back(1);
  }
  return 0;
}
