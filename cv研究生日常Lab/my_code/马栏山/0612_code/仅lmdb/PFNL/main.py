import os
import sys
import shutil

from model.pfnl import PFNL

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
    
if __name__=='__main__':
    """
    para1: class __init__ definition
    para2: forward
    para3: below
    """
    tab = sys.argv[1]  # 0609
    
    """
    train
    """
    opt_train = True
    if opt_train == True:

        flag_first = False  # clear log and existing models   ##### True!!!!!!!!!!
        flag_down = True  # drop lr when collasp    ##### False!!!!!!!!!
        
        while True:
            """
            instantize, refresh the class vars
            """
            model = PFNL(tab=tab)

            """
            if it is the first time, and folder exists, delect and recreate it
            """
            if flag_first == True:
                if os.path.exists(model.model_dir):
                    shutil.rmtree(model.model_dir, ignore_errors=True)
                    os.makedirs(model.model_dir)
                flag_first = False
            
            """
            drop lr
            """
            if flag_down == True:
                model.learning_rate /= 2
                model.end_lr /= 2
                flag_down = False
            
            """
            log
            """
            with open(model.log_path, 'a+') as f:
                f.write(str(vars(model)) + "\n")
            
            """
            train
            """
            break_flag = model.train()
            
            if break_flag == True:  # collasp
                if model.learning_rate > 1e-4:
                    flag_down = True
                print("keep training.")
                continue
            elif break_flag == False:  # return None
                print("done or OOM.")
                break
        
    """
    test
    """
    opt_test = False
    if opt_test:
        model = PFNL(tab=tab)
        # log
        with open(model.log_path, 'w') as f:
            f.write(str(vars(model)) + "\n")

        start_vid = int(sys.argv[2])  # 0, start from 0
        end_vid = int(sys.argv[3])  # 149
        
        model.test_videos(
            root_dir='xxx.lmdb',
            save_dir='/home/xql/projects/mls/dataset_png/refine',
            save_tag=tab,
            start_vid=start_vid,
            end_vid=end_vid,
            )
