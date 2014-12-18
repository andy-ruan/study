#include <iostream>
#include <cassert>

typedef int DATA;

//////////////////////////////////////////////////////////////////
class HeapSort{
    friend std::ostream& operator<<(std::ostream& os, const HeapSort& heap);

    public:
        HeapSort(const DATA* data, int size);
        ~HeapSort();

    public:
        void sort();

    protected:
        void heapify(int last);
        void adjust(int count);

    private:
        HeapSort(const HeapSort&);
        HeapSort& operator = (const HeapSort&);

    protected:
        const DATA*   data;  
        int*    index;
        int     size;
};

HeapSort::HeapSort(const DATA* data, int size)
 :data(data),index(NULL), size(size)
{ 
    this->index =  new int[size]; 
    for ( int i = 0; i < size; i++){
        this->index[i] = i;
    }
}

HeapSort::~HeapSort()
{
    size = 0;
    delete [] index;
    data = NULL;
}
std::ostream& operator<<(std::ostream& os, const HeapSort& heap)
{
    for ( int i = 0; i < heap.size;i ++){
        os<<heap.data[heap.index[i]]<<" ";
    }
    return os;
}

void HeapSort::sort()
{
    std::cout<<*this<<std::endl<<std::endl;
    for ( int i = 1; i < size; i++){
        heapify(i);
    }
    std::cout<<*this<<std::endl<<std::endl;
    for ( int i = 0; i < size; i++){
        const int tmp = index[0];
        index[0] = index[size-i-1];
        index[size-i-1] = tmp;

        adjust(size - i - 1);
        std::cout<<*this<<std::endl;
    }
}

void HeapSort::adjust(int count)
{
    // first is max.
    //
    int top = 0; 
    int val = index[top];

    // left < parent, right < parent.
    for ( int left = 2 * top + 1; left < count; left = 2 * top + 1){
        int right = left + 1;
        if ( data[val] < data[index[left]]){
            if ( left + 1 < count && data[index[left]] < data[index[right]] ){
                index[top] = index[right];
                top = right;
            } else {
                index[top] = index[left];
                top = left;
            }
        } else if (right < count && data[val] < data[index[right]]){
            index[top] = index[right];
            top = right;
        } else {
            break;
        }
    }
    index[top] = val;
}

void HeapSort::heapify(int last)
{
    // first is max.
    while ( last > 0){
        int parent = (last - 1) / 2;
        if ( data[index[parent]] < data[index[last]] ){
            int tmp = index[last];
            index[last] = index[parent];
            index[parent] = tmp;
            last = parent;
        } else {
            break;
        }
    }
}

#ifdef WITH_MAIN_HEAP_SORT

#include <stdlib.h>
#include <sstream>

int main()
{
    srand(time(NULL));    
    int size = rand() % 100 + 1;
    DATA    data[101];
//    size = 10;
    for ( int i = 0; i < size; i++){
        data[i] = (rand()%10000);
        std::cout<<data[i] <<" ";
    }
    std::cout<<std::endl<<std::endl;

    HeapSort heap(data, size);
    heap.sort();
    std::cout<<heap<<std::endl;
}

#endif
