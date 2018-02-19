
#include<opencv2/highgui.hpp>
#include<opencv2/opencv.hpp>

int main(int argc,char *argv[]){
    cv::VideoCapture cap(0);
    if(!cap.isOpened()){
        return -1;
    }
    while(1){
        cv::Mat frame;
        cap>>frame;
        cv::imshow("window",frame);
        int key=cv::waitKey(1);
        if(key==113){
            break;
        }else if(key==115){
            cv::imwrite("img.png",frame);
        }
    }
    cv::destroyAllWindows();
    return 0;
}
