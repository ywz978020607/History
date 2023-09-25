ch9329_utils = {}

_G.sys = require("sys")
-- sys.wait(1000)
-- local uartid = 1 -- 根据实际设备选取不同的uartid
-- --初始化
-- local result = uart.setup(
--     uartid,--串口id
--     9600,--波特率
--     8,--数据位
--     1--停止位
-- )
-- -- uart.write(uartid, cache_data)

function ch9329_utils.mysplit (inputstr, sep)
    if sep == nil then
        sep = "%s"
    end
    local t={}
    for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
        table.insert(t, str)
    end
    return t
end
function ch9329_utils.list2bytes(inputlist)
    local res = ''
    for i = 1, #inputlist do
        res = res .. string.char(inputlist[i])
    end
    return res
end

function ch9329_utils.cal_sum(bytes_in)
    local sum = 0
    for i = 1, #bytes_in do
        sum = (sum + string.byte(bytes_in, i)) & 0xff
    end
    return string.char(sum)
end

function ch9329_utils.get_mouse_cmd(mode, speed)
    speed = speed or 5 -- tonumber()
    local mouse_prefix = '\x57\xab\x00\x05\x05\x01'
    local mouse_release = mouse_prefix .. '\x00\x00\x00\x00'
    local cmd_mouse = {
        mkl = '\x01\x00\x00\x00',
        mkr = '\x02\x00\x00\x00',
        -- 右下为正
        mup = '\x00\x00' .. string.char((-speed) & 0xff) .. '\x00',
        mdown = '\x00\x00' .. string.char((speed) & 0xff) .. '\x00',
        mleft = '\x00' .. string.char((-speed) & 0xff) .. '\x00\x00',
        mright = '\x00' .. string.char((speed) & 0xff) .. '\x00\x00',
        msup = '\x00\x00\x00' .. string.char((-speed) & 0xff),
        msdown = '\x00\x00\x00' .. string.char((speed) & 0xff),
    }
    local res = {mouse_prefix .. cmd_mouse[mode]}
    if mode == "mkl" or mode ==  "mkr" then
        table.insert(res, mouse_release)
    end
    return res
end


function ch9329_utils.get_usb_key_cmd(keys, alt, shift, need_vuc) -- #六键无冲
    -- note: keys = "strs" 逐字符访问!!
    if alt == nil then alt = false end
    if shift == nil then shift = false end
    if need_vuc == nil then need_vuc = false end
    --
    local kb_prefix = '\x57\xab\x00\x02\x08'
    local _release_all_key = kb_prefix .. '\x00\x00\x00\x00\x00\x00\x00\x00'
    local svuc = kb_prefix .. '\x00\x00\x19\x18\x06\x00\x00\x00'
    local slshift = kb_prefix .. '\x02\x00\x00\x00\x00\x00\x00\x00'
    local __DICT_KEY_NORMAL= {
        ["esc"]=0x29,--Esc
        ["f1"]=0x3a,--F1
        ["f2"]=0x3b,--F2
        ["f3"]=0x3c,--F3
        ["f4"]=0x3d,--F4
        ["f5"]=0x3e,--F5
        ["f6"]=0x3f,--F6
        ["f7"]=0x40,--F7
        ["f8"]=0x41,--F8
        ["f9"]=0x42,--F9
        ["f10"]=0x43,--F10
        ["f11"]=0x44,--F11
        ["f12"]=0x45,--F12
        ["log.infoscreen"]=0x46,--log.info
        ["scrolllock"]=0x47,--ScrollLock
        ["pausebreak"]=0x48,--PauseBreak
        ["`"]=0x35,--`
        ["1"]=0x1e,--1
        ["2"]=0x1f,--2
        ["3"]=0x20,--3
        ["4"]=0x21,--4
        ["5"]=0x22,--5
        ["6"]=0x23,--6
        ["7"]=0x24,--7
        ["8"]=0x25,--8
        ["9"]=0x26,--9
        ["0"]=0x27,--0
        ["-"]=0x2d,---
        ["="]=0x2e,--=
        ["~"]=0x35,--~
        ["!"]=0x1e,--!
        ["@"]=0x1f,--@
        ["--"]=0x20,--#
        ["$"]=0x21,--$
        ["%"]=0x22,--%
        ["^"]=0x23,--^
        ["&"]=0x24,--&
        ["*"]=0x25,--*
        ["("]=0x26,--(
        [")"]=0x27,--)
        ["_"]=0x2d,--_
        ["+"]=0x2e,--+
        ["backspace"]=0x2a,--Backspace
        [" "]=0x2a,--Backspace
        ["tab"]=0x2b,--Tab
        ["q"]=0x14,--q
        ["w"]=0x1a,--w
        ["e"]=0x08,--e
        ["r"]=0x15,--r
        ["t"]=0x17,--t
        ["y"]=0x1c,--y
        ["u"]=0x18,--u
        ["i"]=0x0c,--i
        ["o"]=0x12,--o
        ["p"]=0x13,--p
        ["["]=0x2f,--[
        ["]"]=0x30,--]
        ["\\"]=0x31,--\
        ["Q"]=0x14,--Q
        ["W"]=0x1a,--W
        ["E"]=0x08,--E
        ["R"]=0x15,--R
        ["T"]=0x17,--T
        ["Y"]=0x1c,--Y
        ["U"]=0x18,--U
        ["I"]=0x0c,--I
        ["O"]=0x12,--O
        ["P"]=0x13,--P
        ["{"]=0x2f,--{
        ["}"]=0x30,--}
        ["|"]=0x31,--|
        ["caps"]=0x39,--Caps
        ["a"]=0x04,--a
        ["s"]=0x16,--s
        ["d"]=0x07,--d
        ["f"]=0x09,--f
        ["g"]=0x0a,--g
        ["h"]=0x0b,--h
        ["j"]=0x0d,--j
        ["k"]=0x0e,--k
        ["l"]=0x0f,--l
        [";"]=0x33,--;
        ["'"]=0x34,--'
        ["A"]=0x04,--A
        ["S"]=0x16,--S
        ["D"]=0x07,--D
        ["F"]=0x09,--F
        ["G"]=0x0a,--G
        ["H"]=0x0b,--H
        ["J"]=0x0d,--J
        ["K"]=0x0e,--K
        ["L"]=0x0f,--L
        [":"]=0x33,--:
        ["\""]=0x34,--"
        ["enter"]=0x28,--Enter
        ["z"]=0x1d,--z
        ["x"]=0x1b,--x
        ["c"]=0x06,--c
        ["v"]=0x19,--v
        ["b"]=0x05,--b
        ["n"]=0x11,--n
        ["m"]=0x10,--m
        [","]=0x36,--,
        ["."]=0x37,--.
        ["/"]=0x38,--/
        ["Z"]=0x1d,--Z
        ["X"]=0x1b,--X
        ["C"]=0x06,--C
        ["V"]=0x19,--V
        ["B"]=0x05,--B
        ["N"]=0x11,--N
        ["M"]=0x10,--M
        ["<"]=0x36,--<
        [">"]=0x37,-->
        ["?"]=0x38,--?
        ["space"]=0x2c,--Space
        [" "]=0x2c,--Space
        ["app"]=0x65,--App
        ["menu"]=0x65,--Menu
        ["insert"]=0x49,--Insert
        ["delete"]=0x4c,--Delete
        ["home"]=0x4a,--Home
        ["end"]=0x4d,--End
        ["pageup"]=0x4b,--PageUp
        ["pagedown"]=0x4e,--PageDown
        ["left"]=0x50,--Left
        ["up"]=0x52,--Up
        ["right"]=0x4f,--Right
        ["down"]=0x51,--Down
        ["numlock"]=0x53,--NumLock
        ["numpad/"]=0x54,--Numpad /
        ["numpad*"]=0x55,--Numpad *
        ["numpad-"]=0x56,--Numpad -
        ["numpad+"]=0x57,--Numpad +
        ["numpadenter"]=0x58,--Numpad Enter
        ["numpad1"]=0x59,--Numpad 1
        ["numpad2"]=0x5a,--Numpad 2
        ["numpad3"]=0x5b,--Numpad 3
        ["numpad4"]=0x5c,--Numpad 4
        ["numpad5"]=0x5d,--Numpad 5
        ["numpad6"]=0x5e,--Numpad 6
        ["numpad7"]=0x5f,--Numpad 7
        ["numpad8"]=0x60,--Numpad 8
        ["numpad9"]=0x61,--Numpad 9
        ["numpad0"]=0x62,--Numpad 0
        ["numpad."]=0x63,--Numpad .
        }

    local temp_cmd = {} -- len=8
    for i = 1, 8 do temp_cmd[i] = 0x00 end
    if alt then
        temp_cmd[1] = temp_cmd[1] + 4
    end
    if shift then
        temp_cmd[1] = temp_cmd[1] + 2
    end
    local return_cmd = {}
    if need_vuc then
        return_cmd = {svuc, _release_all_key}
    else
        return_cmd = {slshift, _release_all_key}
    end

    local pressed = {}
    local idx = 3
    for i = 1, #keys do
        local key = string.sub(keys, i, i)
        if pressed[key] ~= nil then
            pressed = nil
            pressed = {}
            -- 添加之前的
            table.insert(return_cmd, kb_prefix .. ch9329_utils.list2bytes(temp_cmd))
            table.insert(return_cmd, _release_all_key)
            -- 重置
            for j = 3, 8 do
                temp_cmd[j] = 0x00
            end
            idx = 3
        end
        if __DICT_KEY_NORMAL[key] ~= nil then
            temp_cmd[idx] = __DICT_KEY_NORMAL[key]
        else
            -- temp_cmd[idx] = key[0]
            log.info("error: key not exists:", key)
            log.info(tostring(key[0]))
        end
        pressed[key] = true
        idx = idx + 1
    end
    if need_vuc then
        temp_cmd[8] = 0x2c
        table.insert(return_cmd, kb_prefix .. ch9329_utils.list2bytes(temp_cmd))
        table.insert(return_cmd, _release_all_key)
    else
        table.insert(return_cmd, kb_prefix .. ch9329_utils.list2bytes(temp_cmd))
        table.insert(return_cmd, slshift)
        table.insert(return_cmd, _release_all_key)
    end
    return return_cmd
end
-- out_cmd = ch9329_utils.get_usb_key_cmd("672c", false, false, true)

function ch9329_utils.run_send(uartid, list_cmd)
    for i = 1, #list_cmd do
        sys.wait(100)
        uart.write(uartid, list_cmd[i] .. ch9329_utils.cal_sum(list_cmd[i]))
        -- log.info(string.toHex(list_cmd[i] .. ch9329_utils.cal_sum(list_cmd[i])))
    end
end

function ch9329_utils.deal_input_dict(uartid, get_data)
    if get_data['mode'] == 'kb' then
        context = tostring(get_data['context'])
        context_list = ch9329_utils.mysplit(context, '\\u')
        for i = 1, #context_list do
            data = context_list[i]
            if #data == 4 then
                ch9329_utils.run_send(uartid, ch9329_utils.get_usb_key_cmd(data, false, false, true))
            elseif #data > 0 then
                ch9329_utils.run_send(uartid, ch9329_utils.get_usb_key_cmd(data))
            end
        end
    else
        ch9329_utils.run_send(uartid, ch9329_utils.get_mouse_cmd(get_data['mode'], math.modf(get_data["speed"] or 5)))
    end
end



return ch9329_utils