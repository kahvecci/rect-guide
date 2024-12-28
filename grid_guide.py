"""
    This script adds guide grid for rectangle coordinats. 
    Created by kahvecci
    22.12.2024
"""

import pymupdf as fitz
import sys
import os

WIDTH = 595.5
HEIGHT = 842.25

if len(sys.argv) != 2:
    print("Usage: python grid_guide.py <pdf_file>")
    print("Example: python grid_guide.py example.pdf")
    sys.exit(1)

pdf_path = sys.argv[1]

if not os.path.exists(pdf_path):
    print(f"Error: File '{pdf_path}' not found")
    sys.exit(1)
    
if not pdf_path.lower().endswith('.pdf'):
    print("Error: File must be a PDF")
    sys.exit(1)


doc = fitz.Document(pdf_path)
page = doc[0]

# draw rect guide line on page

def draw_guide_lines(increment = 50, color = (1, 0, 0), width = 1.4, opacity = 0.8, coor=True):
    
    # for positions

    vertical_positions = [p for p in range(0, int(HEIGHT), increment)]
    horizontal_positions = [p for p in range(0, int(WIDTH), increment)]

    for p in vertical_positions: # vertical
        p += increment
        p1 = fitz.Point(0, p)
        p2 = fitz.Point(WIDTH, p)
        page.draw_line(p1, p2, color=color, width=width, stroke_opacity=opacity)
        
    for p in horizontal_positions: # horizontal
        p += increment
        p1 = fitz.Point(p, 0)
        p2 = fitz.Point(p, HEIGHT)
        page.draw_line(p1, p2, color=color, width=width, stroke_opacity=opacity)
        
    if coor:
        # for vertical and horizontal point intesections 
        intersections = []
        for y in vertical_positions:
            for x in horizontal_positions:
                intersections.append((x, y))
                
        for x, y in intersections:
            page.insert_text(fitz.Point(x+2, y+7), f"({x},{y})", fontsize=6, color=color, rotate=0, stroke_opacity=opacity)
            page.insert_text(fitz.Point(x-1.5, y+3.5), "•", fontsize=10, color=(0,0,0), rotate=0, stroke_opacity=opacity)

        
draw_guide_lines(increment=10, color= (0, 0, 0), width=0.5, opacity= 0.5, coor=False) # secondary lines with 10 increment
draw_guide_lines() #main lines 

# Save PDF
doc.save("output_grid.pdf")
doc.close()
