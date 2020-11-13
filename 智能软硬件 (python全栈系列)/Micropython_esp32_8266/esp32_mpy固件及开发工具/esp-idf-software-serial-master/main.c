/*
Github: junhuanchen
Copyright (c) 2018 Juwan
Licensed under the MIT license:
http://www.opensource.org/licenses/mit-license.php
*/

#include <stdio.h>

#include "sw_serial.h"

int app_main()
{
    SwSerial *tmp = sw_new(22, 21, false, 512);
    printf("%u\n", tmp->bitTime);
    if (tmp != NULL)
    {
        
        sw_open(tmp, 115200); // 115200 > 9600

        // puts("sw_write test");

        // for (size_t i = 0; i < 256; i++)
        // {
        //     sw_write(tmp, (uint8_t)i);
        // }
        
        puts("sw_write test");
        for (size_t i = 0; i < 127; i++)
        {
            sw_write(tmp, (uint8_t)i);
        }
        vTaskDelay(500 / portTICK_RATE_MS);

        puts("sw_write test");
        for (size_t i = 127; i < 256; i++)
        {
            sw_write(tmp, (uint8_t)i);
        }
        vTaskDelay(500 / portTICK_RATE_MS);

        while (true)
        {
            
            vTaskDelay(1000 / portTICK_RATE_MS);
            puts("check recvd data");
            int len = sw_any(tmp);
            
            if (len > 0)
            {
                for (size_t i = 0; i < len; i++)
                {
                    printf("%02X ", sw_read(tmp));
                }

                printf("\nrecv sw_any %02u %02u %02u \n", sw_any(tmp), tmp->inPos, tmp->outPos);

            }

        }
        
    }
    
    sw_del(tmp);
    return 0;
}
