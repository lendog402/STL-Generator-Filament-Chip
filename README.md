The stlgenV2.py will generate a STl file that can be printed for a filament chip, similar to a paint chip.

The script has four parameters, Material, Type, Color, and Code.  These are included as raised text on the final print so the user will know what color they are holding.

The file the script creates will use these four parameters in the filename.  (e.g PLA Matte Black 10110) would produce an STL file named PLA-Matte-Black-10110.stl.


The batch_generate.py script will parase a CSV that contains these values and create a STL for each line.

The batch_generate.py script will not process any line starting with a #.  You don't have to delete previously generated STL files, you can just use a # to comment the line.

