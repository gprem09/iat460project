import math
import io
from perlin_noise import PerlinNoise
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white


def build_grid(emotion_data):
    emo = emotion_data.get("primary_emotion", "Unknown").upper()
    intensity = emotion_data.get("intensity_score", 0.5)
    pal = emotion_data.get("color_palette", [])
    
    L = len(pal)
    if L == 0:
        return []
        
    GW = 50
    GH = 50
    
    # seed from emotion string - learned this trick online
    s = sum(ord(c) for c in emo) + int(intensity * 1000)
    octs = max(1, min(10, int(intensity * 10))) 
    noise = PerlinNoise(octaves=octs, seed=s)
    
    raw = []
    mn = float('inf')
    mx = float('-inf')
    
    for y in range(GH):
        row = []
        for x in range(GW):
            nx = x / GW
            ny = y / GH
            v = noise([nx, ny])
            row.append(v)
            if v < mn: mn = v
            if v > mx: mx = v
        raw.append(row)
        
    rng = mx - mn if mx != mn else 1
    
    # normalize and map to colors
    out = []
    for y in range(GH):
        crow = []
        for x in range(GW):
            n = ((raw[y][x] - mn) / rng) * 0.999
            idx = math.floor((n * intensity) * L)
            idx = max(0, min(L - 1, idx))
            crow.append(pal[idx]["hex"])
        out.append(crow)
        
    return out


def draw_pdf(grid_colors, palette, emotion, intensity, subtitle, output_path=None):
    buf = io.BytesIO() if output_path is None else output_path
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter
    
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1 * inch, h - 1 * inch, "The Algorithmic Loom")
    
    if subtitle:
        c.setFont("Helvetica-Oblique", 12)
        c.setFillColor(HexColor("#555555"))
        c.drawString(1 * inch, h - 1.25 * inch, f'"{subtitle}"')
        
    c.setFont("Helvetica", 11)
    c.setFillColor(black)
    c.drawString(1 * inch, h - 1.55 * inch, f"EMOTION EXTRACTED:  {emotion}")
    c.drawString(1 * inch, h - 1.75 * inch, f"COMPUTED INTENSITY:  {intensity:.2f}")
    
    gsz = len(grid_colors) 
    mdw = 4.5 * inch
    csz = mdw / gsz
    
    sx = 1 * inch
    sy = h - 2.2 * inch - csz
    
    c.setLineWidth(2)
    c.setStrokeColor(black)
    c.rect(sx, sy - (gsz - 1) * csz, mdw, mdw, stroke=1, fill=0)
    
    c.setLineWidth(0.3)
    c.setStrokeColor(HexColor("#DDDDDD"))
    
    for y, row in enumerate(grid_colors):
        for x, hx in enumerate(row):
            cx = sx + (x * csz)
            cy = sy - (y * csz)
            
            c.setFillColor(HexColor(hx))
            c.rect(cx, cy, csz, csz, stroke=1, fill=1)
            
            r = int(hx[1:3], 16)
            g = int(hx[3:5], 16)
            b = int(hx[5:7], 16)
            luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
            
            c.setFillColor(white if luma < 150 else black)
            c.circle(cx + csz/2, cy + csz/2, csz/10, stroke=0, fill=1)
            
    # draw the legend on the right side
    lx = 5.8 * inch
    ly = h - 2.5 * inch
    
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(black)
    c.drawString(lx, ly, "Thread Legend")
    
    c.setFont("Helvetica", 10)
    for i, item in enumerate(palette):
        hx = item["hex"]
        nm = item["name"]
        
        c.setStrokeColor(HexColor("#AAAAAA")) 
        c.setFillColor(HexColor(hx))
        c.rect(lx, ly - 0.4 * inch - (i * 0.4 * inch), 0.25 * inch, 0.25 * inch, stroke=1, fill=1)
        
        c.setFillColor(black)
        c.drawString(lx + 0.4 * inch, ly - 0.3 * inch - (i * 0.4 * inch), nm)
        
    c.showPage()
    c.save()
    
    if output_path is None:
        buf.seek(0)
        return buf
    return output_path


if __name__ == "__main__":
    # just testing
    test = {
        "primary_emotion": "Joy",
        "intensity_score": 0.9,
        "poetic_subtitle": "Golden rays of light dancing upon the summer grass.",
        "color_palette": [
            {"hex": "#FF3333", "name": "Vibrant Heart"},
            {"hex": "#FF6633", "name": "Summer Embers"},
            {"hex": "#FF9933", "name": "Warm Glow"},
            {"hex": "#FFCC33", "name": "Sunbeam Sand"},
            {"hex": "#FFFF33", "name": "Morning Light"},
            {"hex": "#CCFF33", "name": "Spring Blade"},
            {"hex": "#99FF33", "name": "Vital Sprout"}
        ]
    }
    g = build_grid(test)
    print("grid done, rows:", len(g))
