from pathlib import Path


def define_svg_symbols(mapping):
    symbols = {}
    for key, (shape, color) in mapping.items():
        symbol_id = f"symbol-{key}"
        if shape == "centered_dot":
            symbols[key] = (
                f'<symbol id="{symbol_id}" viewBox="0 0 10 10"><circle cx="5" cy="5" r="1" fill="{color}"/></symbol>'
            )
        elif shape == "square":
            symbols[key] = (
                f'<symbol id="{symbol_id}" viewBox="0 0 10 10"><rect x="1" y="1" width="8" height="8" fill="{color}"/></symbol>'
            )
        elif shape == "circle":
            symbols[key] = (
                f'<symbol id="{symbol_id}" viewBox="0 0 10 10"><circle cx="5" cy="5" r="4" fill="{color}"/></symbol>'
            )
        elif shape == "character":
            symbols[key] = (
                f'<symbol id="{symbol_id}" viewBox="0 0 10 10"><text x="5" y="7" font-size="7" fill="{color}" text-anchor="middle">{key}</text></symbol>'
            )
    return symbols


def grid_to_svg(grid, mapping, cell_size=10):
    total_width = len(grid[0]) * cell_size
    total_height = len(grid) * cell_size
    svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}">\n'
    symbols = define_svg_symbols(mapping)
    svg_content += "<defs>\n" + "".join(symbols.values()) + "</defs>\n"
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in mapping:
                symbol_id = f"symbol-{char}"
                svg_content += f'<use xlink:href="#{symbol_id}" x="{x * cell_size}" y="{y * cell_size}" width="{cell_size}" height="{cell_size}"/>\n'

    svg_content += "</svg>"
    return svg_content


# def draw_element(ax, element, position, cell_size=1, w=1, h=1):
#     x, y, shape, color = position[0], position[1], element[0], element[1]
#     if shape == 'centered_dot':
#         dot_size = cell_size * 5
#         ax.plot(x + 0.5, y + 0.5, color=color, marker='o', markersize=dot_size)
#     elif shape == 'square':
#         square = patches.Rectangle((x + 0.1, y + 0.1), 0.8, 0.8, color=color, edgecolor=None, linewidth=0)
#         ax.add_patch(square)
#     elif shape == 'circle':
#         circle = patches.Circle((x + 0.5, y + 0.5), 0.4, color=color, edgecolor=None)
#         ax.add_patch(circle)
#     elif len(shape) == 1:  # Single character
#         ax.text(x + 0.5, y + 0.5, shape, color=color, ha='center', va='center', fontsize=cell_size * 10 * max(w,h))
#     else:
#         raise ValueError('Invalid shape: ' + shape)


def grids_to_vector_graphics(grid_list, mapping, cell_size=10, svg_stem=None, html=None):
    """
    Convert a list of grids to vector graphics.
    Saves as SVG files if svg is provided.
    Creates an HTML file with SVG viewer if html is provided.
    """
    svg_data_list = [grid_to_svg(grid, mapping) for grid in grid_list]

    if svg_stem:
        svg_stem = Path(svg_stem)
        dir_name = svg_stem.parent
        if not dir_name.exists():
            dir_name.mkdir(parents=True)
        for idx, svg_data in enumerate(svg_data_list):
            indexed_filename = dir_name / f"{svg_stem.stem}.{str(idx).zfill(len(str(len(grid_list))))}.svg"
            with open(indexed_filename, "w") as file:
                file.write(svg_data)

    # Create HTML file if html is provided
    if html:
        with open(html, "w") as html_file:
            html_file.write("<html><head><style>\n")
            html_file.write("html, body { margin: 0; padding: 0; height: 100%; }\n")
            html_file.write("body { display: flex; flex-direction: column; height: 100vh; }\n")
            html_file.write(
                "#svgViewer { flex-grow: 1; display: flex; justify-content: center; align-items: center; overflow: hidden; }\n"
            )
            html_file.write("svg { width: 100%; height: 100%; }\n")  # SVG fills its container

            html_file.write(".controls { padding: 10px; text-align: center; }\n")
            html_file.write(
                "#progressBar { width: 100%; background-color: #ddd; position: relative; white-space: nowrap; }\n"
            )
            html_file.write("div#progressBar > div { height: 10px; display: inline-block; }\n")

            html_file.write("</style></head><body>\n")
            html_file.write('<div id="svgViewer">\n')
            for i, svg_data in enumerate(svg_data_list):
                display_style = "" if i == 0 else "none"
                html_file.write(f'<div style="display: {display_style};">{svg_data}</div>\n')
            html_file.write("</div>\n")

            html_file.write('<div id="progressBar" onclick="selectIndex(event)">\n')
            for idx in range(len(grid_list)):
                html_file.write(
                    f'  <div id="progressSegment{idx}" style="width: {100/len(grid_list)}%; background-color: #ddd;"></div>\n'
                )
            html_file.write("</div>\n")

            html_file.write('<div class="controls">\n')
            html_file.write('<button onclick="reset()">Reset</button>\n')
            html_file.write('<button onclick="play()">Play/Pause</button>\n')
            html_file.write('<button onclick="prev()">Prev</button>\n')
            html_file.write('<button onclick="next()">Next</button>\n')
            html_file.write('<input type="number" id="gotoIndex" value="0" min="0" onchange="goto()">\n')
            html_file.write('<button onclick="goto()">Go to Index</button>\n')
            html_file.write('<input type="number" id="interval" value="200" min="0">\n')
            html_file.write("</div>\n")

            html_file.write("<script>\n")
            html_file.write("let current = 0;\n")
            html_file.write("let playInterval = null;\n")

            html_file.write('document.addEventListener("DOMContentLoaded", (event) => { showCurrent(); });\n')

            html_file.write("function showCurrent() {\n")
            html_file.write('  let svgs = document.getElementById("svgViewer").children;\n')
            html_file.write("  for (let i = 0; i < svgs.length; i++) {\n")
            html_file.write("    let segment = document.getElementById(`progressSegment${i}`);\n")
            html_file.write(
                '    segment.style.backgroundColor = i === 0 ? "#8FBC8F" : (i <= current ? "#4CAF50" : "#ddd");\n'
            )
            html_file.write('    svgs[i].style.display = i === current ? "block" : "none";\n')
            html_file.write("  }\n")
            html_file.write('  document.getElementById("gotoIndex").value = current;\n')
            html_file.write("}\n")

            html_file.write("function prev() {\n")
            html_file.write("  if (current > 0) current--;\n")
            html_file.write("  showCurrent();\n")
            html_file.write("}\n")

            html_file.write("function next() {\n")
            html_file.write('  if (current < document.getElementById("svgViewer").children.length - 1) current++;\n')
            html_file.write("  showCurrent();\n")
            html_file.write("}\n")

            html_file.write("function selectIndex(event) {\n")
            html_file.write("  let x = event.clientX - event.target.getBoundingClientRect().left;\n")
            html_file.write("  let totalWidth = event.target.offsetWidth;\n")
            html_file.write(
                '  let newIndex = Math.floor((x / totalWidth) * document.getElementById("svgViewer").children.length);\n'
            )
            html_file.write(
                '  if (newIndex >= 0 && newIndex < document.getElementById("svgViewer").children.length) {\n'
            )
            html_file.write("    current = newIndex;\n")
            html_file.write("    showCurrent();\n")
            html_file.write("  }\n")
            html_file.write("}\n")

            html_file.write("function goto() {\n")
            html_file.write('  let index = parseInt(document.getElementById("gotoIndex").value);\n')
            html_file.write(
                '  if (!isNaN(index) && index >= 0 && index < document.getElementById("svgViewer").children.length) {\n'
            )
            html_file.write("    current = index;\n")
            html_file.write("    showCurrent();\n")
            html_file.write("  }\n")
            html_file.write("}\n")

            html_file.write("function play() {\n")
            html_file.write("  if (playInterval) {\n")
            html_file.write("    clearInterval(playInterval);\n")
            html_file.write("    playInterval = null;\n")
            html_file.write("  } else {\n")
            html_file.write("    playInterval = setInterval(() => {\n")
            html_file.write('      if (current < document.getElementById("svgViewer").children.length - 1) {\n')
            html_file.write("        current++;\n")
            html_file.write("        showCurrent();\n")
            html_file.write("      } else {\n")
            html_file.write("        clearInterval(playInterval);\n")  # Stop playing when the last index is reached
            html_file.write("        playInterval = null;\n")
            html_file.write("      }\n")
            html_file.write('    }, parseInt(document.getElementById("interval").value));\n')
            html_file.write("  }\n")
            html_file.write("}\n")

            html_file.write("function reset() {\n")
            html_file.write("  current = 0;\n")
            html_file.write("  showCurrent();\n")
            html_file.write("  if (playInterval) {\n")
            html_file.write("    clearInterval(playInterval);\n")
            html_file.write("    playInterval = null;\n")
            html_file.write("  }\n")
            html_file.write("}\n")

            html_file.write("</script>\n")
            html_file.write("</body></html>")

    return svg_data_list


# example usage

if __name__ == "__main__":

    # Example usage
    grid_list = [
        [
            [".", "#", "O", "0", "1"],
            ["#", ".", "O", "1", "2"],
            ["O", "O", ".", "2", "3"],
            ["0", "1", "2", "3", "4"],
            ["1", "2", "3", "4", "5"],
        ],
        [
            [".", "#", "O", "0", "1"],
            ["#", ".", "O", "1", "2"],
            ["O", "O", "O", "2", "3"],
            ["0", "1", "2", "3", "4"],
            ["1", "2", "3", "4", "5"],
        ],
        [
            [".", "#", "O", "0", "1"],
            ["#", "O", "O", "1", "2"],
            ["O", "O", "O", "2", "3"],
            ["0", "1", "2", "3", "4"],
            ["1", "2", "3", "4", "5"],
        ],
    ]

    mapping = {
        ".": ("centered_dot", "black"),
        "#": ("square", "black"),
        "O": ("circle", "red"),
        "0": ("c", "green"),
        "1": ("→", "blue"),
        "2": ("x", "purple"),
        "3": ("+", "orange"),
        "4": ("*", "brown"),
        "5": ("-", "pink"),
    }

    grids_to_vector_graphics(grid_list, mapping, cell_size=1, svg_stem="test.svg", html="test.html")
