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

// ��·�鲢.
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
////////////////////// ��С��ʵ��.
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
            // ����, СԪ���ϸ�.
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
            // ����, ��Ԫ���³�. ��Ҫ �� ���ڵ� hea[0] ��ʼ
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

////////////////////////// ʤ����ʵ��
// �ڵ���µ�ʱ����Ҫ�ıȽϴ����϶࣬�Ƚ���.
//
// winner[] ���ڲ��ڵ�: ������ winner[1].
//      winner[i] ��¼ winner[2*i] �� winner[2*i+1]��ʤ����.
// data[] ���ⲿ�ڵ�
// ������ż��, �Һ���������
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
            // ������ż��, �Һ���������
            if ( data[other] < data[idx] ){
                winner[curr] = other;   // ����Ҷ�ӽڵ�.
            }

            // ��Ҫ����: ������ �ѵ���: �����ڲ��ڵ�.
            while ( curr > 0){
                // maker sure: winner[curr/2] �� winner[curr], winner[other] ��С.
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

////////////////////////// ������ʵ��.
//
// ͬʤ��������, ʵ�ʼ�¼���ǱȽϵ�ʧ���ߣ�������ʤ����.
//
// looser[] ���ڲ��ڵ�: ������ looser[1], looser[0] ��ʤ����.
// data[] ���ⲿ�ڵ�.
//      ������ײ�, looser[i] ��¼���� data[2*i] �� data[2*i+1]��ʧ����(���)
//      ���������ڵ� looser[i] ��¼���� Looser[2*i]Ϊ����ʤ���� �� looser[i*2+1]Ϊ����ʤ���� �е�ʧ����
// ������ż��, �Һ���������
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
