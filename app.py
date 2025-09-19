from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/uploads"  # Render-friendly writable folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    # Basic validation
    if "file" not in request.files:
        return redirect(url_for("error"))

    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("error"))

    conversion = request.form.get("conversion")
    if not conversion:
        return redirect(url_for("error"))

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(input_path)

    # Simulate conversion by copying file to a new extension (replace with real logic later)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    conv_map = {
        "pdf2docx": ".docx",
        "docx2pdf": ".pdf",
        "ppt2docx": ".docx",
        "docx2ppt": ".pptx",
    }
    out_ext = conv_map.get(conversion, ext)
    converted_filename = f"{name}{out_ext}"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], converted_filename)

    try:
        shutil.copyfile(input_path, output_path)
    except Exception:
        return redirect(url_for("error"))

    display_map = {
        "pdf2docx": "PDF → DOCX",
        "docx2pdf": "DOCX → PDF",
        "ppt2docx": "PPTX → DOCX",
        "docx2ppt": "DOCX → PPTX",
    }
    display_conversion = display_map.get(conversion, conversion)

    return render_template("result.html", filename=converted_filename, conversion=display_conversion)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)

