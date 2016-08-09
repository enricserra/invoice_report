Reports worrisome events regarding samples.

usage: invoice.py [-h] -i INVOICE_TSV --invoice_id
                                     INVOICE_ID --output_file OUTPUT_FILE

    Example of INVOICE_TSV:
    
    LP2000950-DNA_B08	RGD	ISIS_30X	23/12/2015 12:45
    LP2000754-DNA_E09	cancer_normal	ISIS_30X	02/12/2015 22:02
    LP2000938-DNA_H01	cancer_normal	ISIS_30X	22/12/2015 18:33
    LP2000939-DNA_B02	cancer_tumor	SOX_75X	22/12/2015 18:33


There are 2 test files, for sample already labeled with an invoice id, 
sample not found in catalog (this HAS to be executed AFTER sample goes to 
catalog) third security check requires DB to be modified (ambiguity, meaning two 
objects can be found through the same sample_id).