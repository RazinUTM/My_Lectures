"""
s2_numbers.py -- reference numbers for Lab S2 (Influence Lines), UTM CE Lab II.

Model: cantilever (Gerber) bridge, total length 1130 mm.
  beam ABC : pin at A (x=0), roller at B (x=250), cantilever tip C (x=440)
  suspended span CD : hinges at C (440) and D (690)
  beam DEF : cantilever tip D (690), roller at E (880), pin at F (1130)
Unit load at x (mm). Ordinates are dimensionless (force per unit load).
Sign convention: support reactions positive upwards; hinge forces R_C, R_D are the
forces transmitted from the suspended span to the cantilever tips (positive downwards
on the cantilever, i.e. the force the gauge at C or D registers).
"""
import json

L_AB, L_BC, L_CD, L_DE, L_EF = 250, 190, 250, 190, 250
xA, xB, xC, xD, xE, xF = 0, 250, 440, 690, 880, 1130
HALTS = [("A", 0), ("1", 100), ("2", 200), ("B", 250), ("3", 300), ("4", 400), ("C", 440),
         ("5", 500), ("6", 600), ("D", 690), ("7", 700), ("8", 800), ("E", 880), ("9", 900),
         ("10", 1000), ("11", 1100), ("F", 1130)]

def R_C(x):   # hinge force at C (suspended span simply supported on C, D)
    return (xD - x) / L_CD if xC <= x <= xD else 0.0
def R_D(x):
    return (x - xC) / L_CD if xC <= x <= xD else 0.0
def R_A(x):
    if x <= xC:  return (xB - x) / L_AB              # load on ABC: moments about B
    if x <= xD:  return -(xC - xB) / L_AB * R_C(x)    # hinge force at tip C levers A
    return 0.0
def R_B(x):
    if x <= xC:  return x / L_AB
    if x <= xD:  return (xC / L_AB) * R_C(x)
    return 0.0
def R_F(x):   # mirror of R_A about the centre of the suspended span
    if x >= xD:  return (x - xE) / L_EF
    if x >= xC:  return -(xD - xE) / L_EF * R_D(x) * (-1)  # careful: (xD-xE) negative
    return 0.0
def R_E(x):
    if x >= xD:  return (xF - x) / L_EF
    if x >= xC:  return ((xF - xD) / L_EF) * R_D(x)
    return 0.0

# tidy R_F (the expression above simplifies to -(xE-xD)/L_EF * R_D = -0.76 R_D)
def R_F(x):
    if x >= xD:  return (x - xE) / L_EF
    if x >= xC:  return -((xE - xD) / L_EF) * R_D(x)
    return 0.0

ILS = {"R_A": R_A, "R_B": R_B, "R_C": R_C, "R_D": R_D, "R_E": R_E, "R_F": R_F}

def area(f, a, b, n=20000):
    # exact for piecewise linear: use fine trapezoid
    h = (b - a) / n
    return h * (0.5 * f(a) + sum(f(a + i * h) for i in range(1, n)) + 0.5 * f(b))

out = {}
# 1. ordinates at the halts
out["halts"] = [{"label": k, "x": x, **{name: round(f(x), 4) for name, f in ILS.items()}} for k, x in HALTS]
# 2. equilibrium check (sum of support reactions = 1)
out["sum_check"] = [round(R_A(x) + R_B(x) + R_E(x) + R_F(x), 6) for _, x in HALTS]
# 3. areas (mm) of each IL, split into positive and negative parts
def split_area(f):
    pos = area(lambda t: max(f(t), 0.0), 0, 1130); neg = area(lambda t: min(f(t), 0.0), 0, 1130)
    return {"positive": round(pos, 2), "negative": round(neg, 2), "total": round(pos + neg, 2)}
out["areas"] = {name: split_area(f) for name, f in ILS.items()}
# areas of R_A over each segment
out["area_RA_segments"] = {"AB": round(area(R_A, 0, 250), 2), "BC": round(area(R_A, 250, 440), 2),
                           "CD": round(area(R_A, 440, 690), 2), "DEF": round(area(R_A, 690, 1130), 2)}
# 4. compound load: 5 kg leading at x, 2.5 kg trailing at x+100 (moving to the right)
def compound(f, x, m1=5.0, m2=2.5, s=100):
    return m1 * f(x) + m2 * f(x + s)
out["compound_RA"] = [{"label": k, "x": x, "RA_kg": round(compound(R_A, x), 3)} for k, x in HALTS if x + 100 <= 1130]
out["compound_RB"] = [{"label": k, "x": x, "RB_kg": round(compound(R_B, x), 3)} for k, x in HALTS if x + 100 <= 1130]
# critical positions by scanning (1 mm steps)
xs = range(0, 1031)
best_min = min(xs, key=lambda x: compound(R_A, x)); best_max = max(xs, key=lambda x: compound(R_A, x))
out["compound_RA_extremes"] = {"max": {"x": best_max, "value": round(compound(R_A, best_max), 3)},
                               "min": {"x": best_min, "value": round(compound(R_A, best_min), 3)}}
best_maxB = max(xs, key=lambda x: compound(R_B, x))
out["compound_RB_extremes"] = {"max": {"x": best_maxB, "value": round(compound(R_B, best_maxB), 3)}}
# 5. illustrative gauge readings for practice (synthetic, deterministic "noise")
#    reading (div) = ordinate * 2.5 kg / 0.05 kg per div  + small perturbation
noise = [1, -1, 0, 1, -1, 2, -1, 0, 1, -1, 0, 0, 1, -1, 0, 1, 0]
out["practice_readings_A"] = []
for (k, x), e in zip(HALTS, noise):
    exact = R_A(x) * 2.5 / 0.05
    reading = int(round(exact)) + e
    ordinate_test = reading * 0.05 / 2.5
    th = R_A(x)
    diff = (ordinate_test - th) / th * 100 if abs(th) > 1e-9 else None
    out["practice_readings_A"].append({"label": k, "x": x, "reading_div": reading, "eta_test": round(ordinate_test, 3),
                                       "eta_theory": round(th, 3), "abs_diff": round(ordinate_test - th, 3),
                                       "pct_diff": None if diff is None else round(diff, 1)})
# 6. error propagation
out["errors"] = {"slope_AB_per_mm": 1 / 250, "slope_CD_per_mm": 0.76 / 250,
                 "ordinate_err_5mm_AB": round(5 / 250, 3), "ordinate_err_5mm_CD": round(5 * 0.76 / 250, 4),
                 "ordinate_err_1div": round(0.05 / 2.5, 3)}
# 7. UDL examples (w in kg/mm) -> R in kg per unit w
out["udl_RA_per_w"] = {"whole": out["areas"]["R_A"]["total"], "AB_only": out["area_RA_segments"]["AB"],
                       "BC_and_CD": round(out["area_RA_segments"]["BC"] + out["area_RA_segments"]["CD"], 2)}
import pathlib; json.dump(out, open(pathlib.Path(__file__).resolve().parent / "s2_numbers.json", "w"), indent=1)
for h in out["halts"]:
    print(f'{h["label"]:>2} x={h["x"]:4d}  RA={h["R_A"]:7.4f} RB={h["R_B"]:7.4f} RC={h["R_C"]:6.3f} RD={h["R_D"]:6.3f} RE={h["R_E"]:7.4f} RF={h["R_F"]:7.4f}')
print("sum check:", set(out["sum_check"]))
print("areas:", json.dumps(out["areas"]))
print("RA segments:", out["area_RA_segments"])
print("compound RA:", [(c["label"], c["RA_kg"]) for c in out["compound_RA"]])
print("compound RA extremes:", out["compound_RA_extremes"], " RB max:", out["compound_RB_extremes"])
print("practice:", [(p["label"], p["reading_div"], p["eta_test"], p["pct_diff"]) for p in out["practice_readings_A"]])
print("errors:", out["errors"]); print("udl:", out["udl_RA_per_w"])
