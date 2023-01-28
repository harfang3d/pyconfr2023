# Demo project for Python Convention France 2023

import harfang as hg

hg.InputInit()
hg.WindowSystemInit()

res_x, res_y = 800, 800
win = hg.NewWindow("PyConFr2023", res_x, res_y, 32, hg.WV_Windowed)
hg.RenderInit(win, hg.RT_OpenGL)
hg.RenderReset(res_x, res_y, hg.RF_MSAA4X | hg.RF_MaxAnisotropy)

#
pipeline = hg.CreateForwardPipeline()
res = hg.PipelineResources()

hg.AddAssetsFolder("assets_compiled")

imgui_prg = hg.LoadProgramFromAssets('core/shader/imgui')
imgui_img_prg = hg.LoadProgramFromAssets('core/shader/imgui_image')

# load scene
scene = hg.Scene()
hg.LoadSceneFromAssets("main.scn", scene, res, hg.GetForwardPipelineInfo())

# gather the axis names
node_list = scene.GetNodes()
axis_list = []
for i in range(node_list.size()):
	node = node_list.at(i)
	node_name = node.GetName()
	print(node_name)
	if node_name.startswith("_PIVOT_"):
		axis = node_name.split("_")[-1]
		pivot_name = node_name.split("_")[1] + " " + node_name.split("_")[2]
		axis_list.append({"pivot": pivot_name, "axis": axis, "node": node})
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

	if hg.ImGuiBegin('Robot Arm'):
		hg.ImGuiText('Axis control')
		for axis in axis_list:
			hg.ImGuiText(axis["pivot"] + "(" + axis["axis"] + ")")
	hg.ImGuiEnd()

	hg.SetView2D(view_id, 0, 0, res_x, res_y, -1, 1, hg.CF_None, hg.Color.Black, 1, 0)
	hg.ImGuiEndFrame(view_id)

	hg.Frame()
	hg.UpdateWindow(win)

hg.RenderShutdown()
hg.DestroyWindow(win)
