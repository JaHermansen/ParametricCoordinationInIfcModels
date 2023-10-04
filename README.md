# Parametric Coordination in IFC Models: A Master's Thesis Exploration

In the vast domain of Building Information Modeling (BIM), the Industry Foundation Classes (IFC) emerges as an unparalleled standard for seamless data exchange across diverse software platforms. As a significant component of my Master's thesis research, the script detailed below elucidates a novel methodology to enrich IFC files. By appropriating specific attributes from an external Excel dataset, the script endows the IFC model with a denser data layer, offering a more comprehensive representation. Such an enhancement becomes pivotal in realizing the full potential of parametric coordination within BIM-centric workflows.

## Introduction

The primary goal of the script is to load an IFC model, extract products of a particular type (IfcFlowSegment), attempt to match data from an external Excel datasheet, and subsequently update the IFC model based on this matching.

## Code Description

Here's a breakdown of the core functionalities:

### Initialization

Multiple libraries, essential for data manipulation, IFC file handling, and Excel file reading, are imported. These libraries include `ifcopenshell`, `pandas`, `xlrd`, among others.

```python
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
...
import pandas as pd
import os
import numpy as np
```

### User Input and Model Loading

Users are prompted to provide a directory for the IFC source file. A progress bar displays the model-loading process.

```python
sourcefile = input("Specify directory of file\nInput: ")
...
bar1 = ChargingBar('Processing', max=1)
for i in range(1):
    model = ifcopenshell.open(sourcefile)
    bar1.next()
```

### Data Loading

The external datasheet's directory (typically an Excel file) is specified by the user. If the sheet named "Dashboard" doesn't exist, it is created.

```python
input_path = input("Specify directory of data sheet\nInput: ")
...
if not search_word in sheetNames:
    df2 = pd.DataFrame(DashboardTemplate)
    ...
```
### Processing

The IFC model's products are extracted. Property sets are fetched for each product, and operations are performed based on these sets. There's an attempt to reconcile data from the IFC file and the Excel datasheet. The script keeps track of any missing data during this process.

```python
products = model.by_type("IfcProduct")
...
for i in products:
    if i.is_a("IfcFlowSegment"):
        ...
```

### Reporting and Export

This script provides an automated approach to enriching IFC models with external data, promoting more data-driven, parametric coordination in BIM projects. The integration of external data, combined with the ability to highlight discrepancies, ensures that the BIM models are both data-rich and accurate.
