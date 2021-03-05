import sys, argparse, csv, os
from datetime import datetime

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

def remove_lfcr(csv_string):
    for row in csv_string:
        row.strip('\r\n')
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file,delimiter='\t')
        firstrow=next(csv_reader)
        temp_row.append([])
        csv_string += ','.join(temp_row) + '\n'
        with open(filename, "a+") as outputfile:
            file_writer = csv.writer(outputfile,delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
            file_writer.writerow(firstrow)
            for row in csv_reader:
                    file_writer.writerow(row)
    return

def fix_quotes(csv_file):
    filename = "fixed_tsv.tsv"
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file,delimiter='\t')
        firstrow=next(csv_reader)
        with open(filename, "a+") as outputfile:
            file_writer = csv.writer(outputfile,delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
            for row in csv_reader:
                temp_row.append([])
                file_writer.writerow(row)
    return

def make_files(path, hosts, firstrow, csv_file):
    ownerdict = owner_dict()
    for i in hosts:
        try:            
            filename = path + "/" +  ownerdict[i.replace("/","-")] + "/" + i.replace("/","-") + ".tsv"
        except:
            filename = path + "/" + i.replace("/","-") + ".tsv"
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file,delimiter='\t')
            firstrow=next(csv_reader)
            with open(filename, "a+") as outputfile:
                file_writer = csv.writer(outputfile,delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
                file_writer.writerow(firstrow)
                for row in csv_reader:
                    if (row[6]==i):
                        file_writer.writerow(row)
    return

def get_first_row(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f,delimiter='\t')
        return(next(reader))  # gets the first line
    
def make_owner_folders(datetime,filename="ownerslist.tsv", owners=[]):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file,delimiter='\t')
        for row in csv_reader:
            folder = row[1].split("@",maxsplit=1)[0]
            folder = folder.lower()
            if folder not in owners:
                owners.append(folder)
    for owner in owners:
        #print(owner)
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
    os.makedirs(os.path.join(now.strftime("%Y%m%d")))
    ownerscsv=make_owner_folders(now.strftime("%Y%m%d"))
    make_files(now.strftime("%Y%m%d"), get_unique_hosts(csv_file), get_first_row(csv_file),csv_file)
    