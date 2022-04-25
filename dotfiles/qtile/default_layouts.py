from libqtile import layout

from default_variables import layout_margin, layout_ratio


default_config = {
    'border_focus': '#ff6600',
    'border_normal': '#000000',
    'border_width': 1,
    'margin': layout_margin,
    'ratio': layout_ratio
}

layouts = [
    layout.Max(**default_config),
    layout.MonadTall(**default_config),
]

# Possible layouts:
# layout.Stack(num_stacks=2),
# layout.Bsp(),
# layout.Columns(),
# layout.Floating(),
# layout.Matrix(),
# layout.MonadWide(),
# layout.RatioTile(),
# layout.Tile(),
# layout.TreeTab(),
# layout.VerticalTile(),
# layout.Zoomy(),
