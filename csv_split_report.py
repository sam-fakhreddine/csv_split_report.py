import sys, argparse, csv, os
from datetime import datetime
from xlsxwriter.workbook import Workbook
import logging
import functools

FORMAT = "%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)

# command arguments
parser = argparse.ArgumentParser(description='csv to postgres',\
 fromfile_prefix_chars="@" )
parser.add_argument('file', help='csv file to import', action='store')
args = parser.parse_args()
csv_file = args.file

def get_unique_hosts(csv_file):
    hosts = list()
    with open(csv_file, 'rt') as f:
        csv_reader = csv.reader(f,delimiter='\t')
        for line in csv_reader:
            hosts.append(line[6])
    return(list(set(hosts)))      

def make_files(path, hosts, csv_file):
    ownerdict = owner_dict()
    
    for i in hosts:
        columnwidths={}
        logging.info("Working on {}".format(i))
        newrow=0

        try:            
            #filename = path + "/" +  ownerdict[i.replace("/","-")] + "/" + i.replace("/","-") + ".tsv"
            xlsx_filename = path + "/" +  ownerdict[i.replace("/","-")] + "/" + i.replace("/","-") + ".xlsx"
        except:
            #filename = path + "/" + i.replace("/","-") + ".tsv"
            xlsx_filename = path + "/" + i.replace("/","-") + ".xlsx"
        workbook = Workbook(xlsx_filename)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        text_format = workbook.add_format({'text_wrap': True, 'valign': "top" })
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file,delimiter='\t')
            firstrow = next(csv_reader)
            for r, row in enumerate(csv_reader):
                widths={}
                widths.clear()
                if ((i in "hanastack-init/hana") and float(row[23])>=7):
                    newrow = newrow+1
                    for c, col in enumerate(row):                        
                        logging.debug("Writing: row: {} col: {} in {}".format(newrow,c,xlsx_filename))
                        worksheet.write(newrow, c, col,text_format)
                        #worksheet.set_column(c, c, len(col)+2)\
                        widths[c]=(len(col.split("\n\n",maxsplit=1)[0]))
                        #widths[c]=len(col)
                columnwidths[newrow]= widths
            logging.info(columnwidths)
            columns = []
            if newrow > 0:                
                for c, col in enumerate(firstrow):
                    columns.append({'header':col})
                    worksheet.write(0,c,col,bold)
                    logging.debug(columns)
            worksheet.add_table(0,0,newrow,24, {'columns': columns})                
        workbook.close()
    return


def column_widiths():
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
    return


def make_owner_folders(datetime,filename="ownerslist.tsv", owners=[]):
    os.makedirs(datetime)
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file,delimiter='\t')
        for row in csv_reader:
            folder = row[1].split("@",maxsplit=1)[0]
            folder = folder.lower()
            if folder not in owners:
                owners.append(folder)
    for owner in owners:
        logging.debug(os.path.join(datetime,owner))
        os.makedirs(os.path.join(datetime,owner))
    return()

def owner_dict(filename="ownerslist.tsv"):
    ownerdict = {}
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file,delimiter='\t')
        for row in csv_reader:
            owner=row[1].split("@",maxsplit=1)[0]
            instance=row[0]
            ownerdict[instance]=owner
    return ownerdict

""" def convert_to_utf8(csv_file):
    with open(csv_file, 'r', encoding='utf16') as csvf:
    for line in csv.reader(csvf):
        temp_row.append([])
        csv_string += ','.join(temp_row) + '\n'
    return(csv_string) """

if __name__ == '__main__':
    now = datetime.now()
    make_owner_folders(now.strftime("%Y%m%d"))
    make_files(now.strftime("%Y%m%d"), get_unique_hosts(csv_file), csv_file)
    