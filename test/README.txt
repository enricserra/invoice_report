test_1: Already paid
$ python ../invoice.py --invoice_tsv test_already_invoiced_7020064998.tsv --output_file out.txt --invoice_id 7020064998
	
http://10.0.32.140:8080/opencga/webservices/rest/v1/files/search/?sid=S0kqvloTb4hcyoBAZ3Wc&limit=-1&name=LP2000950-DNA_B08.bam&bioformat=ALIGNMENT&studyId=2
Traceback (most recent call last):
  File "../invoice.py", line 114, in <module>
    exit(main())
  File "../invoice.py", line 28, in main
    raise Exception(invoice_errors)
Exception: Sample LP2000950-DNA_B08 already invoiced {u'invoice_id': u'7020064998', u'invoice_date': u'23/12/2015 12:45'} line 1


test_2: Sample not in catalog (something went wrong with the GEL PPL) 

$ python ../invoice.py --invoice_tsv already_invoiced_7020064998.tsv --output_file out.txt --invoice_id 7020064998

invoice_fail_sample_not_in_catalog.tsv  README.txt                              test_already_invoiced_7020064998.tsv
enric_serra@enric-serra-Latitude-E7440:~/CLONE_report/invoice_report/test$ python ../invoice.py --invoice_tsv invoice_fail_sample_not_in_catalog.tsv --output_file out.txt --invoice_id 7020064998
http://10.0.32.140:8080/opencga/webservices/rest/v1/files/search/?sid=S0kqvloTb4hcyoBAZ3Wc&limit=-1&name=LP399950-DNA_B08.bam&bioformat=ALIGNMENT&studyId=2
Traceback (most recent call last):
  File "../invoice.py", line 114, in <module>
    exit(main())
  File "../invoice.py", line 28, in main
    raise Exception(invoice_errors)
Exception: LP399950-DNA_B08 was never found in catalog line 1


