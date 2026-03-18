# Algorithmic Loom - IAT 460 Project

generative art project that takes text input and turns it into an embroidery pattern

## how to run

1. make sure you have a `.env` file with your `GEMINI_API_KEY`
2. install deps: `pip install -r requirements.txt`
3. run: `python app.py`
4. go to `http://localhost:5000`

## what it does

you type in a poem or anything really, it sends it to gemini to analyze the emotion, then generates a cross-stitch grid based on that with perlin noise. you can download it as a pdf too.

## files

- `app.py` - flask server
- `llm.py` - gemini api stuff
- `loom.py` - grid generation + pdf rendering
- `static/templates/index.html` - the frontend