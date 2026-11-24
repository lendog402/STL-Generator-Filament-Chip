import argparse
from build123d import *

def make_tag_stl(words: list[str], output_path: str = "plate.stl") -> None:
    width = 40.0
    length = 40.0
    base_thickness = 4.0
    emboss_height = 0.8
    font_size = 6.3  # 50% larger than 4.2

    # Base 40mm x 40mm x 4mm block centered in X/Y, sitting from Z=0 to Z=4
    with BuildPart() as part:
        with Locations((0, 0, base_thickness / 2)):
            Box(width, length, base_thickness)

        # Arrange up to 4 words evenly across the top surface (Z = 4mm)
        num_words = len(words)
        margin_y = 3.5
        usable_height = length - 2 * margin_y
        step_y = usable_height / max(num_words, 1)
        start_y = (length / 2) - margin_y - (step_y / 2)

        for idx, word in enumerate(words):
            y_pos = start_y - idx * step_y
            with BuildSketch(Plane.XY.offset(base_thickness)) as text_sketch:
                with Locations((0, y_pos)):
                    Text(
                        word,
                        font_size=font_size,
                        font="Arial",
                        align=(Align.CENTER, Align.CENTER),
                    )
            extrude(amount=emboss_height)

    export_stl(part.part, output_path)
    print(f"Saved {output_path} ({width}mm x {length}mm x {base_thickness}mm base)")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a 40x40x4mm STL with four words on the surface."
    )
    parser.add_argument("words", nargs=4, help="Four words to place on the surface")
    parser.add_argument(
        "-o", "--output", default="four_words.stl", help="Output STL filename"
    )
    args = parser.parse_args()
    make_tag_stl(args.words, args.output)

if __name__ == "__main__":
    main()