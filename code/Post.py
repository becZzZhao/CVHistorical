import pandas as pd
import regex
import numpy as np
from functools import reduce
from datetime import datetime



class Post:
    @staticmethod
    def clean_header(header):
        # states = pd.read_csv('state_names.txt', sep = '\t')
        my_file = open("state_names.txt", "r")
        with open("state_names.txt") as f:
            state_list = f.read().splitlines()
        print(state_list)
        # print(states)
        department_name = header.iloc[0,0].strip().lower()
        office_and_state = header.iloc[1,0].split(sep = '—')
        office = office_and_state[0].strip().lower()
        myState = office_and_state[1]
        state_name = [x for x in state_list if regex.match("(?:%s){e<=1}" % x, myState) !=None ][0]



        print("State Name:  >%s< " % state_name)
        print("Department Name:  >%s< " % department_name)
        print("Office Name:  >%s< " %office)


class Name:
    @staticmethod
    def getName(str):
        # remove rows with just abbreviations, also reamoe abbrevivation.
        words = str.split(" ")
        myName = [name for name in words if len(name) > 1]
        if len(myName) == 0: myName = [np.nan]
        return myName[0]


    @staticmethod
    def map_process_names(census_chunk, col_name):
        df = census_chunk.groupby([col_name, 'YEAR']).size().reset_index().rename(columns={0:'count'})
        numRows_raw = df.shape[0]

        # remove strings containing non-alphabetical and lower case results.
        df =  df[~df[col_name].str.contains('[^A-Z\s]', regex= True, na=False)]
        numRows_clean = df.shape[0]
        # remove rows with just abbreviations, also reamoe abbrevivation.
        df[col_name] = df[col_name].apply(lambda x: Name.getName(x))
        df = df.dropna(how = 'any')
        numRows_complete = df.shape[0]
        df = df.drop(columns=[ 'count'])
        numUniqueNames = len(df[col_name].unique())

        meta = [numRows_raw, numRows_clean, numRows_complete, numUniqueNames]


        # print("%s%% of the name have either non-alphnermeric [?, *, []] patterns." % str(round(100-numRows_clean/numRows_raw*100,2)))
        # print("%s%% of the strings do not have a comeplete alphabetical name." % str(
        #     round(100 - numRows_complete / numRows_raw * 100, 2)))
        # print("%s unique names in found in the dataset. %s instance of name-year pair" % (len(df['NAMEFRST'].unique()), len(df['YEAR'].unique()) ))
        # print("output")

        return df, meta

    @staticmethod
    def genMeta(meta_list, meta_list_updates, col_name):
        if col_name == "NAMEFRST" or col_name == "NAMELAST":
            if meta_list == None:
                meta_list = meta_list_updates
            else:
                meta_list[0] += meta_list_updates[0]
                meta_list[1] += meta_list_updates[1]
                meta_list[2] +=  meta_list_updates[2]
                meta_list[3] += meta_list_updates[3]

        return meta_list

    @staticmethod
    def genMeta_output_info(final_meta_list, col_name, outpath):
        if col_name == "NAMEFRST" or col_name == "NAMELAST":
            numRows_raw = final_meta_list[0]
            numRows_clean = final_meta_list[1]
            numRows_complete = final_meta_list[2]
            numResults = final_meta_list[3]
            numUniqueName = final_meta_list[4]
            line0 = "Extracted on %s -- Variable <%s> from <1850-1880 Census>: " % (datetime.now(), col_name)
            line00 = "filepath: %s " % outpath
            line1 = "%s%% of the name have either non-alphnermeric [?, *, []] patterns."% str(round(100-numRows_clean/numRows_raw*100,2))
            line2 = "%s%% of the name contains abbreviations only, deleted."% str(round( (numRows_clean - numRows_complete) / numRows_raw * 100, 2))
            line3 = "%s unique names and %s unique name-year pair found out of %s names in the dataset. " % (numUniqueName,numResults,numRows_raw)

        return [line0, line1, line2, line3]

    @staticmethod
    def chunk_process(func , inpath, outpath, col_name, write_meta = False):
        result = None
        meta = None
        for chunk in pd.read_csv(inpath, chunksize=2500000):
            chunk_result, meta_updates = Name.map_process_names(chunk, col_name)
            meta = Name.genMeta(meta, meta_updates, col_name= col_name)
            if result is None:
                result = chunk_result
            else:
                result = pd.concat([result, chunk_result]).drop_duplicates().reset_index(drop=True)

        result.to_csv(outpath, index = False)

        # generate metadata
        meta.append(len(result))
        meta_info = Name.genMeta_output_info(meta, col_name = col_name, outpath = outpath)
        # io reference: https: // thispointer.com / how - to - append - text - or -lines - to - a - file - in -python /

        for line in meta_info:
            print(line)

        if write_meta == True:
            with open("meta_data.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)

                # Append text at the end of file
                for line in meta_info:
                    file_object.write("\n" + line)

                file_object.write("\n-------------------------------------------------------------------------")







# import pandas
# from functools import reduce
#
# def get_counts(chunk):
#     voters_street = chunk[
#         "Residential Address Street Name "]
#     return voters_street.value_counts()
#
# def add(previous_result, new_result):
#     return previous_result.add(new_result, fill_value=0)
#
# # MapReduce structure:
# chunks = pandas.read_csv("voters.csv", chunksize=1000)
# processed_chunks = map(get_counts, chunks)
# result = reduce(add, processed_chunks)
#
# result.sort_values(ascending=False, inplace=True)
# print(result)









