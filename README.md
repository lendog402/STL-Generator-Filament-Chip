# STL Filament Chip Generator

This project contains scripts for generating STL files for printable filament chips, similar to paint chips.

## `stlgenV2.py`

`stlgenV2.py` generates a single STL file for a filament chip.

The script accepts four parameters:

- `Material`
- `Type`
- `Color`
- `Code`

These values are included as raised text on the final print so the user can identify the chip they are holding.

The generated STL filename is created from the same four parameters, using hyphens between the values.

### Example

Input:

- Material: `PLA`
- Type: `Matte`
- Color: `Black`
- Code: `10110`

Output filename:
PLA-Matte-Black-10110.stl


Example call from terminal: 

For one STL
python3 stlgenV2.py PLA Basic Silver 12344

For multiple STL
python3 batch_generate.py filament.csv -s stlgenV2.py -d stl_out


