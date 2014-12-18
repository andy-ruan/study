#include <iostream>
#include <cassert>
#include <vector>

typedef uint32_t DATA;
//DATA  maxItem(-1);
//DATA  maxItem(1000);
DATA  maxItem(1000);
DATA  minItem(0);


//////////////////////////////////////////////////////////////////
class WinnerTree{
    friend std::ostream& operator<<(std::ostream& os, const WinnerTree& tree);

    public:
        WinnerTree(DATA* dat, int num)
        : num(num)
        {
            size = 1;
            while ( size < num){
                size <<= 1;
            }

            this->winner =  new int[size+1];
            this->data = new DATA[size+1];
            for ( int i = 0; i < num; i++){
                this->data[i] = dat[i];
                this->winner[i] = num;
            }
            for ( int i = num; i <= size; i++){
                this->data[i] = maxItem;
                this->winner[i] = num;
            }
        }
        ~WinnerTree();
        virtual void init();

    public:
        void sort();

    protected:
        virtual void adjust(int idx);
        virtual void rebuild(int idx);

    private:
        WinnerTree(const WinnerTree&);
        WinnerTree& operator = (const WinnerTree&);

    protected:
        DATA*   data;  
        int*    winner;
        int     size;
        const int     num;
};
class LooserTree: public WinnerTree{
    public:
        LooserTree(DATA* dat, int num)
            : WinnerTree(dat, num), looser(winner)
        {
            for ( int i = num; i <= size; i++){
                this->data[i] = minItem;
            }
 
        }

    public:
        virtual void sort();

    protected:
        virtual void adjust(int idx);

    protected:
        int*    looser;
};

void WinnerTree::init()
{ 
    std::cout<<*this<<std::endl;
    for ( int i = 0; i < num; i ++){
        //adjust(num - i - 1);
        adjust(i);
        std::cout<<"============ "<< i<<std::endl;
        std::cout<<*this<<std::endl;
    }
}

WinnerTree::~WinnerTree()
{
    size = 0;
    delete [] winner;
    delete [] data;
    data = NULL;
    winner = NULL;
}
std::ostream& operator<<(std::ostream& os, const WinnerTree& heap)
{
    os<<"0:"<<heap.winner[0]<<std::endl;
    for ( int i = 1, sum = 1; sum < heap.size; i*=2){
        for ( int j = 0; j < i && sum < heap.size; j++, sum++){
            os<<sum<<":"<<heap.winner[sum]<<" ";
        } 
        os<<std::endl;
    }
    for ( int i = 0; i <= heap.num; i++){
        os<<i<<":"<<heap.data[i]<<" ";
    }
    os<<std::endl;
    return os;
}

void WinnerTree::adjust(int idx)
{
    fprintf(stderr, "in WinnerTree\n");
    int cur = (idx + size) / 2;
    while ( cur > 0 && data[idx] < data[winner[cur]]){
        winner[cur] = idx; 
        cur /= 2;
    }
}
void WinnerTree::rebuild(int idx)
{
    int curr = (idx+size)/2;
    int other = idx%2 == 0? idx + 1: idx - 1;
    // 左孩子是偶数, 右孩子是奇数
    if ( data[other] < data[idx] ){
        winner[curr] = other;
    }

    // 需要调整: 类似于 堆调整
    while ( curr > 0){
        other = curr %2 == 0? curr + 1: curr - 1;
        if ( data[winner[other]] < data[winner[curr]]){
            winner[curr/2] = winner[other];
        } else {
            winner[curr/2] = winner[curr];
        }
        curr /= 2;
    } 
}


void WinnerTree::sort()
{
    std::vector<DATA>   result;
    for ( int i = 0; i < num; i ++){
        result.push_back(data[winner[1]]);
        data[winner[1]] = maxItem;
        rebuild(winner[1]);
        std::cout<<"============ "<< i<<std::endl;
        std::cout<<*this<<std::endl;
    }
    std::cout<<"=========================\n";
    for ( int i = 0; i < result.size(); i++){
        std::cout<<result[i]<<" ";
    }
    std::cout<<std::endl;
    std::cout<<"=========================\n";
}

void LooserTree::adjust(int idx)
{
    std::cout<<"in Looser\n";
    int win(idx);
    int curr = (idx + size) / 2;
    while ( curr > 0){
        if ( data[looser[curr]] < data[win] ){
            int tmp = looser[curr];
            looser[curr] = win;
            win = tmp;
        }
        curr /= 2;
    }
    looser[0] = win;
}

void LooserTree::sort()
{
    std::vector<DATA>   result;

    for ( int i = 0; i <= num; i ++){
        result.push_back(data[looser[0]]);
        data[looser[0]] = maxItem;
        adjust(looser[0]);
        std::cout<<"============ "<< i<<std::endl;
        std::cout<<*this<<std::endl;
    }
    std::cout<<"=========================\n";
    for ( int i = 0; i < result.size(); i++){
        std::cout<<result[i]<<" ";
    }
    std::cout<<std::endl;
    std::cout<<"=========================\n";
}
/*
*/

#ifdef WITH_MAIN_WINNER_TREE

#include <stdlib.h>
#include <sstream>

int main()
{
    int seed = time(NULL);
    seed = 1418807438;
    std::cout<<"seed="<<seed<<std::endl;
    srand(seed);
    int size = rand() % 100 + 1;
    DATA    data[101];
    size = 10;
    for ( int i = 0; i < size; i++){
        data[i] = (rand()%100);
        std::cout<<i<<":"<<data[i] <<" ";
    }
    std::cout<<std::endl<<std::endl;

    WinnerTree winner(data, size);
    LooserTree looser(data, size);

    winner.init();
    winner.sort();

    looser.init();
    looser.sort();

}

#endif
