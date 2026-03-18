import io
from flask import Flask, request, jsonify, render_template, send_file
from llm import analyze_text
from loom import build_grid, draw_pdf

app = Flask(__name__, template_folder="static/templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # print("hitting analyze endpoint")
    data = request.json
    
    txt = data.get("text", "")
    
    if not txt:
        return jsonify({"error": "No text provided"}), 400
        
    try:
        emo_data = analyze_text(txt)
        
        # get grid from loom
        grid_cols = build_grid(emo_data)
        
        # print(emo_data)
        
        return jsonify({
            "metadata": emo_data,
            "grid": grid_cols
        })
    except Exception as e:
        print("omg error in analyze:", e)
        return jsonify({"error": "Failed to analyze text"}), 500

@app.route("/render_pdf", methods=["POST"])
def render_pdf():
    # print("rendering pdf now")
    data = request.json
    
    meta = data.get("metadata", {})
    g = data.get("grid", [])
    
    if not meta or not g:
        return jsonify({"error": "Missing rendering data"}), 400
        
    try:
        emo = meta.get("primary_emotion", "Unknown").upper()
        intense = meta.get("intensity_score", 0.5)
        sub = meta.get("poetic_subtitle", "")
        pal = meta.get("color_palette", [])
        
        buff = draw_pdf(g, pal, emo, intense, sub)
        
        return send_file(
            buff,
            as_attachment=True,
            download_name=f"loom_blueprint_{emo.lower()}.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        print("crashed pdf render :(", e)
        return jsonify({"error": "Failed to render PDF"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
