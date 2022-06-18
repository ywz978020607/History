import sys
import torch
import matplotlib
import matplotlib.pyplot as plt

def plot_train(log_file = "../mytry/train_log.txt"):
    f = open(log_file, 'r')
    data = f.readlines()
    f.close()
    loss_list = []
    for line in range(len(data)):
        loss = float(data[line].split(":")[2].split("|")[0].strip())
        loss_list.append(loss)
    matplotlib.use('Agg')  # tmux专用  不报错
    plt.plot(loss_list)
    plt.savefig('train_loss.png')
    print("plot successfully.")

if __name__=='__main__':
    if len(sys.argv)>1:
        plot_train(sys.argv[1])
    else:
        plot_train()

# log_file = "/home/ywz/remote/CompressAI-master/ywz/mytry/train_log.txt"
# f = open(log_file,'r')
# data = f.readlines()
# f.close()
# loss_list = []
# for line in range(len(data)):
#     loss = data[line].split(":")[2].split("|")[0].strip()
#     loss_list.append(loss)
# matplotlib.use('Agg') #tmux专用  不报错
# plt.plot(loss_list)
# plt.savefig('train_loss.png')
# print("plot successfully.")

