::逐帧计算两个视频的Y U V通道的PSNR，输出到stats_file指定文件（如psnr.log）；注意log中帧数从1开始
ffmpeg -s 832x480 -i F:\test_18\HM16.5_LDP\QP37\BasketballDrill_832x480_500.yuv -s 832x480 -i F:\test_18\raw\BasketballDrill_832x480_500.yuv -lavfi psnr="stats_file=psnr.log" -f null -
pause