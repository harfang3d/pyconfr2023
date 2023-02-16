# Demo project for Python Convention France 2023

import asyncio
import sys
import harfang as hg
from math import pi

hg.InputInit()
hg.WindowSystemInit()

res_x, res_y = 800, 800
vp_width , vp_height = res_x, res_y

win = hg.NewWindow("PyConFr2023", res_x, res_y, 32, hg.WV_Windowed)
if sys.platform == "emscripten":
    hg.RenderInit(win, hg.RT_OpenGLES)
else:
    hg.RenderInit(win, hg.RT_OpenGL)
hg.RenderReset(res_x, res_y, hg.RF_None)


def on_resize3d(ev):
    global vp_width, vp_height
    vp_width = int(ev.width)
    vp_height = int(ev.height)
    print("resize:", vp_width,vp_height)


async def main():
    if sys.platform == "emscripten":
        platform.EventTarget.addEventListener(None, "resize3d", on_resize3d )

    #
    pipeline = hg.CreateForwardPipeline()
    res = hg.PipelineResources()

    if sys.platform == "emscripten":
        hg.AddAssetsFolder("assets_compiled")
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

    sprite_size = 0.5
    sprite_aspect_ratio = 200 / 320
    sprite_mdl = hg.CreatePlaneModel(vtx_layout, 1 * sprite_size, res_y / res_x * sprite_size * sprite_aspect_ratio, 1, 1)
    sprite_prg = hg.LoadProgramFromAssets('core/shader/sprite')
    sprite_texture,_ = hg.LoadTextureFromAssets("maps/pyconfr23.png", hg.TF_UBorder | hg.TF_VBorder | hg.TF_SamplerMinAnisotropic | hg.TF_SamplerMagAnisotropic)
    prev_sprite_texture = None

    hg.ImGuiInit(10, imgui_prg, imgui_img_prg)

    webcam_reload_timer = hg.GetClock()
    webcam_image_index = 0

    # main loop
    while not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
        dt = hg.TickClock()
        view_id = 0

        if hg.GetClock() - webcam_reload_timer > hg.time_from_sec_f(1.0 / 30.0): # 30 FPS
            prev_sprite_texture = sprite_texture
            sprite_texture,_ = hg.LoadTextureFromAssets("maps/img" + str(webcam_image_index) + ".png", hg.TF_UBorder | hg.TF_VBorder | hg.TF_SamplerMinAnisotropic | hg.TF_SamplerMagAnisotropic)
            hg.DestroyTexture(prev_sprite_texture)
            scene.GarbageCollect()
            webcam_image_index += 1
            if webcam_image_index > 9:
                webcam_image_index = 0
            webcam_reload_timer = hg.GetClock()

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
        sprite_matrix = hg.TransformationMat4(hg.Vec3(0.65, -0.75, 0), hg.Vec3(pi / 2, pi, 0))
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

