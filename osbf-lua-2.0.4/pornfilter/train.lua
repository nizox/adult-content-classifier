#!/usr/bin/env lua

local osbf = require("osbf")
local yajl = require("yajl")

-- Change the path if you installed getopt.lua in another place
dofile("getopt.lua")

-- Set the path to where your databases are.
db_path="./"
nonporndb = db_path .. "nonporn.cfc"
porndb    = db_path .. "porn.cfc"

local optind, options = getopt(arg, { porn = 0, nonporn = 0, undo = 0})

if options["nonporn"] then
  db_index = 1
elseif options["porn"] then
  db_index = 2
else
  print("Syntax: train --nonporn|--porn  [--undo]")
  return 1
end

dbset = {
          classes = {nonporndb, porndb},
          ncfs = 1,
          delimiters = ""
}
learn_flags = 0

local f = options["undo"] and osbf.unlearn or osbf.learn
local m = options["undo"] and "unlearn" or "learn"

for line in io.lines() do
    local data = yajl.to_value(line)
    if data["url"] then
        print(m .. " " .. data["url"])
    end
    assert(f(data["body"], dbset, db_index, learn_flags))
end
