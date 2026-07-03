from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.ttLib.removeOverlaps import removeOverlaps
import copy


def clean_and_crop_font(
    input_path: str, output_path: str, padding_percent: float = 0.03
):
    """
    Cleans up internal shape overlaps across standard glyphs using fontTools utilities, identifies bounds based purely on core letters, and flat-crops vector points.
    """
    font = TTFont(input_path)
    glyph_table = font["glyf"]

    standard_glyph_names = []
    for name in glyph_table.keys():
        if "." in name or "swash" in name.lower() or "_" in name:
            continue
        if glyph_table[name].numberOfContours <= 0:
            continue
        standard_glyph_names.append(name)

    print(f"Merging vector paths for {len(standard_glyph_names)} standard glyphs...")

    removeOverlaps(font, glyphNames=standard_glyph_names, removeHinting=True)

    global_y_max = float("-inf")
    global_y_min = float("inf")

    for name in standard_glyph_names:
        glyph = glyph_table[name]
        for _, y in glyph.coordinates:
            if y > global_y_max:
                global_y_max = y
            if y < global_y_min:
                global_y_min = y

    em_square = font["head"].unitsPerEm if "head" in font else 1000
    gap_units = int(em_square * padding_percent)

    y_max_limit = int(global_y_max + gap_units)
    y_min_limit = int(global_y_min - gap_units)

    print(f"Calculated Normal Limits -> Ceiling: {y_max_limit}, Floor: {y_min_limit}")

    for name in standard_glyph_names:
        glyph = glyph_table[name]
        cropped_coords = []
        for x, y in glyph.coordinates:
            new_y = y
            if y > y_max_limit:
                new_y = y_max_limit
            elif y < y_min_limit:
                new_y = y_min_limit
            cropped_coords.append((x, new_y))

        glyph.coordinates = GlyphCoordinates(cropped_coords)
        glyph.recalcBounds(glyph_table)

    ylimit = min(abs(y_max_limit), abs(y_min_limit))

    if "head" in font:
        font["head"].yMax = ylimit
        font["head"].yMin = -ylimit
    if "hhea" in font:
        font["hhea"].ascender = ylimit
        font["hhea"].descender = -ylimit
        font["hhea"].lineGap = 0
    if "OS/2" in font:
        font["OS/2"].sTypoAscender = ylimit
        font["OS/2"].sTypoDescender = -ylimit
        font["OS/2"].sTypoLineGap = 0
        font["OS/2"].usWinAscent = ylimit
        font["OS/2"].usWinDescent = ylimit

    font.save(output_path)
    print(f"Done! Cleaned, artifact-free font saved to: {output_path}")


def scale_font_vectors(input_path: str, output_path: str, scale_factor: float = 1.25):
    """
    Scales all vector glyphs and spacing metrics up to increase the font's apparent size without changing the point size in your software.
    """
    font = TTFont(input_path)

    glyph_table = font["glyf"]
    for glyph_name in glyph_table.keys():
        glyph = glyph_table[glyph_name]

        if glyph.numberOfContours <= 0:
            continue

        scaled_coords = []
        for x, y in glyph.coordinates:
            scaled_coords.append((int(x * scale_factor), int(y * scale_factor)))

        glyph.coordinates = glyph.coordinates.__class__(scaled_coords)

    hmtx_table = font["hmtx"]
    for glyph_name in hmtx_table.metrics.keys():
        width, lsb = hmtx_table.metrics[glyph_name]
        hmtx_table.metrics[glyph_name] = (
            int(width * scale_factor),
            int(lsb * scale_factor),
        )

    if "hhea" in font:
        font["hhea"].ascender = int(font["hhea"].ascender * scale_factor)
        font["hhea"].descender = int(font["hhea"].descender * scale_factor)
        font["hhea"].lineGap = int(font["hhea"].lineGap * scale_factor)

    if "OS/2" in font:
        font["OS/2"].sTypoAscender = int(font["OS/2"].sTypoAscender * scale_factor)
        font["OS/2"].sTypoDescender = int(font["OS/2"].sTypoDescender * scale_factor)
        font["OS/2"].sTypoLineGap = int(font["OS/2"].sTypoLineGap * scale_factor)
        font["OS/2"].usWinAscent = int(font["OS/2"].usWinAscent * scale_factor)
        font["OS/2"].usWinDescent = int(font["OS/2"].usWinDescent * scale_factor)

    font.save(output_path)
    print(
        f"Successfully scaled font vectors by {scale_factor}x and saved to {output_path}"
    )


def auto_trim_font_with_tracking(
    input_path: str, output_path: str, padding_percent: float = 0.03
):
    """
    Scans all glyph vectors, identifies which characters define the highest and lowest boundaries, prints them, and trims the font vertical metrics.
    """
    font = TTFont(input_path)
    glyph_table = font["glyf"]

    glyph_to_char = {}
    if "cmap" in font:
        cmap = font["cmap"].getBestCmap()
        if cmap:
            for codepoint, name in cmap.items():
                try:
                    glyph_to_char[name] = chr(codepoint)
                except ValueError:
                    continue

    global_y_max = float("-inf")
    global_y_min = float("inf")
    max_char_source = "Unknown"
    min_char_source = "Unknown"

    for glyph_name in glyph_table.keys():
        if "." in glyph_name:
            continue

        glyph = glyph_table[glyph_name]
        if glyph.numberOfContours <= 0:
            continue
        glyph = glyph_table[glyph_name]

        if glyph.numberOfContours <= 0:
            continue

        for _, y in glyph.coordinates:
            if y > global_y_max:
                global_y_max = y
                max_char_source = glyph_to_char.get(glyph_name, f"Glyph: {glyph_name}")
            if y < global_y_min:
                global_y_min = y
                min_char_source = glyph_to_char.get(glyph_name, f"Glyph: {glyph_name}")

    print("-" * 60)
    print(
        f" HIGHEST ELEMENT: Y = {global_y_max:<5} | Character responsible: '{max_char_source}'"
    )
    print(
        f" LOWEST ELEMENT:  Y = {global_y_min:<5} | Character responsible: '{min_char_source}'"
    )
    print("-" * 60)

    em_square = font["head"].unitsPerEm if "head" in font else 1000
    gap_units = int(em_square * padding_percent)

    calculated_ascender = int(global_y_max + gap_units)
    calculated_descender = int(global_y_min - gap_units)

    print(
        f"Calculated Boundaries ({padding_percent * 100}% gap added) -> Ascender: {calculated_ascender}, Descender: {calculated_descender}\n"
    )

    if "head" in font:
        font["head"].yMax = calculated_ascender
        font["head"].yMin = calculated_descender

    if "hhea" in font:
        font["hhea"].ascender = calculated_ascender
        font["hhea"].descender = calculated_descender
        font["hhea"].lineGap = 0

    if "OS/2" in font:
        font["OS/2"].sTypoAscender = calculated_ascender
        font["OS/2"].sTypoDescender = calculated_descender
        font["OS/2"].sTypoLineGap = 0
        font["OS/2"].usWinAscent = calculated_ascender
        font["OS/2"].usWinDescent = abs(calculated_descender)

    font.save(output_path)
    print(f"Successfully auto-cropped font and saved to: {output_path}")


def isolate_and_crop_font(
    input_path: str, output_path: str, padding_percent: float = 0.03
):
    """
    Finds global min/max boundaries using ONLY standard alphabet glyphs, then crops standard glyphs to those bounds while leaving swash variants completely untouched.
    """
    font = TTFont(input_path)
    glyph_table = font["glyf"]

    global_y_max = float("-inf")
    global_y_min = float("inf")

    for glyph_name in glyph_table.keys():
        if "." in glyph_name or "swash" in glyph_name.lower() or "_" in glyph_name:
            continue

        glyph = glyph_table[glyph_name]
        if glyph.numberOfContours <= 0:
            continue

        for _, y in glyph.coordinates:
            if y > global_y_max:
                global_y_max = y
            if y < global_y_min:
                global_y_min = y

    print(
        f"Standard Glyph Boundaries -> Max Peak: {global_y_max}, Min Floor: {global_y_min}"
    )

    em_square = font["head"].unitsPerEm if "head" in font else 1000
    gap_units = int(em_square * padding_percent)

    y_max_limit = int(global_y_max + gap_units)
    y_min_limit = int(global_y_min - gap_units)

    print(
        f"Hard Clamping Thresholds  -> Ceiling:  {y_max_limit}, Floor:     {y_min_limit}\n"
    )

    standard_modified_count = 0

    for glyph_name in glyph_table.keys():
        if "." in glyph_name or "swash" in glyph_name.lower() or "_" in glyph_name:
            continue

        glyph = glyph_table[glyph_name]
        if glyph.numberOfContours <= 0:
            continue

        cropped_coords = []
        modified = False

        for x, y in glyph.coordinates:
            new_y = y
            if y > y_max_limit:
                new_y = y_max_limit
                modified = True
            elif y < y_min_limit:
                new_y = y_min_limit
                modified = True
            cropped_coords.append((x, new_y))

        if modified:
            glyph.coordinates = glyph.coordinates.__class__(cropped_coords)
            glyph.recalcBounds(glyph_table)
            standard_modified_count += 1

    print(
        f"Cropping Complete: Clamped vector endpoints across {standard_modified_count} standard glyphs."
    )

    if "head" in font:
        font["head"].yMax = y_max_limit
        font["head"].yMin = y_min_limit

    if "hhea" in font:
        font["hhea"].ascender = y_max_limit
        font["hhea"].descender = y_min_limit
        font["hhea"].lineGap = 0

    if "OS/2" in font:
        font["OS/2"].sTypoAscender = y_max_limit
        font["OS/2"].sTypoDescender = y_min_limit
        font["OS/2"].sTypoLineGap = 0
        font["OS/2"].usWinAscent = y_max_limit
        font["OS/2"].usWinDescent = abs(y_min_limit)

    font.save(output_path)
    print(f"Saved optimized font file to: {output_path}")


def transform_underscore_to_hyphen(
    input_path: str, output_path: str, scale_x: float = 0.55, scale_y: float = 1.40
):
    """
    Clones the weathered underscore glyph, resizes its vector paths using matrix scaling factors, and lifts it up to serve as a perfectly matching hyphen.
    """
    font = TTFont(input_path)
    glyph_table = font["glyf"]
    hmtx_table = font["hmtx"]

    if "underscore" not in glyph_table:
        print("Error: 'underscore' glyph not found in this font file to clone.")
        return

    print("Transforming weathered underscore into a baseline hyphen...")

    x_height = 450
    if (
        "OS/2" in font
        and hasattr(font["OS/2"], "sxHeight")
        and font["OS/2"].sxHeight > 0
    ):
        x_height = font["OS/2"].sxHeight
    target_y_center = x_height // 2 + 50

    hyphen_glyph = copy.deepcopy(glyph_table["underscore"])

    transformed_coords = []
    for x, y in hyphen_glyph.coordinates:
        new_x = int(x * scale_x)
        new_y = int(y * scale_y)
        transformed_coords.append((new_x, new_y))

    hyphen_glyph.coordinates = GlyphCoordinates(transformed_coords)
    hyphen_glyph.recalcBounds(glyph_table)

    current_y_center = (hyphen_glyph.yMax + hyphen_glyph.yMin) // 2

    vertical_shift = target_y_center - current_y_center

    final_coords = []
    for x, y in hyphen_glyph.coordinates:
        final_coords.append((x, y + vertical_shift))

    hyphen_glyph.coordinates = GlyphCoordinates(final_coords)
    hyphen_glyph.recalcBounds(glyph_table)

    glyph_table["hyphen"] = hyphen_glyph

    left_side_bearing = int(80 * scale_x)
    right_side_bearing = int(80 * scale_x)
    total_advance_width = hyphen_glyph.xMax + right_side_bearing

    hmtx_table.metrics["hyphen"] = (total_advance_width, left_side_bearing)

    font.save(output_path)
    print(f"Successfully compiled transformed hyphen into: {output_path}")


def add_font_metadata_suffix(
    input_path: str,
    output_path: str,
    suffix: str = "Patched",
):
    """
    Updates the internal naming tables of a font file to append a suffix, ensuring it registers as a unique typeface family in software dropdowns.
    """
    font = TTFont(input_path)
    name_table = font["name"]

    target_ids = [1, 3, 4, 6, 16]

    modified_records = 0
    for record in name_table.names:
        if record.nameID in target_ids:
            try:
                original_text = record.toUnicode()

                if record.nameID == 6:
                    cleaned_orig = original_text.replace(" ", "")
                    new_text = f"{cleaned_orig}{suffix}"
                else:
                    new_text = f"{original_text}{suffix}"

                record.string = new_text.encode(record.getEncoding())
                modified_records += 1

            except (UnicodeDecodeError, UnicodeEncodeError):
                continue

    font.save(output_path)
    print(
        f"Successfully updated {modified_records} naming records! Saved to {output_path}"
    )


if __name__ == "__main__":
    clean_and_crop_font(
        input_path="P22OperinaPro.ttf",
        output_path="P22OperinaProPatched.ttf",
        padding_percent=0.03,
    )

    scale_font_vectors(
        input_path="P22OperinaProPatched.ttf",
        output_path="P22OperinaProPatched.ttf",
        scale_factor=2.5,
    )

    transform_underscore_to_hyphen(
        input_path="P22OperinaProPatched.ttf",
        output_path="P22OperinaProPatched.ttf",
        scale_x=0.50,
        scale_y=1.35,
    )
    add_font_metadata_suffix(
        input_path="P22OperinaProPatched.ttf",
        output_path="P22OperinaProPatched.ttf",
        suffix="Patched",
    )
