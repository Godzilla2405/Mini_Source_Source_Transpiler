#include <bits/stdc++.h>
using namespace std;

void print_array(const vector<int>& arr) {
    cout << '[';
    for (size_t i = 0; i < arr.size(); ++i) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ", ";
    }
    cout << ']';
}

int partition(vector<int>& arr, int low, int high);
void quick_sort(vector<int>& arr, int low, int high);

int partition(vector<int>& arr, int low, int high) {
    auto pivot = arr[high];
    auto i = (low - 1);
    for (int j = low; j < high; j++) {
        if ((arr[j] <= pivot)) {
            i = (i + 1);
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (i + 1);
}

void quick_sort(vector<int>& arr, int low, int high) {
if ((low < high)) {
    auto pi = partition(arr, low, high);
    quick_sort(arr, low, (pi - 1));
    quick_sort(arr, (pi + 1), high);
}
}

int main() {
    vector<int> arr = {10, 7, 8, 9, 1, 5};
    cout << "Unsorted array:" << " ";
    print_array(arr);
    cout << endl;
    quick_sort(arr, 0, ((arr.size() - 1)));
    cout << "Sorted array:" << " ";
    print_array(arr);
    cout << endl;
    return 0;
}