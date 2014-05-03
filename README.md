Summary
--------------
This tool performs the conversion process from the raw (point-based) database of Mediterranean movements to a database of line segments which can be used as the database for a GIS layer to be displayed on DARMC.

Dependencies:
* [unicodecsv](https://github.com/jdunck/python-unicodecsv) - can be easily installed with ```pip install unicodecsv```

Updating the Database
--------------------
Download the main data as a csv file from the Mediterranean Movements project folder on Google Drive. No manual formatting of the data is necessary. Name this file ``complete_movements_spreadsheet.csv```, although this is not needed if you do not plan to use the single-stage formatter.

From the med-mvmts project folder, run ```processing_workflow.py```.

Example Output:
```
your-computer:med-mvmts user$ python processing_workflow.py
| - Reading data from input spreadsheet...
| - Parsing point data to line segments... interpreted 1358 total segments
| - Writing trips to output file...
| - Runtime 0.44 seconds.

---  Mediterranean Movements Validator ---
| - Retrieved 1359 total movements
| - Filtered 646 geocoded movements
| - Wrote 646 valid movements
```

If the process completes successfully, you will get an output sheet of all geocoded movements called ```valid_movements.csv```.


Creating Spatial Data from Outputs 
-------------------- 
These output CSV files can easily be spatialized by taking advantage of QGIS's excellent WKT geometry support for text-delimited files. Use *Layer > Add Delimited Text Layer...* to create a layer from ```valid_movements.csv```. The WKT field should be recognized in the source database automatically, and you should not need to adjust any other default parameters.

Save that teporary layer as a shapefile and use ArcCatalog on a Harvard lab computer (or any computer with ArcGIS installed) to overwrite the existing layer in the DARMC geodatabase.
