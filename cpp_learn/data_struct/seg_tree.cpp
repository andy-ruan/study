
#define WITH_MAIN_SEG_TREE
typedef struct _PointPair{
    int left;
    int right; 
} PointPair;

class PointPairCmp{
    public:
        bool operator () (const PointPair& left, const PointPair& right)
        {
            if ( left.left == right.left){
                return left.right < right.right;
            }
            return left.left < right.left;
        }
};


#ifdef WITH_MAIN_SEG_TREE

#include <stdlib.h>
#include <sstream>
#include <vector>
#include <iostream>

int main()
{
    srand(time(NULL));    
    int size = 20;
    std::vector<PointPair>  points;

    for ( int i = 0; i < size; i++){
        PointPair   point;
        point.left = rand() % 1000;
        point.right = rand() % 1000;
        if ( point.left > point.right){
            continue;
        }
        points.push_back(point);
    }
    /*
    for ( int i = 0; i < points.size(); i++){
        std::cout<<"["<<points[i].left<<","<<points[i].right<<"]"<<std::endl;
    }
    */
    std::sort(points.begin(), points.end(), PointPairCmp());
    for ( int i = 0; i < points.size(); i++){
        std::cout<<"["<<points[i].left<<","<<points[i].right<<"]"<<std::endl;
    }
}

#endif
