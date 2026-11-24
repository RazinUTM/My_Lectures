import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageChops
SRC = pathlib.Path("/tmp/claude-0/-home-claude/65fb654d-60b9-5e6d-b462-30d9d0ce855e/scratchpad/ext/img")
OUT = pathlib.Path(__file__).parent / "web_img"
FONT = None
for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"]:
    if pathlib.Path(f).exists(): FONT = f
def font(sz): return ImageFont.truetype(FONT, sz) if FONT else ImageFont.load_default()

def trim(im, pad=12, tol=18, bg=None):
    im = im.convert("RGB")
    bg = bg or im.getpixel((2, 2))
    diff = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L").point(lambda p: 255 if p > tol else 0)
    box = diff.getbbox()
    if not box: return im
    l, t, r, b = box
    return im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))

def cut_title(im, frac):  # remove a top band (e.g. "MAPDL Element Plot" title)
    return im.crop((0, int(im.height * frac), im.width, im.height))

def fit(im, maxw=1600, maxh=1000):
    im = im.copy(); im.thumbnail((maxw, maxh), Image.LANCZOS); return im

def save(im, name):
    p = OUT / name; im.save(p, optimize=True); print(f"{name:28s} {im.size}  {p.stat().st_size//1024} KB")

def strip(panels, labels, h=420, gap=24, bg=(255, 255, 255), lab_h=56):
    ims = []
    for im in panels:
        r = h / im.height; ims.append(im.resize((int(im.width * r), h), Image.LANCZOS))
    W = sum(i.width for i in ims) + gap * (len(ims) + 1); H = h + lab_h + 2 * gap
    out = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(out); x = gap
    for im, lab in zip(ims, labels):
        out.paste(im, (x, gap + lab_h))
        d.text((x + 4, gap + 6), lab, fill=(21, 34, 59), font=font(30)); x += im.width + gap
    return out

pm = lambda n: Image.open(SRC / f"ansys_pymapdl__{n}.png")
# W9
save(fit(trim(pm("sphx_glr_00-how_finite_element_works_002")), 1000, 1000), "w9_shapeN.png")
save(fit(trim(Image.open(SRC / "hplgit_fem-book__demo2D_basisfunc.png"))), "w9_tent2d.png")
save(fit(trim(Image.open(SRC / "hplgit_fem-book__fe_mesh1D_phi_2_3.png"))), "w9_hat1d.png")
save(fit(trim(Image.open(SRC / "precice_tutorials__tutorials-flow-over-heated-plate-example.png"))), "w9_cht.png")
# W10
save(fit(trim(Image.open(SRC / "precice_tutorials__tutorials-flow-over-heated-plate-steady-state-result.png"))), "w10_aster.png")
save(fit(trim(cut_title(pm("sphx_glr_3d_plate_thermal_002"), 0.0))), "w10_mapdl_thermal.png")
# W11
b8 = trim(cut_title(pm("sphx_glr_bracket_static_008"), 0.12)); b12 = trim(cut_title(pm("sphx_glr_bracket_static_012"), 0.0))
save(fit(b8, 900, 700), "w11_bracket_mesh.png"); save(fit(b12, 1000, 760), "w11_bracket_vm.png")
save(fit(trim(Image.open(SRC / "nicoguaro_SolidsPy__wrench.png"))), "w11_wrench.png")
save(fit(trim(Image.open(SRC / "hplgit_fenics-tutorial__elasticity.png"))), "w11_beam3d.png")
# W12
save(fit(trim(pm("sphx_glr_00-how_finite_element_works_004")), 700, 700), "w12_gauss.png")
save(fit(trim(pm("sphx_glr_00-how_finite_element_works_003")), 700, 700), "w12_iso_centre.png")
save(fit(trim(Image.open(SRC / "solidspy__Beam_convergence.png"))), "w12_conv.png")
save(fit(trim(Image.open(SRC / "solidspy__Beam_mesh-12.png"))), "w12_mesh12.png")
save(fit(trim(Image.open(SRC / "solidspy__Beam_mesh-192.png"))), "w12_mesh192.png")
save(fit(trim(Image.open(SRC / "nicoguaro_SolidsPy__square-4_elements.png"), bg=(0, 0, 0))), "w12_2x2.png")
save(fit(trim(Image.open(SRC / "nicoguaro_SolidsPy__square-4_elements-vertical_disp.png"))), "w12_2x2_uy.png")
# W13
h2 = trim(cut_title(pm("sphx_glr_2d_plate_with_a_hole_002"), 0.12)); h3 = trim(pm("sphx_glr_2d_plate_with_a_hole_003"))
save(fit(h2, 1100, 500), "w13_hole_mesh.png"); save(fit(h3, 1100, 760), "w13_hole_vm.png")
save(fit(trim(Image.open(SRC / "sfepy_sfepy__ITS2D.png"))), "w13_its_sketch.png")
save(fit(trim(Image.open(SRC / "sfepy_sfepy__its2D_3.png"))), "w13_its_quarter.png")
save(fit(trim(Image.open(SRC / "sfepy_sfepy__its2D_2.png"))), "w13_its_stress.png")
# W14 strips
b4 = trim(cut_title(pm("sphx_glr_bracket_static_004"), 0.12)); b6 = trim(cut_title(pm("sphx_glr_bracket_static_006"), 0.12))
save(strip([b4, b6, b8, b12], ["1  Lines (geometry)", "2  Area", "3  Mesh (PLANE183)", "4  Solve: von Mises"], h=380), "w14_bracket_steps.png")
h1 = trim(cut_title(pm("sphx_glr_2d_plate_with_a_hole_001"), 0.12))
save(strip([h1, h2, h3], ["1  Lines", "2  Mesh, refined at the hole", "3  von Mises: K_t = 2.34"], h=340), "w14_hole_steps.png")

# --- second pass: panels for W14 and a tighter plate-with-hole mesh crop ---
def trim_ignore_corner(im, corner=(0, 0.72, 0.18, 1.0), **kw):
    im = im.convert("RGB"); w, h = im.size
    x0, y0, x1, y1 = int(corner[0] * w), int(corner[1] * h), int(corner[2] * w), int(corner[3] * h)
    bg = im.getpixel((2, 2)); tmp = im.copy(); tmp.paste(Image.new("RGB", (x1 - x0, y1 - y0), bg), (x0, y0))
    diff = ImageChops.difference(tmp, Image.new("RGB", tmp.size, bg)).convert("L").point(lambda p: 255 if p > 18 else 0)
    l, t, r, b = diff.getbbox(); pad = 14
    return im.crop((max(0, l - pad), max(0, t - pad), min(w, r + pad), min(h, b + pad)))
h2b = trim_ignore_corner(cut_title(pm("sphx_glr_2d_plate_with_a_hole_002"), 0.12))
save(fit(h2b, 1200, 500), "w13_hole_mesh.png")
save(fit(trim_ignore_corner(cut_title(pm("sphx_glr_2d_plate_with_a_hole_001"), 0.12)), 1200, 500), "w14_h1_lines.png")
save(fit(trim_ignore_corner(cut_title(pm("sphx_glr_bracket_static_004"), 0.12)), 800, 640), "w14_b1_lines.png")
save(fit(trim_ignore_corner(cut_title(pm("sphx_glr_bracket_static_006"), 0.12)), 800, 640), "w14_b2_area.png")
save(fit(trim_ignore_corner(cut_title(pm("sphx_glr_bracket_static_008"), 0.12)), 800, 640), "w11_bracket_mesh.png")
