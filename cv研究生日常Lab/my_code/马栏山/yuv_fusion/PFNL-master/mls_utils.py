import numpy as np
import sys
import math
import glob
import os


def yuv_import(video_path, startfrm, nfs, height_frame=0,
               width_frame=0, opt_bar=False, opt_clear=False):
    """ryanxing 200520
    import Y U V channels from a yuv video.

    nfs: num of frames that you need.
    startfrm: start from 0.

    return: Y, U, V, each with (nfs, height, width), [0, 255], uint8
        if startfrm excesses the file len, return [] & no error.
    """
    fp = open(video_path, 'rb')  # 0101...bytes

    # retrieve resolution info from video path
    if height_frame == 0:
        # res = video_path.split("-")[2].split("_")[0]
        res = video_path.split("_")[-2]
        width_frame = int(res.split("x")[0])
        height_frame = int(res.split("x")[1])

    # target at startfrm
    blk_size = int(height_frame * width_frame * 3 / 2)
    fp.seek(blk_size * startfrm, 0)

    d0 = height_frame // 2
    d1 = width_frame // 2

    # init
    y_batch = []
    u_batch = []
    v_batch = []

    # extract
    y_size = height_frame * width_frame
    u_size = d0 * d1
    v_size = d0 * d1
    for ite_frame in range(nfs):

        if ite_frame == 0:
            tmp_c = fp.read(1)
            if tmp_c == b'':  # startfrm > the last frame
                return [], [], []
            fp.seek(-1, 1)  # offset=-1, start from the present position

        y_frame = [ord(fp.read(1)) for i in range(y_size)]  # bytes -> ascii
        y_frame = np.array(y_frame, dtype=np.uint8).reshape((height_frame, width_frame))
        y_batch.append(y_frame)

        u_frame = [ord(fp.read(1)) for i in range(u_size)]
        u_frame = np.array(u_frame, dtype=np.uint8).reshape((d0, d1))
        u_batch.append(u_frame)

        v_frame = [ord(fp.read(1)) for i in range(v_size)]
        v_frame = np.array(v_frame, dtype=np.uint8).reshape((d0, d1))
        v_batch.append(v_frame)

        if opt_bar:
            print("\r<%d, %d>" % (ite_frame, nfs - 1), end="", flush=True)

    fp.close()

    if opt_clear:
        print("\r" + 20 * " ", end="\r", flush=True)

    y_batch = np.array(y_batch)
    u_batch = np.array(u_batch)
    v_batch = np.array(v_batch)
    return y_batch, u_batch, v_batch


def write_yuv(video_path, y_frame, u_frame, v_frame):
    """ryanxing 200520
    add one yuv 420p frame into the yuv file.

    y: (H W), [0, 1], torch.float32 on cpu
    u, v: (H/2 W/2), [0, 255], int (bytes -> utf-8) on cpu
    """
    fp = open(video_path, 'ab')

    y_frame = y_frame.mul(255).clamp(0, 255).round().byte().numpy()  # torch.float32 -> int -> bytes in cpu
    y_frame = np.reshape(y_frame, (1, -1))
    u_frame = np.reshape(u_frame, (1, -1))
    v_frame = np.reshape(v_frame, (1, -1))

    for i in y_frame:
        fp.write(i)
    for i in u_frame:
        fp.write(bytes(i))  # int -> bytes
    for i in v_frame:
        fp.write(bytes(i))  # int -> bytes

    fp.close()


def _as_floats(img1, img2):
    """
    promote im1, im2 to nearest appropriate floating point precision.
    """
    float_type = np.result_type(img1.dtype, img2.dtype, np.float32)
    img1 = np.asarray(img1, dtype=float_type)
    img2 = np.asarray(img2, dtype=float_type)
    return img1, img2


def cal_mse(img1, img2):
    """
    calculate mse (mean squared error) of two imgs.
    
    img1, img2: (H W)
    
    return mse, np.float32
    """
    assert (len(img1.shape) == 2), "len(img1.shape) != 2!"
    assert (img1.shape == img2.shape), "img1.shape != img2.shape!"
    img1, img2 = _as_floats(img1, img2) # necessary!!!
    return np.mean((img1 - img2)**2, dtype=np.float32) # default to average flattened array. so no need to reshape into 1D array


def cal_psnr(img1, img2):
    """
    calculate psnr of two imgs
    
    img1, img2: (C H W), [0, 255], uint8
    
    return ave of psnrs of all channels], np.float32
    """
    assert (len(img1.shape) == 3), "len(img1.shape) != 3!"
    assert (img1.shape == img2.shape), "img1.shape != img2.shape!"
    img1, img2 = _as_floats(img1, img2) # necessary!!!
    mse_channels = [cal_mse(img1[i], img2[i]) for i in range(img1.shape[0])]
    if min(mse_channels) == 0:
        return float('inf')
    psnr_channels = [10 * math.log10(65025.0 / mse) for mse in mse_channels]
    return np.mean(psnr_channels, dtype=np.float32)


def y4m2yuv(y4m_dataset_dir, yuv_dataset_dir):
    """
    transfer all y4m videos in y4m_dataset_dir into yuv videos stored in yuv_dataset_dir using ffmpeg.
    """
    y4m_path_list = sorted(glob.glob(os.path.join(y4m_dataset_dir, "*")))
    for y4m_path in y4m_path_list:
        yuv_name = y4m_path.split('/')[-1].split('.y4m')[0] + '.yuv'
        yuv_path = os.path.join(yuv_dataset_dir, yuv_name)
        os.system("ffmpeg -i "+y4m_path+" -vsync 0 "+yuv_path +" -y") # overwrite without asking


def set_channel(*args, n_channels=3):
    def _set_channel(img):
        if img.ndim == 2:
            img = np.expand_dims(img, axis=2)  # (H W) -> (H W C=1)

        c = img.shape[2]
        if n_channels == 1 and c == 3:
            img = np.expand_dims(sc.rgb2ycbcr(img)[:, :, 0], 2)  # only extract y channel
        elif n_channels == 3 and c == 1:
            img = np.concatenate([img] * n_channels, 2)  # copy one channel into 3 channels

        return img

    return [_set_channel(a) for a in args]


def np2Tensor(*args, rgb_range=1):
    def _np2Tensor(img):
        np_transpose = np.ascontiguousarray(img.transpose((2, 0, 1)))  # (H W C) -> (C H W)
        tensor = torch.from_numpy(np_transpose).float()
        tensor.mul_(rgb_range / 255)

        return tensor

    return [_np2Tensor(a) for a in args]


if __name__ == "__main__":
    # test yuv_import
    opt_test = False
    if opt_test:
        import cv2
        yuv_path = "F:/test_18/HM16.5_LDP/QP37/BasketballDrill_832x480_500.yuv"
        y_batch, u_batch, v_batch = yuv_import(yuv_path, height_frame=480, width_frame=832, nfs=2, startfrm=1, opt_bar=True)
        cv2.namedWindow("test", 0) # windows can be resize maunually
        cv2.imshow("test", v_batch[0]) # ICCP warning is due to the typing software. turn it off
        cv2.waitKey()
        cv2.destroyAllWindows()

    # test write_yuv
    opt_test = False
    if opt_test:
        yuv_path = "F:/test_18/HM16.5_LDP/QP37/BasketballDrill_832x480_500.yuv"
        y_frame, u_frame, v_frame = yuv_import(yuv_path, height_frame=480, width_frame=832, nfs=1, startfrm=1)  # uint8
        y_frame, = set_channel(y_frame.squeeze(0), n_channels=1)  # (C H W)
        y_frame, = np2Tensor(y_frame, rgb_range=1)  # uint8 -> torch.float32, [0,1]
        write_yuv(video_path="./test.yuv", y_frame=torch.squeeze(y_frame), u_frame=u_frame[0], v_frame=v_frame[0])
    
    # test cal_mse
    opt_test = False
    if opt_test:
        a = 100 * np.ones((2,2), dtype=np.uint8)
        b = 200 * np.ones((2,2), dtype=np.uint8)
        print(cal_mse(a,b))
    
    # test psnr calculation
    opt_test = False
    if opt_test:
        from skimage.metrics import peak_signal_noise_ratio
        a = 100 * np.ones((1,2,2), dtype=np.uint8)
        b = 200 * np.ones((1,2,2), dtype=np.uint8)
        print(cal_psnr(a,b))
        print(peak_signal_noise_ratio(a,b,data_range=255.0)) # the same
    
    # test y-psnr, u-psnr and v-psnr calculation
    opt_test = False
    if opt_test:
        cmp_yuv_path = "F:/test_18/HM16.5_LDP/QP37/BasketballDrill_832x480_500.yuv"
        raw_yuv_path = "F:/test_18/raw/BasketballDrill_832x480_500.yuv"
        for ite_frame in range(500):
            y_batch, u_batch, v_batch = yuv_import(cmp_yuv_path, height_frame=480, width_frame=832, nfs=1, startfrm=ite_frame, opt_bar=True)
            y_batch_ref, u_batch_ref, v_batch_ref = yuv_import(raw_yuv_path, height_frame=480, width_frame=832, nfs=1, startfrm=ite_frame, opt_bar=True)
            print("{:d} - {:.4f} - {:.4f} - {:.4f}".format(ite_frame+1, 
                cal_psnr(y_batch, y_batch_ref),
                cal_psnr(u_batch, u_batch_ref),
                cal_psnr(v_batch, v_batch_ref)))

    # transfer y4m in multi dir
    opt_test = False
    if opt_test:
        y4m_dataset_dir_top = "/media/x/Database/mls/dataset/"
        yuv_dataset_dir_top = "/media/x/Database/mls/dataset_yuv/"
        sub_dir_list = [
            'val_ref_part1', 'val_ref_part2',
            'val_damage_part1', 'val_damage_part2',
            'train_ref_part1', 'train_ref_part2',
            'train_ref_part3', 'train_ref_part4',
            'train_ref_part5', 'train_ref_part6',
            'train_damage_part1', 'train_damage_part2',
            'train_damage_part3', 'train_damage_part4',
            'train_damage_part5', 'train_damage_part6',
            'test_damage_A'
        ]
        for sub_dir in sub_dir_list:
            y4m_dataset_dir = os.path.join(y4m_dataset_dir_top, sub_dir)
            yuv_dataset_dir = os.path.join(yuv_dataset_dir_top, sub_dir)
            if not os.path.exists(yuv_dataset_dir):
                os.system("mkdir "+yuv_dataset_dir)
            y4m2yuv(y4m_dataset_dir, yuv_dataset_dir)
            