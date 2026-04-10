# The Algorithmic Loom — IAT 460 Final Project

A generative art system that transforms written text into emotion-driven cross-stitch embroidery patterns. Input text is analyzed for its emotional content using Google Gemini, which extracts a primary emotion, intensity score, poetic subtitle, and a cohesive 7-color thread palette. These parameters seed a Perlin noise field that produces a 50×50 woven grid pattern, rendered both as an interactive canvas preview and a downloadable PDF blueprint.

## Setup and Installation

1. Clone the repository and navigate into the project directory.
2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open `http://127.0.0.1:5000/` in your browser.

## How It Works

1. The user enters any piece of text — a poem, journal entry, memory, or stream of thought.
2. The text is sent to Google Gemini (`gemini-2.5-flash`), which returns structured emotional metadata: a primary emotion, intensity score (0.0–1.0), a 7-color palette sorted dark to light with poetic thread names, and an evocative subtitle.
3. A 50×50 Perlin noise grid is generated, deterministically seeded by the emotion string and intensity. Higher intensity produces more octaves (texture complexity) and wider palette distribution.
4. The grid is animated cell-by-cell onto an HTML canvas with contrast-aware center dots mimicking cross-stitch markings.
5. The user can export the result as a PDF blueprint containing the title, subtitle, emotion metadata, the full color grid, and a thread legend.

## Project Structure

| File | Description |
|------|-------------|
| `app.py` | Flask web server with routes for analysis and PDF rendering |
| `llm.py` | Gemini API integration with retry logic and structured JSON validation |
| `loom.py` | Perlin noise grid generation and ReportLab PDF blueprint rendering |
| `static/templates/index.html` | Single-page frontend with canvas rendering and animated UI |
| `requirements.txt` | Pinned Python dependencies |
| `outputs/` | Sample PDF blueprint outputs |

## Dependencies

- **Flask** — Web application framework
- **python-dotenv** — Environment variable management
- **google-genai** — Google Gemini API client
- **perlin-noise** — Perlin noise generation for the grid field
- **reportlab** — PDF document generation
