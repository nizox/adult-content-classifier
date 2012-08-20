#!/usr/bin/env lua

local fastcgi = require("wsapi.fastcgi")
local router = require("router")

local function wrapper(wsapi_env)
    wsapi_env.PATH_INFO = wsapi_env.SCRIPT_NAME:gsub("([^/].$)", "%1")
    return router.run(wsapi_env)
end
fastcgi.run(wrapper)
