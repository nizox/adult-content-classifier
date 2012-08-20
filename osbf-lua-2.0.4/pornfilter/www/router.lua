module(..., package.seeall)

require("views")

function not_found(wsapi_env)
    local headers = { ["Content-type"] = "text/html" }

    local function text()
        coroutine.yield("<html><body><p>Not found</p></body></html>")
    end

    return 404, headers, coroutine.wrap(text)
end

local urls = {
    { match = "/classify", view = views.classify },
    { match = "/learn", view = views.learn },
}

function run(wsapi_env)
    for i, url in ipairs(urls) do
        if wsapi_env.PATH_INFO:match(url["match"]) then
            return url["view"](wsapi_env)
        end
    end
    return not_found(wsapi_env)
end
