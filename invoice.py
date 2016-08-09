import argparse
from pyCGA.CatalogWS import *


def main():

    options = get_options()
    invoice_file = open(options.invoice_tsv, 'r')
    files_cga = Files()
    line_number = 0
    invoice_errors = ""
    invoice_report_header = ("SampleName\tIllumina_Experiment_Type\tIllumina_Workflow\t"
                             "Illumina_Date\tGEL_BAM\tGEL_Type\tGEL_BAM_Date\tGEL_BAM_Size\n")
    output_file = open(options.output_file, 'w')
    output_file.write(invoice_report_header)
    error_file = open(options.error_file, 'w')

    for invoice_line in invoice_file:

        line_number += 1
        sample_name, illumina_type, illumina_workflow, illumina_date = illumina_line_to_human_readable(invoice_line)
        bamfile_res = query_bamfile_using_sample_name(sample_name, files_cga)

        if len(bamfile_res) > 1:

            invoice_errors = more_than_one_in_catalog(invoice_errors, bamfile_res.count(), sample_name, line_number)

        if len(bamfile_res) == 0:

            invoice_errors = not_found_in_catalog(invoice_errors, sample_name, line_number)

        for this_bamfile in bamfile_res:

            if 'invoicing' in this_bamfile['attributes'].keys():
                invoice_errors = already_invoiced(invoice_errors, sample_name, this_bamfile['attributes']['invoicing'],
                                                  line_number)
            else:
                bamfile = query_bamfile_using_sample_name(sample_name, files_cga)[0]
                gel_type, gel_size,gel_date, gel_path = gel_query_to_human_readable(bamfile)
                output_file.write(sample_name + "\t" + illumina_type + "\t" + illumina_workflow + "\t" + illumina_date +
                                  "\t" + gel_path + "\t" + gel_type + "\t" + gel_date + "\t" + gel_size + "\n")

    if invoice_errors != "":

    error_file.write(invoice_errors)
        raise Exception(invoice_errors)

    invoice_file.close()
    invoice_file = open(options.invoice_tsv, 'r')

    for invoice_line in invoice_file:

        sample_name, illumina_type, illumina_workflow, illumina_date = illumina_line_to_human_readable(invoice_line)
        bamfile = query_bamfile_using_sample_name(sample_name, files_cga)[0]
        gel_type, gel_size,gel_date, gel_path = gel_query_to_human_readable(bamfile)
        bamfile["attributes"]["invoicing"] = {"invoice_id": options.invoice_id, "invoice_date": illumina_date}

        if invoice_errors != "":

            data_json = {"attributes":{"invoice_id": options.invoice_id, "invoice_date": illumina_date}}
            update_file_post(files, bamfile, data_json)



def get_options():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--invoice_tsv',
                        dest='invoice_tsv',
                        required=True,
                        )
    parser.add_argument('--invoice_id',
                        dest="invoice_id",
                        required=True,
                        )
    parser.add_argument('--output_file',
                        dest="output_file",
                        required=True,
                        )
    parser.add_argument('--error_file',
                        dest="error_file",
                        required=True,
                        )

    options = parser.parse_args()
    return options


def illumina_line_to_human_readable(invoice_line):

    line = (invoice_line.replace("\n", "")).split("\t")
    return line[0], line[1], line[2], line[3]


def gel_query_to_human_readable(bamfile_query):

    return bamfile_query["stats"]["GEL_METRICS"]["DirectoryType"], str(bamfile_query["diskUsage"]/(2**30)) + " GB",\
           date_to_human_readable(bamfile_query["creationDate"]) , get_abs_gel_path(bamfile_query["path"])


def date_to_human_readable(date_to_restore):

    return date_to_restore[0:4] + "-" + date_to_restore[4:6] + "-" + date_to_restore[6:8] + " " + \
           date_to_restore[8:10] + ":" + date_to_restore[10:12] + ":" + date_to_restore[12:14]


def get_abs_gel_path(relative_path, gel_default = "/genomes/"):
    return gel_default + relative_path


def already_invoiced(previous_errors, sample_name, previous_invoicing, line_number):

    return previous_errors + 'Sample ' + sample_name + ' already invoiced ' + str(previous_invoicing) +\
           ' line ' + str(line_number) + '\n'


def not_found_in_catalog(previous_errors, sample_name, line_number):

    return previous_errors + sample_name + ' was never found in catalog line ' + str(line_number) + '\n'


def more_than_one_in_catalog(previous_errors, counts, sample_name, line_number):

    return previous_errors + 'Catalog has more than one entrance (' + counts + ') for sample ' + sample_name + ' line '\
           + str(line_number) + '\n'


def reformat_date(date_column):

    date_column_to_replace = date_column.replace("\n", "")
    return date_column_to_replace.replace("/", "").split(" ")[0] + "_" + date_column_to_replace.split(" ")[1]


def update_file_post(object, bamfile, data_json):

    return object.update_file_post(str(bamfile["id"]), data = data_json)


def query_bamfile_using_sample_name(sample_name, files):

    return files.search(studyId="2", name=sample_name + ".bam", bioformat="ALIGNMENT")


if __name__ == "__main__":
    exit(main())
