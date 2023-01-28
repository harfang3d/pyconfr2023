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

# load scene
scene = hg.Scene()
hg.LoadSceneFromAssets("main.scn", scene, res, hg.GetForwardPipelineInfo())

# main loop
while not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
	dt = hg.TickClock()

	scene.Update(dt)
	hg.SubmitSceneToPipeline(0, scene, hg.IntRect(0, 0, res_x, res_y), True, pipeline, res)

	hg.Frame()
	hg.UpdateWindow(win)

hg.RenderShutdown()
hg.DestroyWindow(win)
