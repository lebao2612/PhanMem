
def get_zoom_expr(zoom: str | None, effect_frames: int) -> str:
    if not zoom:
        return "zoom"
    return {
        "in": f"if(lte(on,{effect_frames}),zoom+0.001,zoom)",
        "out": f"if(lte(on,{effect_frames}),zoom-0.001,zoom)"
    }.get(zoom, "zoom")

def get_pan_x_expr(pan: str | None, effect_frames: int) -> str:
    if pan not in ("left", "right"):
        return "x"
    return {
        "left": f"if(lte(on,{effect_frames}),x-1.1,x)",
        "right": f"if(lte(on,{effect_frames}),x+1.1,x)"
    }[pan]

def get_pan_y_expr(pan: str | None, effect_frames: int) -> str:
    if pan not in ("up", "down"):
        return "y"
    return {
        "up": f"if(lte(on,{effect_frames}),y-1.1,y)",
        "down": f"if(lte(on,{effect_frames}),y+1.1,y)"
    }[pan]
