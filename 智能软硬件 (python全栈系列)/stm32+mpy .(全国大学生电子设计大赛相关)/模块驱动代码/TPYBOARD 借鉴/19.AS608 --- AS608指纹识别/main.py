import as608

fig=as608.FIG(4)

fig.savefig(37)
user=fig.disfig()
if(user==0):
	print('无法识别')
else :
	print('找到用户',user)