; Alt + i/k/j/l 分别为鼠标指针的上下左右移动
!i::MouseMove, 0, -10, 0, R  ; 向上移动 10 像素
!k::MouseMove, 0, 10, 0, R   ; 向下移动 10 像素
!j::MouseMove, -10, 0, 0, R  ; 向左移动 10 像素
!l::MouseMove, 10, 0, 0, R   ; 向右移动 10 像素

; Alt + e 和 Alt + d 分别为鼠标滚轮上滚和下滚
!e::MouseClick, WheelUp       ; 滚轮向上滚动
!d::MouseClick, WheelDown     ; 滚轮向下滚动

; Alt + s 和 Alt + f 分别为左键和右键点击
!s::MouseClick, left          ; 左键点击
!f::MouseClick, right         ; 右键点击
