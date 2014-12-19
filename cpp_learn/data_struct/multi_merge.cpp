#include <ostream>
#include <iostream>

void wait()
{
    int seed = 500;
    for ( int i = 2; i < seed; i++){
        bool is_prime = true;
        for ( int j = 2; j < i; j++){
            if ( i % j == 0){
                is_prime = false;
                break;
            }
        }
    }
}
// Data::operator <
// Data::operator = 
// typedef int Data;
class Data{
    friend std::ostream& operator<<(std::ostream& os, const Data& data);

    public:
        Data(int x = 0): val(x) {}
        Data(const Data& rhs):val(rhs.val){}
        Data& operator = (const Data& rhs)
        {
            if ( this != &rhs ){
                val = rhs.val;
            }
            return *this;
        }
        bool operator < (const Data& rhs) const
        {
            wait();
            return val < rhs.val;
        }

    const static Data     MaxItem;
    const static Data     MinItem;
    private:
        uint32_t val;
};
#ifdef DEBUG
const Data Data::MaxItem = 100;
#else
const Data Data::MaxItem = 20 << 10;
#endif
const Data Data::MinItem = 0;

std::ostream& operator<<(std::ostream& os, const Data& data)
{
    os<<data.val;
    return os;
}

// 多路归并.
class MultiMerge{
    public:
        MultiMerge(Data* dat, int num)
            : num(num)
        {
            data = new Data[num+1];
            index = new int[num+1];
            for ( int i = 0; i < num; i++){
                data[i] = dat[i];
                index[i] = i;
            }
        }
        virtual ~MultiMerge()
        {
            delete [] data;
            delete [] index;
        }

        virtual int best(Data& val) const 
        { 
            val = data[index[0]]; 
            return index[0]; 
        }

        virtual void setKey(int i, const Data& val)
        {
            data[i] = val;
            adjust(i);
        }
    protected:
        virtual void adjust(int idx) {}

    protected:
        void swap(int& x, int& y)
        {
            int tmp = x;
            x = y;
            y = tmp;
        }

        MultiMerge(const MultiMerge&);
        MultiMerge* operator =(const MultiMerge&);

        Data*   data;
        int*    index;
        const int num;

};
////////////////////// 最小堆实现.
class MinHeap:public MultiMerge{
    public:
        MinHeap(Data* dat, int num)
            : MultiMerge(dat, num), heap(index)
        {
            for ( int i = 0; i < num; i++){
                heap[i] = i;
                heapify(i);
            }
        }

    protected:
        void heapify(int i)
        {
            // [0, i-1] is MinHeap.
            // make sure, par < left, par < right.
            // 往上, 小元素上浮.
            for ( int curr = i; curr > 0; ){
                int par = (curr - 1) / 2;
                if ( data[heap[curr]] < data[heap[par]] ){
                    swap(heap[curr], heap[par]);
                    curr = par;
                } else {
                    break;
                }
            }
        }

        void adjust(int idx)
        {
            // make sure: par < left, par < right.
            // 往下, 大元素下沉. 需要 从 根节点 hea[0] 开始
            for ( int curr = 0; curr < num; ){
                int left = curr * 2 + 1;
                int right = left + 1;
                if ( right < num && data[heap[right]] < data[heap[curr]]){
                    if ( data[heap[left]] < data[heap[right]]){
                        swap(heap[curr], heap[left]);
                        curr = left;
                    } else {
                        swap(heap[curr], heap[right]);
                        curr = right;
                    }
                }else if ( left < num && data[heap[left]] < data[heap[curr]]){
                    swap(heap[curr], heap[left]);
                    curr = left;
                } else {
                    break;
                }
            }
        }

    private:
        int*    heap;
};

////////////////////////// 胜者树实现
// 节点更新的时候需要的比较次数较多，比较慢.
//
// winner[] 是内部节点: 树根是 winner[1].
//      winner[i] 记录 winner[2*i] 与 winner[2*i+1]的胜利者.
// data[] 是外部节点
// 左孩子是偶数, 右孩子是奇数
class WinnerTree: public MultiMerge{
    public:
        WinnerTree(Data* dat, int num)
            : MultiMerge(dat, num), winner(index)
        {
            for ( int i = 0; i < num; i++){
                winner[i] = num;
            }
            data[num] = Data::MaxItem;
            winner[num] = num;
            for ( int i = 0; i < num; i++){
                heapify(i);
            }
            winner[0] = winner[1];
        }

    protected:
        void heapify(int idx)
        {
            int curr = (idx+num)/2;
            while ( curr > 0 && data[idx] < data[winner[curr]]){
                winner[curr] = idx;
                curr /= 2;
            }
        }
        void adjust(int idx)
        {
            int curr = (idx+num)/2;
            int other = idx%2 == 0? idx + 1: idx - 1;
            // 左孩子是偶数, 右孩子是奇数
            if ( data[other] < data[idx] ){
                winner[curr] = other;   // 调整叶子节点.
            }

            // 需要调整: 类似于 堆调整: 调整内部节点.
            while ( curr > 0){
                // maker sure: winner[curr/2] 比 winner[curr], winner[other] 都小.
                other = curr %2 == 0? curr + 1: curr - 1;
                if ( data[winner[other]] < data[winner[curr]]){
                    winner[curr/2] = winner[other];
                } else {
                    winner[curr/2] = winner[curr];
                }
                curr /= 2;
            } 
            winner[0] = winner[1];
        }

    private:
        int*    winner;
};

////////////////////////// 败者树实现.
//
// 同胜者树类似, 实际记录的是比较的失败者，而不是胜利者.
//
// looser[] 是内部节点: 树根是 looser[1], looser[0] 是胜利者.
// data[] 是外部节点.
//      对于最底层, looser[i] 记录的是 data[2*i] 和 data[2*i+1]中失败者(大的)
//      对于其他节点 looser[i] 记录的是 Looser[2*i]为跟的胜利者 和 looser[i*2+1]为根的胜利者 中的失败者
// 左孩子是偶数, 右孩子是奇数
cclass LooserTree: public MultiMerge{
    public:
        LooserTree(Data* dat, int num)
            : MultiMerge(dat, num), looser(index)
        {
            for ( int i = 0; i < num; i++){
                looser[i] = num;
            }
            data[num] = Data::MinItem;
            looser[num] = num;
            for ( int i = 0; i < num; i++){
                adjust(i);
            }
        }

    protected:
       void adjust(int idx)
       {
           int win(idx);
           for (int curr = (idx + num)/2; curr > 0; curr /= 2){
               if ( data[looser[curr]] < data[win]){
                   swap(looser[curr], win);
                }
            }
            looser[0] = win;
       } 
 
    private:
        int*    looser;
};
#ifdef WITH_MAIN_MULTI_MERGE
#include <iostream>
#include <unistd.h>
#include <sys/time.h>

class DataGen{
    public:
        DataGen(const int seed):init(seed), seed(seed){}

        Data next()
        {
            Data tmp(seed);
            if ( Data::MaxItem < tmp){
                return Data::MaxItem;
            }
            seed += 3;
            return tmp;
        }
        void reset(){ seed = init; }
    private:
        const int init;
        int seed;
};

int test(MultiMerge* merge, DataGen** dataGen, int num)
{
    struct timeval t1,t2;
    gettimeofday(&t1, NULL);

    int     idx = 1;
    while ( 1 ){
        Data    best;
        int     best_idx = merge->best(best);
        if ( best < Data::MaxItem){
#ifdef  DEBUG
//            std::cout<<best<<"("<<best_idx<<") ";
            std::cout<<best<<" ";
            if ( idx % (num*2) == 0){
                std::cout<<std::endl;
                idx = 0;
            }
#endif
            idx ++;
            merge->setKey(best_idx, dataGen[best_idx]->next());
        } else {
            break;
        }
    }

    gettimeofday(&t2, NULL);
    return (t2.tv_sec - t1.tv_sec) * 1000 + (t2.tv_usec - t1.tv_usec)/ 1000;
}
int main()
{
    DataGen* dataGen[6];
    dataGen[0] = new DataGen(1); 
    dataGen[1] = new DataGen(3); 
    dataGen[2] = new DataGen(4); 
    dataGen[3] = new DataGen(5); 
    dataGen[4] = new DataGen(2); 
    dataGen[5] = new DataGen(0); 

    Data     data[6];
    for ( int i = 0; i < 6; i++){
        dataGen[i]->reset();
        data[i] = dataGen[i]->next();
    }
    /*
    for ( int i = 0; i < 100; i++){
        for ( int j = 0; j < 6; j++){
            Data data = dataGen[j]->next();
            std::cout<<data<<" ";
        }
        std::cout<<std::endl;
    }
    return 0;
    */

    MultiMerge* merge = NULL;
    int ms = 0;
    for ( int i = 0; i < 6; i++){
        dataGen[i]->reset();
        data[i] = dataGen[i]->next();
    }
    merge = new MinHeap(data, 6);
    ms = test(merge, dataGen, 6);
    std::cout<<std::endl;
    std::cout<<"MinHeap: "<<ms<<" ms"<<std::endl;
    delete merge;

    for ( int i = 0; i < 6; i++){
        dataGen[i]->reset();
        data[i] = dataGen[i]->next();
    }
    merge = new WinnerTree(data, 6);
    ms = test(merge, dataGen, 6);
    std::cout<<std::endl;
    std::cout<<"WinnerTree: "<<ms<<" ms"<<std::endl;
    delete merge;

    for ( int i = 0; i < 6; i++){
        dataGen[i]->reset();
        data[i] = dataGen[i]->next();
    }
    merge = new LooserTree(data, 6);
    ms = test(merge, dataGen, 6);
    std::cout<<std::endl;
    std::cout<<"LooserTree: "<<ms<<" ms"<<std::endl;
    delete merge;
  
}
#endif
