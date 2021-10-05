--[[
Alternativ intermission code with better support for multiple
intermission videos. It's UDP commands use a slighly different
syntax so you don't have to specify all available videos in
the code itself:
To start an intermission video, send:
   looper/play:video.mp4
where video.mp4 is the intermission video file you want to
play. While an intermission is running, additional play
commands will be ignored. If you want to stop an intermission
and return to the looping video, you can send the following
command at any time:
    looper/loop:
]]--
gl.setup(NATIVE_WIDTH, NATIVE_HEIGHT)
node.alias "looper"

local raw = sys.get_ext "raw_video"

local Looper = function(file)
    local vid = raw.load_video{
        file = file,
        audio = true,
        looped = true,
    }
    local function set_running(running)
        if running then
            vid:target(0, 0, WIDTH, HEIGHT):layer(-1)
            vid:start()
        else
            vid:stop()
            vid:target(0, 2000, 0, 2000)
        end
    end

    return {
        set_running = set_running;
    }
end

local Intermission = function()
    local vid

    local function start(filename)
        if vid then
            return
            -- vid:dispose()
        end
        vid = raw.load_video{
            file = filename,
            audio = true,
        }
        vid:target(0, 0, WIDTH, HEIGHT):layer(-1)
    end

    local function stop()
        if vid then
            vid:dispose()
            vid = nil
        end
    end

    local function is_playing()
        if not vid then
            return false
        end
        local state = vid:state()
        if state == "finished" then
            stop()
        end
        return state == "loaded"
    end

    return {
        start = start;
        stop = stop;
        is_playing = is_playing;
    }
end

local loop = Looper "loop.mp4"
local intermission = Intermission()

local function show_loop()
    loop.set_running(true)
    intermission.stop()
end

local function show_intermission(filename)
end

util.data_mapper{
    ["play"] = function(filename)
        intermission.start(filename)
    end;
    ["loop"] = function()
        show_loop()
    end;
}

show_loop()

function node.render()
    gl.clear(0, 0, 0, 0)
    loop.set_running(not intermission.is_playing())
end