
import cv2

def main():
    capture=cv2.VideoCapture(0)
    if capture.isOpened() is False:
        raise("IO Error")
    ret,image=capture.read()
    if ret == False:
        print("ret is False")
        return 
    cv2.imwrite("sample.png",image)

if __name__ == '__main__':
    main()
