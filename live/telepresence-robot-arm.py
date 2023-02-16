# Demo project for Python Convention France 2023

import asyncio
import sys
import harfang as hg
from math import pi

hg.InputInit()
hg.WindowSystemInit()

LED_GPIO = 2

res_x, res_y = 800, 800
vp_width , vp_height = res_x, res_y

win = hg.NewWindow("PyConFr2023", res_x, res_y, 32, hg.WV_Windowed)
if sys.platform == "emscripten":
    hg.RenderInit(win, hg.RT_OpenGLES)
else:
    hg.RenderInit(win, hg.RT_OpenGL)
hg.RenderReset(res_x, res_y, hg.RF_None)



import pygame

import pygame.vidcap as camera

pygame.display.set_caption("pycon fr 2023 IoT test")

import shutil


from telemetrix_aio import telemetrix_aio


async def new_motor(board):
    # set the max speed and acceleration
    motor = await board.set_pin_mode_stepper(interface=4, pin1=16, pin2=5, pin3=4, pin4=0)
    await board.stepper_set_max_speed(motor, 100)
    await board.stepper_set_acceleration(motor, 400)
    return motor
    

async def blink(board, pin):

    # set the pin mode
    await board.set_pin_mode_digital_output(pin)

    # toggle the pin 4 times and exit
    for x in range(2):
        print('ON')
        await board.digital_write(pin, 0)
        await asyncio.sleep(1)
        print('OFF')
        await board.digital_write(pin, 1)
        await asyncio.sleep(1)
        

def on_resize3d(ev):
    global vp_width, vp_height
    vp_width = int(ev.width)
    vp_height = int(ev.height)
    print("resize:", vp_width,vp_height)


async def main():
    global motor
    if sys.platform == "emscripten":
        platform.EventTarget.addEventListener(None, "resize3d", on_resize3d )

        assets = Path("assets_compiled")
        assets.mkdir()

        cfg = {
            "io": "url",
            "type": "mount",
            "mount": {
                "point": assets.as_posix(),
                "path": "/",
            },
            "path": f"/ => {assets.as_posix()}",
        }

        track = platform.window.MM.prepare("live/assets_compiled.zip", json.dumps(cfg))

        await shell.runner.pv(track)


    # default to localhost for telemetrix target.
    if sys.argv[-1].endswith('.py'):
        ip_addr = '127.0.0.1'
    else:
        ip_addr = sys.argv[-1]


    # default websocket mode is wss:// change it when on lan.
    if sys.platform in ('emscripten',):
        print('Using websocket')
        if ip_addr.startswith('192.168.') or ip_addr in ('localhost','127.0.0.1'):
            window.MM.set_socket("ws://")
            print(f"Board (Web)socket : {ip_addr}:31335 not using ssl")

    else:
        print(f"Board socket : {ip_addr}:31335")

        
    #
    pipeline = hg.CreateForwardPipeline()
    res = hg.PipelineResources()

    # init camera
    cam = camera.Camera(camera.list_cameras()[0], (320, 200), 0)
    await cam.start()

    # let camera start, and esp8266 time to boot, and also assets mount

    print("-assets lists-")
    await asyncio.sleep(2)

    for df in os.listdir("assets_compiled"):
        print(df)
    print("-assets mounted-")

    for i in range(0, 100):
        shutil.copy("/dev/video0", "video0.png")
        if len(open("video0.png", "rb").read()):
            break
        await asyncio.sleep(0.016)
    else:
        print("could not grab a frame")

        
    # instantiate telemetrix_aio

    board = telemetrix_aio.TelemetrixAIO(ip_address=ip_addr, autostart=False)
    await board.start_aio()


    if sys.platform == "emscripten":
        hg.AddAssetsFolder("assets_compiled")
        if not hg.AddAssetsFolder("/dev"):
            raise Error("Assets device Folder")
    else:
        hg.AddAssetsFolder("assets_compiled_GL")


    imgui_prg = hg.LoadProgramFromAssets("core/shader/imgui")
    imgui_img_prg = hg.LoadProgramFromAssets("core/shader/imgui_image")

    # load scene
    scene = hg.Scene()
    print("27(loading scene)")
    hg.LoadSceneFromAssets("main_fallback_shader.scn", scene, res, hg.GetForwardPipelineInfo())
    print("29(scene loaded)")
    # gather the axis names
    node_list = scene.GetNodes()
    axis_list = []
    for i in range(node_list.size()):
        node = node_list.at(i)
        node_name = node.GetName()
        print(node_name)
        if node_name.startswith("_PIVOT_"):
            axis = node_name.split("_")[-1]
            if node_name.find("FINGER") > -1:
                pivot_name = node_name.split("_")[2] + " " + node_name.split("_")[3] + node_name.split("_")[4]
            else:
                pivot_name = node_name.split("_")[1] + " " + node_name.split("_")[2]

            _rot = node.GetTransform().GetRot()
            if axis == "X":
                angle = hg.RadianToDegree(_rot.x)
            elif axis == "Y":
                angle = hg.RadianToDegree(_rot.y)
            else:
                angle = hg.RadianToDegree(_rot.z)
            angle_min = angle - 90.0
            angle_max = angle + 90.0
            axis_list.append({"pivot": pivot_name, "axis": axis, "node": node, "angle": angle, "min": angle_min, "max": angle_max})
            print(axis)

    cam = scene.GetNode("camera")

    # sprite display
    # create a plane model for the final rendering stage
    vtx_layout = hg.VertexLayoutPosFloatNormUInt8TexCoord0UInt8()

    sprite_size = 1.8
    sprite_aspect_ratio = 200 / 320
    sprite_mdl = hg.CreatePlaneModel(vtx_layout, 1 * sprite_size, res_y / res_x * sprite_size * sprite_aspect_ratio, 1, 1)
    sprite_prg = hg.LoadProgramFromAssets('core/shader/sprite')
    #sprite_texture,_ = hg.LoadTextureFromAssets("maps/pyconfr23.png", hg.TF_UBorder | hg.TF_VBorder | hg.TF_SamplerMinAnisotropic | hg.TF_SamplerMagAnisotropic)
    sprite_texture = None
    prev_sprite_texture = sprite_texture
    webcam_image_index = 0
    skip = False
    hg.ImGuiInit(10, imgui_prg, imgui_img_prg)


    await blink(board, LED_GPIO)

    motor  = await new_motor(board)

    IDLE = True
    
    def idle_callback():
        nonlocal IDLE
        IDLE = True
        print("motor set")

    async def busy_loop(fangle):
        nonlocal IDLE
        if not IDLE:
            print("error: motor is busy")
            return
        pos = int(1.8 * fangle)        
        print(f"motor going to {pos} steps for {fangle}°")
        IDLE = False                            
        await board.stepper_move_to(motor, pos) 
        await board.stepper_run(motor, completion_callback=idle_callback)
        print("motor going idle")
        IDLE = True
    
    # main loop
    while not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
        dt = hg.TickClock()
        view_id = 0

        # video feed
        feed = f"/dev/video{webcam_image_index}"

        if os.path.isfile(feed):  # hg.GetClock() - webcam_reload_timer > hg.time_from_sec_f(1.0 / 30.0): # 30 FPS
            prev_sprite_texture = sprite_texture
            shutil.copy(feed, f"assets_compiled/maps/video{webcam_image_index}.png")
            sprite_texture, _ = hg.LoadTextureFromAssets(
                f"maps/video{webcam_image_index}.png",
                hg.TF_UBorder | hg.TF_VBorder | hg.TF_SamplerMinAnisotropic | hg.TF_SamplerMagAnisotropic,
            )
            if prev_sprite_texture:
                hg.DestroyTexture(prev_sprite_texture)
            scene.GarbageCollect()
            os.unlink(feed)

        # 3D
        scene.Update(dt)

        cam_matrix = cam.GetTransform().GetWorld()
        hg.SetViewPerspective(view_id, 0, 0, res_x, res_y, cam_matrix,
                              cam.GetCamera().GetZNear(), cam.GetCamera().GetZFar(),
                              hg.FovToZoomFactor(cam.GetCamera().GetFov()))
        view_id, pass_id = hg.SubmitSceneToPipeline(view_id, scene, hg.IntRect(0, 0, res_x, res_y), True, pipeline, res)

        hg.SetViewRect(view_id, 0, 0, res_x, res_y)
        hg.SetViewClear(view_id, hg.CF_None)
        sprite_val_uniforms = [hg.MakeUniformSetValue('color', hg.Vec4(1, 1, 1, 1)),]
        sprite_tex_uniforms = [hg.MakeUniformSetTexture('s_tex', sprite_texture, 0)]
        sprite_matrix = hg.TransformationMat4(hg.Vec3(1, -1, 0), hg.Vec3(pi / 2, pi, 0))
        hg.DrawModel(view_id, sprite_mdl, sprite_prg, sprite_val_uniforms, sprite_tex_uniforms, sprite_matrix)
        view_id += 1

        # GUI
        hg.ImGuiBeginFrame(vp_width, vp_height, hg.TickClock(), hg.ReadMouse(), hg.ReadKeyboard())

        if hg.ImGuiBegin("Robot Arm", True, hg.ImGuiWindowFlags_NoMove | hg.ImGuiWindowFlags_NoResize):
            hg.ImGuiSetWindowPos("Robot Arm", hg.Vec2(res_x / 40, res_y - (res_y / 2.45)), hg.ImGuiCond_Once)
            hg.ImGuiSetWindowSize("Robot Arm", hg.Vec2(res_x / 3, res_y / 2.5), hg.ImGuiCond_Once)
            hg.ImGuiText("Axis control")
            for axis in axis_list:
                # hg.ImGuiText(axis["pivot"] + "(" + axis["axis"] + ")")
                angle_update, axis["angle"] = hg.ImGuiSliderFloat(
                    axis["pivot"] + "(" + axis["axis"] + ")", axis["angle"], axis["min"], axis["max"]
                )
                if angle_update:
                    
                    if axis["node"].GetName() == "_PIVOT_0_Z":
                        if IDLE:
                            asyncio.create_task( busy_loop(axis["angle"]) )
                        else:
                            print("pivot motor busy")
                        
                    _trs = axis["node"].GetTransform()
                    _rot = _trs.GetRot()
                    if axis["axis"] == "X":
                        _rot.x = hg.DegreeToRadian(axis["angle"])
                    elif axis["axis"] == "Y":
                        _rot.y = hg.DegreeToRadian(axis["angle"])
                    else:
                        _rot.z = hg.DegreeToRadian(axis["angle"])
                    _trs.SetRot(_rot)
        hg.ImGuiEnd()

        hg.ImGuiEndFrame(view_id)

        hg.Frame()
        hg.UpdateWindow(win)
        await asyncio.sleep(0)

    hg.RenderShutdown()
    hg.DestroyWindow(win)

asyncio.run(main())

