-- ----------------------------------------------
-- external use demo

-- get points
-- local res = http_onenet.get_points("10xxxxx---product_id", "2xxxxxxxxxxx--apikey", 1) 
-- log.info("res---", json.encode(res))
-- --  I/user.res---	{"demo":[{"value":1,"at":"2023-04-25 19:17:55.417"}],"dataNET":[{"value":0,"at":"2023-04-01 00:14:17.760"}],"dataRI":[{"value":0,"at":"2023-04-01 00:14:17.760"}]}

-- write points
-- local post_res = http_onenet.post_points("10xxxxx---product_id", "2xxxxxxxxxxx--apikey", {["demo"]=1})
-- log.info("post res::::", post_res)
-- -- I/user.post res::::	200
-- ----------------------------------------------

http_onenet = {}

-- get points
function http_onenet.get_points(id, key, limit)
    local res_data = {}
    local code, headers, body = http.request("GET", "http://api.heclouds.com/devices/"..id.."/datapoints", {["api-key"]=key},json.encode({limit=limit})).wait()
    -- log.info("http.get", code, headers, body)
    body = json.decode(body)
    -- log.info("decode body:", body)
    if body.errno == 0 then
        for k,v in ipairs(body.data.datastreams) do
            res_data[v["id"]] = v["datapoints"]
        end
    end
    return res_data
end

-- write points
function http_onenet.post_points(id, key, write_dict)
    temp_list = {}
    idx = 1
    for k,v in pairs(write_dict) do
        temp_list[idx] = {["id"] = k,["datapoints"]= {{["value"] = v}} }
        idx = idx + 1
    end
    data = {["datastreams"]=temp_list}
    -- log.info("post data:", data)
    local code, headers, body = http.request("POST", "http://api.heclouds.com/devices/"..id.."/datapoints", {["api-key"]=key},json.encode(data)).wait()
    -- requests.post(url, headers=headers, data=json.dumps(data))
    -- log.info(code, headers, body)
    return code
end


return http_onenet


-- -- 200	table: 0045B328	{"errno":0,"data":{"count":2,"datastreams":[{"datapoints":[{"at":"2023-04-01 00:14:17.760","value":0}],"id":"dataRI"},{"datapoints":[{"at":"2023-04-01 00:14:17.760","value":0}],"id":"dataNET"}]},"error":"succ"}