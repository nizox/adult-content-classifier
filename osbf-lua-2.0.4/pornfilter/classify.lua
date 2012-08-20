#!/usr/local/bin/lua
-- Sample script for classifying a message read from stdin

local osbf = require "osbf"
local yajl = require "yajl"

-- Set the path to where your databases are.
db_path="./"
nonporndb = db_path .. "nonporn.cfc"
porndb    = db_path .. "porn.cfc"
 
dbset = {
          classes = {nonporndb, porndb},
          ncfs = 1,
          delimiters = ""
}
classify_flags = 0

for line in io.lines() do
    local data = yajl.to_value(line)
    pR, p_array, i_pmax = osbf.classify(data["body"], dbset, classify_flags)

    if (pR == nil) then
       print(p_array)  -- in case of error, p_array contains the error message
    else
       io.write(string.format(data["url"] .. " score: %f - ", pR))
       if (pR >= 0) then
         io.write("Non porn\n")
       else
         io.write("Porn!\n")
       end
    end
end
