# 预处理 - 单应性
import cv2
import kornia
import numpy as np

# 分辨率resize对应的H矩阵变换
def h_adjust(orishapea,orishapeb,resizeshapea,resizeshapeb, h):
    a = orishapea / resizeshapea
    b = orishapeb / resizeshapeb
    # the shape of H matrix should be (1, 3, 3)
    h[:, 0, :] = a*h[:, 0, :]
    h[:, :, 0] = (1./a)*h[:, :, 0]
    h[:, 1, :] = b * h[:, 1, :]
    h[:, :, 1] = (1. / b) * h[:, :, 1]
    return h


# 坐标系转换-H矩阵计算
def change_h():
    # roll 滚转：图像旋转 乘上角度相应的矩阵即可
    # pitch 俯仰
    # yaw 偏航
    # distance 高度

    pass



def cal_H():
    # h = kornia.get_perspective_transform(homo_corners, homo_corners_hat)
    pass


def main():
    # 点击顺序 左上  左下  右上 右下
    # 鼠标操作，鼠标选中源图像中需要替换的位置信息
    def mouse_action(event, x, y, flags, replace_coordinate_array):
        cv2.imshow('collect coordinate', img_dest_copy)
        if event == cv2.EVENT_LBUTTONUP:
            # 画圆函数，参数分别表示原图、坐标、半径、颜色、线宽(若为-1表示填充)
            # 这个是为了圈出鼠标点击的点
            cv2.circle(img_dest_copy, (x, y), 2, (0, 255, 255), -1)

            # 用鼠标单击事件来选择坐标
            # 将选中的四个点存放在集合中
            print(f'{x}, {y}')
            replace_coordinate_array.append([x, y])
    # 
    img_dest = cv2.imread('1.jpg', cv2.IMREAD_COLOR)
    height, width, channel = img_dest.shape # (576, 720, 3)
    # 将源数据复制一份，避免后来对该数据的操作会对结果有影响
    img_dest_copy = np.tile(img_dest, 1)

    # 源图像中的数据
    # 定义一个数组，用来存放要源图像中要替换的坐标点，该坐标点由鼠标采集得到
    replace_coordinate = []
    cv2.namedWindow('collect coordinate')
    cv2.setMouseCallback('collect coordinate', mouse_action, replace_coordinate)
    while True:
        # 当采集到四个点后，可以按esc退出鼠标采集行为
        if cv2.waitKey(20) == 27:
            # 
            break
    print(replace_coordinate)
    # 计算H矩阵
    # 根据选中的四个点坐标和代替换的图像信息完成单应矩阵
    target_coordinate = [[0,0], [0, width], [height, 0], [height, width]] #[height, width]
    replace_coordinate = np.array(replace_coordinate)
    target_coordinate = np.array(target_coordinate)
    matrix, mask = cv2.findHomography(replace_coordinate, target_coordinate, 0)
    print(f'matrix: {matrix}')
    perspective_img = cv2.warpPerspective(img_dest, matrix, (img_dest.shape[1],   img_dest.shape[0]))
    cv2.imshow('img', perspective_img)
    # 按esc退出
    while True:
        if cv2.waitKey(20) == 27:
            # 
            break

if __name__ == "__main__":
    # 点击顺序 左上  左下  右上 右下
    main()
