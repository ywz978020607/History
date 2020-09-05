import numpy as np
import math


def yuv_import(video_path, startfrm, nfs,\
    height_frame=0, width_frame=0, bar=False, opt_clear=False):
    """
    import Y U V channels from a yuv video.

    nfs: num of frames that you need.
    startfrm: start from 0.
    
    return: Y, U, V, each with (nfs, height, width), [0, 255], uint8
    """
    fp = open(video_path, 'rb')

    ## retrieve resolution info from video path
    if height_frame == 0:
        res = video_path.split("-")[2].split("_")[0]
        width_frame = int(res.split("x")[0])
        height_frame = int(res.split("x")[1])

    ## target at startfrm
    blk_size = int(height_frame * width_frame * 3 / 2)
    fp.seek(blk_size * startfrm, 0)

    d0 = height_frame // 2
    d1 = width_frame // 2

    ## init
    y_frame = []
    y_batch = []
    u_frame = []
    u_batch = []
    v_frame = []
    v_batch = []

    ## extract
    y_size = height_frame * width_frame
    u_size = d0 * d1
    v_size = d0 * d1
    for ite_frame in range(nfs):

        y_frame = [ord(fp.read(1)) for i in range(y_size)]
        y_frame = np.array(y_frame, dtype=np.uint8).reshape((height_frame, width_frame))
        y_batch.append(y_frame)

        u_frame = [ord(fp.read(1)) for i in range(u_size)]
        u_frame = np.array(u_frame, dtype=np.uint8).reshape((d0, d1))
        u_batch.append(u_frame)
        
        v_frame = [ord(fp.read(1)) for i in range(v_size)]
        v_frame = np.array(v_frame, dtype=np.uint8).reshape((d0, d1))
        v_batch.append(v_frame)

        if bar:
            print("\r<%d, %d>" % (ite_frame, nfs-1), end="", flush=True)

    fp.close()

    if opt_clear:
        print("\r"+20*" ", end="\r", flush=True)

    y_batch = np.array(y_batch)
    u_batch = np.array(u_batch)
    v_batch = np.array(v_batch)
    return y_batch, u_batch, v_batch


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
    
    img1, img2: (H W), [0, 255], uint8
    
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
    
    return ave psnr of each channel, np.float32
    """
    assert (len(img1.shape) == 3), "len(img1.shape) != 3!"
    assert (img1.shape == img2.shape), "img1.shape != img2.shape!"
    img1, img2 = _as_floats(img1, img2) # necessary!!!
    mse_channels = [cal_mse(img1[i], img2[i]) for i in range(img1.shape[0])]
    if min(mse_channels) == 0:
        return float('inf')
    psnr_channels = [10 * math.log10(65025.0 / mse) for mse in mse_channels]
    return np.mean(psnr_channels)


if __name__ == "__main__":

    ## test yuv_import
    opt_test = False
    if opt_test:
        import cv2
        yuv_path = "F:/test_18/HM16.5_LDP/QP37/BasketballDrill_832x480_500.yuv"
        y_batch, u_batch, v_batch = yuv_import(yuv_path, height_frame=480, width_frame=832, nfs=2, startfrm=1, bar=True)
        cv2.namedWindow("test", 0) # windows can be resize maunually
        cv2.imshow("test", v_batch[0]) # ICCP warning is due to the typing software. turn it off
        cv2.waitKey()
        cv2.destroyAllWindows()
    
    ## test cal_mse
    opt_test = False
    if opt_test:
        a = 100 * np.ones((2,2), dtype=np.uint8)
        b = 200 * np.ones((2,2), dtype=np.uint8)
        print(cal_mse(a,b))
    
    ## test psnr calculation
    opt_test = False
    if opt_test:
        from skimage.metrics import peak_signal_noise_ratio
        a = 100 * np.ones((1,2,2), dtype=np.uint8)
        b = 200 * np.ones((1,2,2), dtype=np.uint8)
        print(cal_psnr(a,b))
        print(peak_signal_noise_ratio(a,b,data_range=255.0)) # the same
    
    ## test y-psnr, u-psnr and v-psnr calculation
    opt_test = False
    if opt_test:
        cmp_yuv_path = "F:/test_18/HM16.5_LDP/QP37/BasketballDrill_832x480_500.yuv"
        raw_yuv_path = "F:/test_18/raw/BasketballDrill_832x480_500.yuv"
        for ite_frame in range(500):
            y_batch, u_batch, v_batch = yuv_import(cmp_yuv_path, height_frame=480, width_frame=832, nfs=1, startfrm=ite_frame, bar=True)
            y_batch_ref, u_batch_ref, v_batch_ref = yuv_import(raw_yuv_path, height_frame=480, width_frame=832, nfs=1, startfrm=ite_frame, bar=True)
            print("{:d} - {:.4f} - {:.4f} - {:.4f}".format(ite_frame+1, 
                cal_psnr(y_batch, y_batch_ref),
                cal_psnr(u_batch, u_batch_ref),
                cal_psnr(v_batch, v_batch_ref)))
            