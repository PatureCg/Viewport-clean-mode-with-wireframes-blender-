**Viewport Mode Toggle**

Switch your Blender viewport into a clean, flat, white-background look with one click, then switch back to exactly how it was before.

It's built for wireframe and topology showcases, clean screenshots, and screen recordings, where setting up the viewport by hand each time takes too long. The addon saves your current viewport settings before it changes anything, so pressing the button again puts everything back to your original values, not a default.

**What clean mode does**
- Sets lighting to Flat, object color to Object, and wireframe color to Theme
- Sets the background to a custom pure white
- Turns off X-ray, shadows and cavity
- Hides the floor, axes, 3D cursor, statistics, general info, performance, extras, bones, relationship lines, origins and selection outline
- Turns on the wireframe overlay (1.00 threshold, 0.825 opacity) and turns off face orientation

**How to use it**
- Press **N** in the 3D viewport, open the **Toggle** tab, and click the button. It reads "Enable Clean Mode" or "Restore Original" depending on the current state.
- Or press **Shift+Alt+Z** in the viewport.

**Good to know**
- It works on the viewport you're hovering over, and each viewport remembers its own original settings.
- The saved state is kept in memory only. If you restart Blender while clean mode is on, it can't restore your old settings automatically.
- Tested on Blender 5.1.2. Settings that don't exist in your Blender version are skipped without an error.

If you want it shorter for a store page, or a one-line version for a GitHub repo, I can trim it.
