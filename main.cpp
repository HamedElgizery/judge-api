#include <iostream>

using namespace std;

int test() {
  cout << "Yes";
}

int main() {
  test();
  int a, b, c; cin >> a >> b >> c;
  cout << a + b + c / 0 << endl;
}
