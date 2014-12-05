#include <iostream>
#include <cassert>

// DATA::operator <
// DATA::operator = 
typedef int DATA;

class MinHeap{
    public:
        MinHeap(int size);
        ~MinHeap();

    public:
        void insert(const DATA& dt);
        void heapify(int top);
        bool empty() const { return count <= 0;}
        DATA pop();

        std::ostream& print(std::ostream& ss);

    private:
        MinHeap(const MinHeap&);
        MinHeap& operator = (const MinHeap&);

    protected:
        DATA*   data;  
        int     size;
        int     count;
};

MinHeap::MinHeap(int size)
 :size(size), count(0)
{ 
    data = new DATA[size]; 
}

MinHeap::~MinHeap()
{
    count = size = 0;
    delete [] data;
    data = NULL;
}
std::ostream& MinHeap::print(std::ostream& ss)
{
    assert(0 <= count && count <= size);
    for ( int i = 0; i < count;i ++){
        ss<<data[i]<<" ";
    }
    return ss;
}

void MinHeap::insert(const DATA& val)
{
    if ( count >= size ){
        if ( val < data[0] ){
            pop();
        } else {
            return; // ignore.
        }
    }
    int cur = count ++;
    while ( cur > 0){
        int par = (cur - 1) / 2;
        if ( val < data[par] ){
            data[cur] = data[par];
        } else {
            break;
        }
        cur = par;
    }
    data[cur] = val;
}

DATA MinHeap::pop()
{
    DATA min = data[0];
    if ( count >= 1 ){
        data[0] = data[--count];
        if ( count > 0){
            heapify(0);
        }
    }
    return min;
}
void MinHeap::heapify(int top)
{
    assert( 0 <= top && top < count);
    DATA val = data[top];

    // parent < left, parent < right.
    for ( int child = 2 * top + 1; child < count; child = 2 * top + 1){
        if ( data[child] < val ){
            if ( child + 1 < count && data[child+1] < data[child] ){
                data[top] = data[child+1];
                top = child + 1;
            } else {
                data[top] = data[child];
                top = child;
            }
        } else if (child +1 < count && data[child+1] < val){
            data[top] = data[child+1];
            top = child + 1;
        } else {
            break;
        }
    }
    assert(0 <= top && top < count);
    data[top] = val;
}

#ifdef WITH_MAIN_HEAP_SORT

#include <stdlib.h>
#include <sstream>

int main()
{
    srand(time(NULL));    
    int size = rand() % 100 + 1;
    MinHeap heap(10);
    for ( int i = 0; i < size; i++){
        heap.insert(rand()%10000);
    }
    for ( int i = 0; i < size; i++){
        if (heap.empty()){
            break;
        }
        heap.print(std::cout)<<std::endl;
        heap.pop();
    }
}

#endif
