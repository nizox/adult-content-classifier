module("views", package.seeall)

local osbf = require("osbf")
local request = require("wsapi.request")

db_path="./"
nonporndb = db_path .. "nonporn.cfc"
porndb    = db_path .. "porn.cfc"
 
dbset = {
          classes = { nonporndb, porndb },
          ncfs = 1,
          delimiters = ""
}
classify_flags = 0


function classify(env)
    local headers = { ["Content-type"] = "text/plain" }
    local req = request.new(env)

    local function process()
        pR, p_array, i_pmax = osbf.classify(req.POST.post_data, dbset, classify_flags)
        if pR == nil then
            coroutine.yield("error: " .. p_array)
        else
            coroutine.yield(string.format("%f", pR))
        end
    end

    local function bad_argument(env)
        coroutine.yield("error: data missing")
    end

    if req.method == "POST" and req.POST.post_data then
        return 200, headers, coroutine.wrap(process)
    else
        return 400, nil, coroutine.wrap(bad_argument)
    end
end

function learn(env)
    local headers = { ["Content-type"] = "text/plain" }
    local req = request.new(env)

    local function process()
        dbindex = env.QUERY_STRING == "porn" and 2 or 1 
        ret = osbf.learn(req.POST.post_data, dbset, dbindex, classify_flags)
        if ret == nil then
            coroutine.yield("error")
        else
            coroutine.yield("ok")
        end
    end

    local function bad_argument(env)
        coroutine.yield("error: data missing")
    end
    if req.method == "POST" and req.POST.post_data and (env.QUERY_STRING == "porn" or env.QUERY_STRING == "nonporn") then
        return 200, headers, coroutine.wrap(process)
    else
        return 400, nil, coroutine.wrap(bad_argument)
    end
end
