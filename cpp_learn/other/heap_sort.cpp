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
        DATA*   data;  
        int     size;
};

HeapSort::HeapSort(const DATA* data, int size)
 :size(size)
{ 
    this->data = new DATA[size]; 
    for ( int i = 0; i < size; i++){
        this->data[i] = data[i];
    }
}

HeapSort::~HeapSort()
{
    size = 0;
    delete [] data;
    data = NULL;
}
std::ostream& operator<<(std::ostream& os, const HeapSort& heap)
{
    for ( int i = 0; i < heap.size;i ++){
        os<<heap.data[i]<<" ";
    }
    return os;
}

void HeapSort::sort()
{
//    std::cout<<*this<<std::endl<<std::endl;
    for ( int i = 1; i < size; i++){
        heapify(i);
    }
//    std::cout<<*this<<std::endl<<std::endl;
    for ( int i = 0; i < size; i++){
        const DATA tmp = data[0];
        data[0] = data[size-i-1];
        data[size-i-1] = tmp;
        adjust(size - i - 1);
//        std::cout<<*this<<std::endl;
    }
}

void HeapSort::adjust(int count)
{
    // first is max.
    //
    int top = 0; 
    DATA val = data[top];

    // left < parent, right < parent.
    for ( int left = 2 * top + 1; left < count; left = 2 * top + 1){
        int right = left + 1;
        if ( val < data[left]){
            if ( left + 1 < count && data[left] < data[right] ){
                data[top] = data[right];
                top = right;
            } else {
                data[top] = data[left];
                top = left;
            }
        } else if (right < count && val < data[right]){
            data[top] = data[right];
            top = right;
        } else {
            break;
        }
    }
    data[top] = val;
}

void HeapSort::heapify(int last)
{
    // first is max.
    while ( last > 0){
        int parent = (last - 1) / 2;
        if ( data[parent] < data[last] ){
            DATA tmp = data[last];
            data[last] = data[parent];
            data[parent] = tmp;
            last = parent;
        } else {
            break;
        }
    }

/*
*/

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
