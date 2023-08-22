
-- LuaTools需要PROJECT和VERSION这两个信息
PROJECT = "httpdemo"
VERSION = "1.0.0"

--[[
本demo需要http库, 大部分能联网的设备都具有这个库
http也是内置库, 无需require
]]

-- onenet
product_id = "1063477156"
api_key = "2kJV69eUrcMgCLjkyOzT8k1WY0Y="

-- sys库是标配
_G.sys = require("sys")
--[[特别注意, 使用http库需要下列语句]]
_G.sysplus = require("sysplus")
_G.http_onenet = require("http_onenet")

---- MultipartForm上传文件
-- url string 请求URL地址
-- req_headers table 请求头
-- params table 需要传输的数据参数
local function postMultipartFormData(url, params)
    local boundary = "----WebKitFormBoundary"..os.time()
    local req_headers = {
        ["Content-Type"] = "multipart/form-data; boundary="..boundary,
    }
    local body = {}

    -- 解析拼接 body
    for k,v in pairs(params) do
        if k=="texts" then
            local bodyText = ""
            for kk,vv in pairs(v) do
                print(kk,vv)
                bodyText = bodyText.."--"..boundary.."\r\nContent-Disposition: form-data; name=\""..kk.."\"\r\n\r\n"..vv.."\r\n"
            end
            table.insert(body, bodyText)
        elseif k=="files" then
            local contentType =
            {
                txt = "text/plain",             -- 文本
                jpg = "image/jpeg",             -- JPG 格式图片
                jpeg = "image/jpeg",            -- JPEG 格式图片
                png = "image/png",              -- PNG 格式图片   
                gif = "image/gif",              -- GIF 格式图片
                html = "image/html",            -- HTML
                json = "application/json"       -- JSON
            }
            
            for kk,vv in pairs(v) do
                if type(vv) == "table" then
                    for i=1, #vv do
                        print(kk,vv[i])
                        table.insert(body, "--"..boundary.."\r\nContent-Disposition: form-data; name=\""..kk.."\"; filename=\""..vv[i]:match("[^%/]+%w$").."\"\r\nContent-Type: "..contentType[vv[i]:match("%.(%w+)$")].."\r\n\r\n")
                        table.insert(body, io.readFile(vv[i]))
                        table.insert(body, "\r\n")
                    end
                else
                    print(kk,vv)
                    table.insert(body, "--"..boundary.."\r\nContent-Disposition: form-data; name=\""..kk.."\"; filename=\""..vv:match("[^%/]+%w$").."\"\r\nContent-Type: "..contentType[vv:match("%.(%w+)$")].."\r\n\r\n")
                    table.insert(body, io.readFile(vv))
                    table.insert(body, "\r\n")
                end
            end
        end
    end 
    table.insert(body, "--"..boundary.."--\r\n")
    body = table.concat(body)
    log.info("headers: ", "\r\n" .. json.encode(req_headers), type(body))
    log.info("body: " .. body:len() .. "\r\n" .. body)
    local code, headers, body = http.request("POST",url,
            req_headers,
            body
    ).wait()   
    log.info("http.post", code, headers, body)
end


sys.taskInit(function()
    -----------------------------
    -- 统一联网函数, 可自行删减
    ----------------------------
    if rtos.bsp():startsWith("ESP32") then
        -- wifi 联网, ESP32系列均支持
        local ssid = "uiot"
        local password = "12345678"
        log.info("wifi", ssid, password)
        -- TODO 改成esptouch配网
        LED = gpio.setup(12, 0, gpio.PULLUP)
        wlan.init()
        wlan.setMode(wlan.STATION)
        wlan.connect(ssid, password, 1)
        local result, data = sys.waitUntil("IP_READY", 30000)
        log.info("wlan", "IP_READY", result, data)
        device_id = wlan.getMac()
    elseif rtos.bsp() == "AIR105" then
        -- w5500 以太网, 当前仅Air105支持
        w5500.init(spi.HSPI_0, 24000000, pin.PC14, pin.PC01, pin.PC00)
        w5500.config() --默认是DHCP模式
        w5500.bind(socket.ETH0)
        LED = gpio.setup(62, 0, gpio.PULLUP)
        sys.wait(1000)
        -- TODO 获取mac地址作为device_id
    elseif rtos.bsp() == "EC618" then
        -- Air780E/Air600E系列
        --mobile.simid(2)
        LED = gpio.setup(27, 0, gpio.PULLUP)
        device_id = mobile.imei()
        log.info("ipv6", mobile.ipv6(true))
        sys.waitUntil("IP_READY", 30000)
    end

    -- 打印一下支持的加密套件, 通常来说, 固件已包含常见的99%的加密套件
    if crypto.cipher_suites then
        log.info("cipher", "suites", json.encode(crypto.cipher_suites()))
    end

    -------------------------------------
    -------- HTTP 演示代码 --------------
    -------------------------------------

    

    while 1 do

        local res = http_onenet.get_points(product_id, api_key, 1)
        log.info("res---", json.encode(res))
        --  I/user.res---	{"demo":[{"value":1,"at":"2023-04-25 19:17:55.417"}],"dataNET":[{"value":0,"at":"2023-04-01 00:14:17.760"}],"dataRI":[{"value":0,"at":"2023-04-01 00:14:17.760"}]}

        local post_res = http_onenet.post_points(product_id, api_key, {["demo"]=1})
        log.info("post res::::", post_res)
        -- I/user.post res::::	200
        
        sys.wait(5000)
    end
end)

-- 用户代码已结束---------------------------------------------
-- 结尾总是这一句
sys.run()
-- sys.run()之后后面不要加任何语句!!!!!
