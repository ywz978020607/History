//http://www.51hei.com/bbs/dpj-30516-1.html
//接拨电话
//    其他,错误代码
u8 sim900a_call_test(void)
{
        u8 key;
        u16 lenx;
        u8 callbuf[20];
    u8 wangyan[]={"13476852658"};//向自己的手机拨号,因为程序中是把手机号码当作字符处理，所以要加英文引号
        u8 pohnenumlen=0;        //号码长度,最大15个数，如 callbuf[pohnenumlen]; usart通信时电话号码就是ASCII码；
        u8 *p,*p1,*p2;
        u8 oldmode=0;
        u8 cmode=0;        /*模式0:等待拨号；模式1:拨号中；模式2:通话中；模式3:接收到来电，共4种情况 */
        LCD_Clear(WHITE);
        if(sim900a_send_cmd("AT+CLIP=1","OK",200))return 1;        //设置来电显示
        if(sim900a_send_cmd("AT+COLP=1","OK",200))return 2;        //设置被叫号码显示
        p1=mymalloc(SRAMIN,20);        //申请20个字节直接用于存放SIM900A模块返回的来电电话号码，usart通信时电话号码就是ASCII码；
        if(p1==NULL)return 2;       
        POINT_COLOR=RED;
        Show_Str_Mid(0,30,"ATK-SIM900A 拨号测试",16,240);                                             
        Show_Str(40,70,200,16,"请拨号:",16,0);
        kbd_fn_tbl[0]="拨号";
        kbd_fn_tbl[1]="返回";
        sim900a_load_keyboard(0,180,(u8**)kbd_tbl1);/*加载拨号键盘界面，由此可见进入什么功能就加载相应的界面*/

        POINT_COLOR=BLUE;
        while(1)
        {   if(KEY_LEFT==KEY_Scan(0)) u2_printf("ATD%s;\r\n",wangyan);
                delay_ms(10);
                if(USART2_RX_STA&0X8000)        /*以下凡是受此if语句控制范围的语句都是基于已经接收到sim900a模块返回的数据，*/
                {
                        sim_at_response(0); /* mode:0,不清零USART2_RX_STA; 将收到的来自sim900a模块的AT指令应答数据返回给电脑串口 */

                        if(cmode==1||cmode==2)/*首次进入时cmode为0，模式0:等待拨号；模式1:拨号中；模式2:通话中；模式3:接收到来电  */
                        {/* 首先发送：ATE1，设置回显，再发送：AT+COLP=1，设置被叫号码显示。然后发送：ATD10086;，拨打10086，在接通后，SIM900A模块返回：+COLP: "10086",129,"",""，此时，我们就可以听到中国移动那熟悉的声音了….待一堆废话结束后，我们发送：AT+VTS=1，即可查询本机电话号码。最后，通过发送：ATH，挂断，结束本次 */
                 if(cmode==1)if(sim900a_check_cmd("+COLP:"))cmode=2;        //拨号成功
                                if(sim900a_check_cmd("NO CARRIER"))cmode=0;        //拨号失败
                                if(sim900a_check_cmd("NO ANSWER"))cmode=0;        //拨号失败
                                if(sim900a_check_cmd("ERROR"))cmode=0;                //拨号失败
                        }
                        if(sim900a_check_cmd("+CLIP:")) /*接收到来电， 如果返回值是+CLIP:则表示接收到来电 */
                        {/*"+CLIP:"的含义是：设置提示来电号码，带来电显示时的返回值格式是："+CLIP:（<n>取值列表） " 参考AT命令手册P59
                      AT+CLIP用于设置来电显示，通过发送：AT+CLIP=1，可以实现设置来电显示功能，模块接收到来电的时候，会返回来电号码。并且可以在串口接收到来电号码，如：+CLIP: "02038271790",161,"",,"ALIENTEK",0，表示当前接入号码为：02038271790。
此时，我们发送：ATA，即可接听来电，并进行通话。当对方挂断电话的时候，SIM900A模块会返回：NO CARRIER，并结束此次通话;当然，我们也可以通过发送：ATH，来主动结束通话。*/
                                cmode=3; /* 模式0:等待拨号；模式1:拨号中；模式2:通话中；模式3:接收到来电  */
                                p=sim900a_check_cmd("+CLIP:"); /* 将接收到的"+CLIP:"字符串（即来自模块返回值）存储到P */
                                p+=8; /*将模块返回的来电号码存储在（P+8）处，p+8,就是偏移8个字节,不是一共8个内存空间 */
                            p2=(u8*)strstr((const char *)p,"\"");/*在（P+8）处开始，找到第一个出现“\”符号（每个字符串结束符      
                                             都有“\”符号）的位置，实际上就是从模块返回值中取得电话号码；并将电话号码存储到P2开始处*/
                 p2[0]=0; /*添加结束符。字符串的结束符是'\0' 也是0；p2=(u8*)strstr((const char*)(p1),","); 指定结束符的位置 */
                                /*上面两步的作用是给字符串加上“\0”这个字符串末尾标志  */
                                strcpy((char*)p1,(char*)p);/* 字符串P复制到P1，用于下面case3语句显示 */

                        }
                        USART2_RX_STA=0; /*将接收到的数据清零，以便让串口2再次进入中断执行“if(USART2_RX_STA==0)TIM4_Set(1)”语句*/
                } /*对sim900a返回值的处理部分到此结束 ;*/
/* 上面部分的语句主要是对sim900a返回值的处理，并根据返回值的情况定义4种工作状态：模式0:等待拨号；模式1:拨号中；模式2:通话中；模式3:接收到来电 */               

         key=sim900a_get_keynum(0,180);/* 检测是哪个触摸键被按下，下面根据对触摸键触摸情况、对相关功能进行处理 */
                if(key)  /* 下面的操作都是基于触摸键有被按下  */
                {
                        if(key<13)
                        {
                           if(cmode==0&&pohnenumlen<15) /*模式0：等待拨号且pohnenumlen对应的键值小于15，首次进入时是0 */
                           {
                                 callbuf[pohnenumlen++]=kbd_tbl[key-1][0];/*执行pohnenumlen++的条件是必须有触摸键按下 */
       /* 二维数组kbd_tbl[key-1][0]实际上等价于kbd_tbl[key-1]；本句的作用是将被按下的触屏键值即对应的字符存储到callbuf[pohnenumlen++]  */
               /* 假设i=3，j=1，则key==11即key[1][3]：x轴第二格，y轴第4格，该处就是存放“11” */
                                 u2_printf("AT+CLDTMF=2,\"%c\"\r\n",kbd_tbl[key-1][0]);
/* "AT+CLDTMF=2参考AT命令手册P126，测试DTMF音，时长2秒 ，将命令和键值发送给模块，功能：每拨一个数字键（只对0-9号数字键有效）耳机发出相应的拨号音*/
                                }else if(cmode==2)//通话中，主叫拨通了通话中
                                {
                                        u2_printf("AT+CLDTMF=2,\"%c\"\r\n",kbd_tbl[key-1][0]);
                                        delay_ms(100);
                                        u2_printf("AT+VTS=%c\r\n",kbd_tbl[key-1][0]);
                                        LCD_ShowChar(40+56,90,kbd_tbl[key-1][0],16,0);
                      /*在“请拨号”后面显示按下的键值，即显示拨号键 */
                                }
                        }else
                        {
                                if(key==13)if(pohnenumlen&&cmode==0)pohnenumlen--;
   /*删除；1，如果pohnenumlen==0，则说明callbuf[pohnenumlen]数组中没有存放任何号码，所以就不必执行“pohnenumlen--;”  2，“cmode==0”即等待拨号模式；3，通过对数组下表的加减就可以增删数组元素；如，本例中通过执行“pohnenumlen--;”操作，就将callbuf[pohnenumlen]数组元素做了增删，重要！ */
                                if(key==14)//执行拨号
                                {
                                        if(cmode==0)/*拨号模式；如果按了拨号键且处于等待拨号模式  */
                                        {
                                                callbuf[pohnenumlen]=0;/*最后加入结束符, 字符串结束符是“\0”也是“0” */
                                          //        u2_printf("ATD%s;\r\n",callbuf);/*拨号，号码就是callbuf存储的内容 */
                          u2_printf("ATD%s;\r\n",wangyan);
                     /*给自己拨号拨号，号码就是wangyan存储的内容即13476852658；当按下“拨号”键时，相应的手机就接到了本机的来电 */
                                                cmode=1;         //拨号中模式1:57:01星期三 2014年8月6日
                                        }else /* 如果按了拨号键key14*/
                                        {
                                                sim900a_send_cmd("ATH","OK",200);//挂机
                                                cmode=0; /*将工作模式设置为等待拨号模式  */
                                        }
                                }
                                if(key==15) /* 在通话测试模式中key15就是“接听”  */
                                {
                                        if(cmode==3) /*如果按下“接听”键且处于“接听中”(cmode==3) 模式 */
                                        {/* 接收到来电；上面有“if(sim900a_check_cmd("+CLIP:"))”语句，所以只要有电话打进来，cmode就会等于3！*/
                                                sim900a_send_cmd("ATA","OK",200);/*发送应答指令，ATA，即可接听来电*/
                                                Show_Str(40+56,70,200,16,callbuf,16,0);/*显示来电号码,本句是否有问题？ */
                                                cmode=2; /* 设置为模式2:通话中 */
                                        }else  /* 如果没有电话打进来，触摸15键则会执行“break;”退出while大循环回到主函数界面，*/
                                        {
                                                sim900a_send_cmd("ATH",0,0); /* 不管有没有在通话,都结束通话即挂机 */
                                                break;/*退出循环，执行“myfree(SRAMIN,p1);”语句*/
                                        }
                                }
                        }
                        if(cmode==0)//只有在等待拨号模式有效
                        { /* “callbuf[pohnenumlen]=0; ”这一句非常重要！该句确保每拨一个字符都能正确的显示 */
                                callbuf[pohnenumlen]=0; /*该句作用是每按一下拨号键就在相应的键值后加一个结束符，用以显示在LCD上 */
                                LCD_Fill(40+56,70,239,70+16,WHITE);
                                Show_Str(40+56,70,200,16,callbuf,16,0);/*将每个拨号键值显示出来 */         
                        }                               
                }
                if(oldmode!=cmode)//模式变化了，只要cmode不等于0模式就会进入下面语句
                {
                        switch(cmode)
                        {
                                case 0:
                                        kbd_fn_tbl[0]="拨号";
                                        kbd_fn_tbl[1]="返回";
                                        POINT_COLOR=RED;
                                        Show_Str(40,70,200,16,"请拨号:",16,0);  
                                        LCD_Fill(40+56,70,239,70+16,WHITE);
                                        if(pohnenumlen)
                                        {
                                                POINT_COLOR=BLUE;
                                                Show_Str(40+56,70,200,16,callbuf,16,0);
                                        }
                                        break;
                                case 1:
                                        POINT_COLOR=RED;
                                        Show_Str(40,70,200,16,"拨号中:",16,0);
                                        pohnenumlen=0;//将电话号码清零
                                case 2:
                                        POINT_COLOR=RED;
                                        if(cmode==2)Show_Str(40,70,200,16,"通话中:",16,0);
                                        kbd_fn_tbl[0]="挂断";
                                        kbd_fn_tbl[1]="返回";        
                                        break;
                                case 3:
                                        POINT_COLOR=RED;
                                        Show_Str(40,70,200,16,"有来电:",16,0);
                                        POINT_COLOR=BLUE;
                                        Show_Str(40+56,70,200,16,p1,16,0); //显示来电
                                        kbd_fn_tbl[0]="挂断";
                                        kbd_fn_tbl[1]="接听";
                                        break;                               
                        }
                        if(cmode==2)Show_Str(40,90,200,16,"DTMF音:",16,0);//通话中,可以通过键盘输入DTMF音
                        else LCD_Fill(40,90,120,90+16,WHITE);
                        sim900a_load_keyboard(0,180,(u8**)kbd_tbl1); //显示键盘
                        oldmode=cmode; /*退出“switch(cmode)”语句，确保界面处于一种稳定的与cmode值对应的模式 */
                }/*假设cmode==2“通话中模式”，根据通话的具体情况cmode会得到不同的值，这样就又可以进入“switch(cmode)”语句了。  */
                if((lenx%50)==0)LED0=!LED0;                                              
                lenx++;         
        }
        myfree(SRAMIN,p1);
        return 0;
}
/*
1，u8 sim900a_call_test(void)函数总结：该函数可以接听拨打电话测试，是该模块的核心函数之一，里面的算法以及c语言运用技巧都值得不断温故；可以分为2个部分:
1），按下key0键，做一些拨打电话之前的准备工作让sim900a模块进入工作状态并加载触摸屏界面；首次进入该函数时，把cmode设置为等待拨号模式；
2），该部分包含在一个while大循环里，这个while大循环就是该函数的核心，为了便于分析该函数，将while循环的功能细分为；a），以“if(USART2_RX_STA&0X8000)”语句为控制范围的内容，它的主要功能是假设收到了来自sim900a模块的AT指令应答数据即模块返回数据，基于此并根据接收到的返回值含义把sim900a模块定义为4种工作模式：模式cmode0:等待拨号；模式cmode1:拨号中；模式cmode2:通话中；模式cmode3:接收到来电；而后面程序的操作就是围绕这四种工作模式不断变化使LCD界面适应相应的操作需求以便于主机发出相应的命令；如果sim900a模块接收到来电就会向串口返回相应的数据和来电电话号码，程序就将sim900a模块设置为cmode3即接听模式并将来电号码显示在LCD；如果是拨号中或通话中模式，则根据sim900a模块的返回值将cmode设置为相应的工作模式值；b）接着就是根据某个触摸键是否按下即根据获得的触摸键值key执行向sim900a模块发出相应的AT指令，同时将cmode定义为相应的工作模式值，以便于下一步操作；c），根据cmode模式值执行相应的switch语句内容。
*/