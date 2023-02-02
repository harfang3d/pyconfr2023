# Demo project for Python Convention France 2023

import asyncio
import harfang as hg

hg.InputInit()
hg.WindowSystemInit()

res_x, res_y = 1024, 720
win = hg.NewWindow("PyConFr2023", res_x, res_y, 32, hg.WV_Windowed)
hg.RenderInit(win, hg.RT_OpenGLES)
hg.RenderReset(res_x, res_y, hg.RF_None)

async def main():

    #
    pipeline = hg.CreateForwardPipeline()
    res = hg.PipelineResources()

    hg.AddAssetsFolder("assets_compiled")

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

    hg.ImGuiInit(10, imgui_prg, imgui_img_prg)

    # main loop
    while not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
        dt = hg.TickClock()
        view_id = 0

        # 3D
        scene.Update(dt)
        view_id, pass_id = hg.SubmitSceneToPipeline(view_id, scene, hg.IntRect(0, 0, res_x, res_y), True, pipeline, res)

        # GUI
        # view_id = view_id + 1
        hg.ImGuiBeginFrame(res_x, res_y, hg.TickClock(), hg.ReadMouse(), hg.ReadKeyboard())

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

        hg.SetView2D(view_id, 0, 0, res_x, res_y, -1, 1, hg.CF_None, hg.Color.Black, 1, 0)
        hg.ImGuiEndFrame(view_id)

        hg.Frame()
        hg.UpdateWindow(win)
        await asyncio.sleep(0)

    hg.RenderShutdown()
    hg.DestroyWindow(win)

asyncio.run(main())

