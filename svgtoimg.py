# Convert the provided SVG file to Base64 encoding for embedding in the Markdown.
import base64

# Path to the SVG file uploaded by the user.
svg_file_path = "noun-hacker-2481468.svg"

# Read and encode the SVG file in Base64.
with open(svg_file_path, "rb") as svg_file:
    svg_base64 = base64.b64encode(svg_file.read()).decode("utf-8")

svg_base64