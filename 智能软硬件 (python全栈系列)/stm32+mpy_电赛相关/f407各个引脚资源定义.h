#define BLACK_F407ZE

#define MICROPY_HW_BOARD_NAME       "BLACK STM32F407ZE"
#define MICROPY_HW_MCU_NAME         "STM32F407ZE"

// USART1
#define MICROPY_HW_UART1_TX     (pin_A9)   // PA9,PB6
#define MICROPY_HW_UART1_RX     (pin_A10)  // PA10,PB7
//#define MICROPY_HW_UART1_RTS    (pin_A12)  // PA12
//#define MICROPY_HW_UART1_CTS    (pin_A11)  // PA11

// USART2
#define MICROPY_HW_UART2_TX     (pin_A2)  // PA2,PD5
#define MICROPY_HW_UART2_RX     (pin_A3)  // PA3,PD6
#define MICROPY_HW_UART2_RTS    (pin_A1)  // PA1,PD4
#define MICROPY_HW_UART2_CTS    (pin_A0)  // PA0,PD3

// USART3
#define MICROPY_HW_UART3_TX     (pin_D8)  // PB10,PC10,PD8
#define MICROPY_HW_UART3_RX     (pin_D9)  // PB11,PC11,PD9
#define MICROPY_HW_UART3_RTS    (pin_D12) // PB14,PD12
#define MICROPY_HW_UART3_CTS    (pin_D11) // PB13,PD11

// UART4
#define MICROPY_HW_UART4_TX     (pin_C10)  // PC10,PA0
#define MICROPY_HW_UART4_RX     (pin_C11)  // PC11,PA1

// UART5
#define MICROPY_HW_UART5_TX     (pin_C12) // PC12
#define MICROPY_HW_UART5_RX     (pin_D2)  // PD2

// USART6
#define MICROPY_HW_UART6_TX     (pin_C6) // PC6,PG14
#define MICROPY_HW_UART6_RX     (pin_C7) // PC7,PG9
#define MICROPY_HW_UART6_RTS    (pin_G8) // PG8,G12
#define MICROPY_HW_UART6_CTS    (pin_G13) // PG15,PG13

// UART7
// #define MICROPY_HW_UART7_TX     (pin_E8) // PE8,PF7
// #define MICROPY_HW_UART7_RX     (pin_E7) // PE7,PF6

// UART8
// #define MICROPY_HW_UART8_TX     (pin_E1) // PE1
// #define MICROPY_HW_UART8_RX     (pin_E0) // PE0

// I2C busses
#define MICROPY_HW_I2C1_SCL (pin_B6)  // PB8,PB6
#define MICROPY_HW_I2C1_SDA (pin_B7)  // PB9,PB7

#define MICROPY_HW_I2C2_SCL (pin_B10) // PB10,PF1
#define MICROPY_HW_I2C2_SDA (pin_B11) // PB11,PF0

#define MICROPY_HW_I2C3_SCL (pin_A8)  // PA8
#define MICROPY_HW_I2C3_SDA (pin_C9)  // PC9

// I2S busses
// I2S2_CKIN   PC9

// I2S2_CK     PB13,PB10
// I2S2_MCK    PC6
// I2S2_SD     PB15,PC3
// I2S2_WS     PB12,PB9
// I2S2ext_SD  PB14,PC2

// I2S3_CK     PB3,PC10
// I2S3_MCK    PC7
// I2S3_SD     PB5,PC12
// I2S3_WS     PA15,PA4
// I2S3ext_SD  PB4,PC11

// SPI busses
#define MICROPY_HW_SPI1_NSS  (pin_A4)  // PA4,PA15
#define MICROPY_HW_SPI1_SCK  (pin_A5)  // PA5,PB3
#define MICROPY_HW_SPI1_MISO (pin_A6)  // PA6,PB4
#define MICROPY_HW_SPI1_MOSI (pin_A7)  // PA7,PB5

#define MICROPY_HW_SPI2_NSS  (pin_B12) // PB12,PB9
#define MICROPY_HW_SPI2_SCK  (pin_B13) // PB13,PB10
#define MICROPY_HW_SPI2_MISO (pin_B14) // PB14,PC2
#define MICROPY_HW_SPI2_MOSI (pin_B15) // PB15,PC3

#define MICROPY_HW_SPI3_NSS  (pin_A15)//(pin_A15) // PA15
#define MICROPY_HW_SPI3_SCK  (pin_B3)  // PB3,PC10
#define MICROPY_HW_SPI3_MISO (pin_B4)  // PB4,PC11
#define MICROPY_HW_SPI3_MOSI (pin_B5)  // PB5,PC12

// CAN busses
#define MICROPY_HW_CAN1_TX (pin_B9) // PB9,PD1,PA12
#define MICROPY_HW_CAN1_RX (pin_B8) // PB8,PD0,PA11
#define MICROPY_HW_CAN2_TX (pin_B6) // PB6,PB13
#define MICROPY_HW_CAN2_RX (pin_B5) // PB5,PB12

// DAC
// DAC_OUT1 PA4
// DAC_OUT2 PA5

//ADC
// pc1,pc4,pc5

// KEY0 has no pullup or pulldown, and pressing the switch makes the input go low
#define MICROPY_HW_USRSW_PIN        (pin_E4)
#define MICROPY_HW_USRSW_PULL       (GPIO_PULLUP)
#define MICROPY_HW_USRSW_EXTI_MODE  (GPIO_MODE_IT_FALLING)
#define MICROPY_HW_USRSW_PRESSED    (0)

// KEY1 - no support for multiple user buttons, yet
// pin_E3

// LEDs
#define MICROPY_HW_LED1             (pin_F9)  // Yellow LED D1
#define MICROPY_HW_LED2             (pin_F10) // Yellow LED D2
// Yellow LED D3 is the power LED and always on
#define MICROPY_HW_LED_ON(pin)      (mp_hal_pin_low(pin))
#define MICROPY_HW_LED_OFF(pin)     (mp_hal_pin_high(pin))

// SD card detect switch
//	#define MICROPY_HW_SDCARD_DETECT_PIN        (pin_A8)	// nope
//	#define MICROPY_HW_SDCARD_DETECT_PULL       (GPIO_PULLUP)
//	#define MICROPY_HW_SDCARD_DETECT_PRESENT    (GPIO_PIN_RESET)
// 1      - PC10 - DAT2/RES
// 2      - PC11 - CD/DAT3/CS
// 3      - PD2  - CMD/DI
// 4      - VCC  - VDD
// 5      - PC12 - CLK/SCLK
// 6      - GND  - VSS
// 7      - PC8  - DAT0/D0
// 8      - PC9  - DAT1/RES
// 9  SW2 - GND
// 10 SW1 - GND

// USB config
#define MICROPY_HW_USB_FS (1)
// #define MICROPY_HW_USB_VBUS_DETECT_PIN (pin_A9)
// #define MICROPY_HW_USB_OTG_ID_PIN      (pin_A10)
