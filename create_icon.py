from PIL import Image, ImageDraw, ImageFont
import os

def create_jarvis_icon(size=200, output_file="jarvis_icon.png"):
    """Create a simple JARVIS icon"""
    # Create a blank image with a black background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a blue circle
    circle_color = (0, 191, 255, 255)  # Deep Sky Blue
    circle_radius = size // 2 - 10
    circle_position = (size // 2, size // 2)
    draw.ellipse(
        (
            circle_position[0] - circle_radius,
            circle_position[1] - circle_radius,
            circle_position[0] + circle_radius,
            circle_position[1] + circle_radius
        ),
        fill=circle_color
    )
    
    # Draw a smaller black circle inside for contrast
    inner_circle_radius = circle_radius - 20
    draw.ellipse(
        (
            circle_position[0] - inner_circle_radius,
            circle_position[1] - inner_circle_radius,
            circle_position[0] + inner_circle_radius,
            circle_position[1] + inner_circle_radius
        ),
        fill=(30, 30, 30, 255)
    )
    
    # Attempt to add text "J.A.R.V.I.S" to the icon if a font is available
    try:
        # Try to use a built-in font
        font_size = size // 8
        font = ImageFont.truetype("arial.ttf", font_size)
        text = "J.A.R.V.I.S"
        
        # Calculate text position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = (
            (size - text_width) // 2,
            (size - text_height) // 2
        )
        
        # Draw text
        draw.text(text_position, text, fill=(255, 255, 255, 255), font=font)
    except:
        # If font unavailable, draw a simple "J" in the center
        inner_inner_radius = inner_circle_radius - 20
        draw.ellipse(
            (
                circle_position[0] - inner_inner_radius,
                circle_position[1] - inner_inner_radius,
                circle_position[0] + inner_inner_radius,
                circle_position[1] + inner_inner_radius
            ),
            fill=circle_color
        )
    
    # Save the icon
    img.save(output_file)
    print(f"Icon created at {output_file}")
    
    # Create .ico file for Windows
    try:
        ico_file = "jarvis_icon.ico"
        img.save(ico_file, format="ICO")
        print(f"Icon created at {ico_file}")
    except Exception as e:
        print(f"Could not create ICO file: {e}")

if __name__ == "__main__":
    create_jarvis_icon()
    print("JARVIS icon created successfully!") 