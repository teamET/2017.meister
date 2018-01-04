#include<iostream>
#include<string>
#include<opencv2/imgcodecs.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>
#include<opencv2/core/core.hpp>

int main(){
//    cv::Mat image=cv::imread("sample_image/kuruma.jpg",cv::IMREAD_COLOR);
    cv::Mat image=cv::imread("sample_image/kosen.jpg",cv::IMREAD_COLOR);
    cv::resize(image,image,cv::Size(),0.3,0.3);
    if(image.empty()){
        std::cout<<"image not found";
        std::exit(0);
    }
    cv::namedWindow("image_AUTO",cv::WINDOW_AUTOSIZE);
    cv::namedWindow("image_FULL",cv::WINDOW_FULLSCREEN);
    cv::imshow("image_FULL",image);
    cv::waitKey(0);
/*  if(cv::waitKey(30)=>0){
        std::exit(0);
    }
*/
//    cv::destroyAllWindows();
	return 0;
}
