import csv

def create_file(result, filename):
    filepath = '/tmp/' + filename
    fp = open(filepath, 'w')
    myFile = csv.writer(fp, dialect='excel')
    for item in result:
        myFile.writerow(item)
    fp.close()
    return fp;