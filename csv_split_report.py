from datetime import datetime
import argparse, csv, os, logging, chardet
import pandas as pd

FORMAT = "%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)

# command arguments
parser = argparse.ArgumentParser(
    description="csv to postgres", fromfile_prefix_chars="@"
)
parser.add_argument("file", help="csv file to import", action="store")
args = parser.parse_args()
csv_file = args.file


def make_owner_folders(date_time, filename="ownerslist.tsv"):
    """[summary]

    Args:
        datetime ([type]): [description]
        filename (str, optional): [description]. Defaults to "ownerslist.tsv".
        owners (list, optional): [description]. Defaults to [].

    Returns:
        [type]: [description]
    """
    owners=[]
    logging.info("Making Owner Folders")
    os.makedirs(date_time)
    with open(filename, "r") as file:
        csv_reader = csv.reader(file, delimiter="\t")
        for row in csv_reader:
            folder = row[1].split("@", maxsplit=1)[0]
            folder = folder.lower()
            if folder not in owners:
                owners.append(folder)
    for owner in owners:
        logging.debug("Making Owner Folder: {}".format(os.path.join(date_time, owner)))
        os.makedirs(os.path.join(date_time, owner))


def owner_dict(filename="ownerslist.tsv"):
    """[summary]

    Args:
        filename (str, optional): [description]. Defaults to "ownerslist.tsv".

    Returns:
        [type]: [description]
    """
    ownerdict = {}
    with open(filename, "r") as file:
        csv_reader = csv.reader(file, delimiter="\t")
        for row in csv_reader:
            owner = row[1].split("@", maxsplit=1)[0]
            instance = row[0]
            ownerdict[instance] = owner
    return ownerdict


def dataframe_generator(filename):
    return pd.read_csv(
        filename, delimiter="\t", na_filter=False, encoding=get_encoding(filename)
    )


def pandas_make_files(date_path, df):
    """[summary]

    Args:
        date_path ([type]): [description]
        df ([type]): [description]
    """
    logging.info("Making excel files.")
    df.columns = [c.replace(" ", "_").replace("/", "-") for c in df.columns]
    ownerdict = owner_dict()
    cvss_score = 7.0
    for i in df.Host_Name.unique():
        logging.debug("Working on {}".format(i))
        try:
            xlsx_filename = (
                date_path
                + "/"
                + ownerdict[i.replace("/", "-")]
                + "/"
                + i.replace("/", "-")
                + ".xlsx"
            )
        except:
            xlsx_filename = date_path + "/" + i.replace("/", "-") + ".xlsx"
        writer = pd.ExcelWriter(xlsx_filename, engine="xlsxwriter")
        # text_format = workbook.add_format({"text_wrap": True, "valign": "top"})
        idf = df.loc[(df["Host_Name"].astype(str) == i)]
        jdf = idf.loc[(df["CVSS_Score_"].astype(float) > cvss_score)]
        logging.debug(jdf)
        jdf.to_excel(
            excel_writer=writer,
            index=False,
            sheet_name=i.replace("/", "-")[:29],
        )  # send df to writer
        writer.save()


def get_encoding(file):
    """[summary]

    Args:
        csv_file ([type]): [description]
    """
    with open(file, "rb") as rawdata:
        result = chardet.detect(rawdata.read(10000))
    return result["encoding"]


if __name__ == "__main__":
    """[summary]"""
    now = datetime.now()
    logging.info(now)
    make_owner_folders(now.strftime("%Y%m%d"))
    pandas_make_files(now.strftime("%Y%m%d"), dataframe_generator(csv_file))
    end = datetime.now()
    logging.info(end)
