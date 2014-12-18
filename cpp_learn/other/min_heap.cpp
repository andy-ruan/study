#include <iostream>
#include <cassert>

// DATA::operator <
// DATA::operator = 
// typedef int DATA;
class DATA{
    friend std::ostream& operator<<(std::ostream& os, const DATA& data);

    public:
        DATA(int x = 0): val(x) {}
        DATA(const DATA& rhs):val(rhs.val){}
        DATA& operator = (const DATA& rhs)
        {
            if ( this != &rhs ){
                val = rhs.val;
            }
            return *this;
        }
        bool operator < (const DATA& rhs) const
        {
            return val < rhs.val;
        }

    private:
        int val;

};


std::ostream& operator<<(std::ostream& os, const DATA& data)
{
    os<<data.val;
    return os;
}
//////////////////////////////////////////////////////////////////
class MinHeap{
    friend std::ostream& operator<<(std::ostream& os, const MinHeap& heap);

    public:
        MinHeap(int size);
        ~MinHeap();

    public:
        void insert(const DATA& dt);
        bool empty() const { return count <= 0;}
        DATA pop();

    protected:
        void heapify(int top);

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
std::ostream& operator<<(std::ostream& os, const MinHeap& heap)
{
    assert(0 <= heap.count && heap.count <= heap.size);
    for ( int i = 0; i < heap.count;i ++){
        os<<heap.data[i]<<" ";
    }
    return os;
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

#ifdef WITH_MAIN_MIN_HEAP

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
        std::cout<<heap<<std::endl;
        heap.pop();
    }
}

#endif
