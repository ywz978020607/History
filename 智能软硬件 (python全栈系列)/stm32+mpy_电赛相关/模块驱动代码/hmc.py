from machine import Pin

class HMC():
    def __init__(self):
        self.com=[{},{},{}]
        # for ii in range(6):
        #     if ii<5:
        #         self.com[0][ii] = Pin('PG'+str(ii+11),Pin.OUT)
        #     else:
        #         self.com[0][ii] = Pin('PB3',Pin.OUT)

        #     self.com[1][ii] = Pin('PB'+str(ii+4),Pin.OUT)
        self.com[0][0]=Pin('PB9',Pin.OUT)
        self.com[0][1]=Pin('PB8',Pin.OUT)
        self.com[0][2]=Pin('PB7',Pin.OUT)
        self.com[0][3]=Pin('PB6',Pin.OUT)
        self.com[0][4]=Pin('PA14',Pin.OUT)
        self.com[0][5]=Pin('PA13',Pin.OUT)
        self.set_all_high(0)

        self.com[1][0]=Pin('PD7',Pin.OUT)
        self.com[1][1]=Pin('PD6',Pin.OUT)
        self.com[1][2]=Pin('PD5',Pin.OUT)
        self.com[1][3]=Pin('PD4',Pin.OUT)
        self.com[1][4]=Pin('PD3',Pin.OUT)
        self.com[1][5]=Pin('PD2',Pin.OUT)
        self.set_all_high(1)

        self.com[2][0]=Pin('PD15',Pin.OUT)
        self.com[2][1]=Pin('PD14',Pin.OUT)
        self.com[2][2]=Pin('PD13',Pin.OUT)
        self.com[2][3]=Pin('PD12',Pin.OUT)
        self.com[2][4]=Pin('PD11',Pin.OUT)
        self.com[2][5]=Pin('PD10',Pin.OUT)
        self.set_all_high(2)


        

    def set_all_high(self,pick):
        for ii in range(6):
            self.com[pick][ii].on()

    def set_all_low(self,pick):
        for ii in range(6):
            self.com[pick][ii].off()
    
    
    def set_low(self,pick,num_list):
        self.set_all_high(pick)
        for ii in range(len(num_list)):
            self.com[pick][num_list[ii]].off()

######################################################

    def set_val(self,pick,val_list):
        for ii in range(6):
            self.com[pick][ii].value(val_list[ii])

    def set_val_on(self,pick,num):
        val = bin(int(num))
        self.set_all_low(pick)
        for ii in range(len(val-2)):
            if val[-1-ii] == '1':
                self.com[pick][ii].on()