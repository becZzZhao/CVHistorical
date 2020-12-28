import pandas as pd
import regex
import numpy as np
from functools import reduce
from datetime import datetime



class Post:
    @staticmethod
    def analyze_page_sections(header):
        # takes a list of detected header OCR text results and locations. 
        # analyse the content of the text body and return the label and the location of diffrent sections.

        section_dict, other_sections = Post.check_header_info(header)


        # there are text body between each headers, so we use this to determine the location of the text body
        office_header_keys = [key for key in section_dict.keys() if regex.search('^office_header_',key)!=None]
        office_header_loc = [section_dict[key][1] for key in office_header_keys]

        table_body_loc = []
        for [text, (x,y,w,h)] in other_sections:
            if (w>1000 and h>400):
                table_body_loc.append(['table_body',(x,y,w,h)])

        table_body_key = ["table_body_%s"% str(i+1) for i in range(0,len(table_body_loc) )]

        # add text body information to ditionary
        i = 0
        for key in table_body_key:
            section_dict[key] = table_body_loc[i]
            i+=1

        # sort by y
        if section_dict['department_header']== '':
            print("no department header found")
            del section_dict['department_header']

        sorted_section_dict = {k: v for k, v in sorted(section_dict.items(), key=lambda item: item[1][1][1])}

        return sorted_section_dict

    @staticmethod
    def check_header_info(header_list):
        # p7 p16 problem
        numHeader_state = 0
        header_state_list = []
        department_header = ''
        others = []
        for [header, (x,y,w,h)] in header_list:
            header = regex.split('—|\s', header) # split by either space and "-" sign. | is a seperator for seperators.

            # check whehter the header is a department
            department_check = Post.check_department_info(header)
            if (department_check != None) and (department_header ==''):
                department_name = department_check
                department_header = [department_name,(x,y,w,h)]
                continue

            # check whether the header contains state informaiton
            office_and_state = [x for x in header if x != 'IN']
            state_names = Post.check_state_info(office_and_state)

            if state_names!=None:
                header_state_list.append([state_names[0], (x,y,w,h)])# on top of a page, there might be multiple state names in the header_state indicating the informaiton of the entire page
                                                        # select the first statename since it contains information about the immediate table box below.
                numHeader_state +=1
                continue

            else:
                others.append([header, (x,y,w,h)])

            # print(header_list)
            # print(department_header)
            # print(header_state_list)


        # creat a dictionary from state and department header
        headers_name_loc =header_state_list
        keys =  ["office_header_%s"%int(i+1) for i in range(numHeader_state)]
        header_dict = dict(zip(keys,headers_name_loc))

        # add department name and location to header
        header_dict['department_header'] = department_header

        return header_dict, others

    @staticmethod
    def check_department_info(header):
        department_name = ''
        for i in range(0, len(header)):
            if regex.match("(?:%s){e<=1}" % 'Department', header[i].title()) != None:
                department_name = ' '.join(header[:i+1]).title()
                return department_name
                break
            elif i == len(header):
                return None

    @staticmethod
    def check_state_info(header):

        my_file = open("state_names.txt", "r")
        with open("state_names.txt") as f:
            state_list = f.read().splitlines()
        state_names = []
        for myStr in header:
            myStr = myStr.title()
            fuzzy_search_thresh = max(int(len(myStr)*0.25),1)
            result = [x for x in state_list if regex.match("(?:%s){i<=%s,d<=%s,s<=%s,1i+2d+2s<=%s}" % (x,fuzzy_search_thresh,fuzzy_search_thresh, fuzzy_search_thresh, str(int(fuzzy_search_thresh)+2)), myStr) !=None ]
            if len(result) >0:
                state_names.append(result[0])
        if len(state_names)>0:
            return state_names
        else:
            return None

    @staticmethod
    def clean_header(header):
        # states = pd.read_csv('state_names.txt', sep = '\t')
        my_file = open("state_names.txt", "r")
        with open("state_names.txt") as f:
            state_list = f.read().splitlines()

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


            # stop_words = set(stopwords.words('english'))
            # filtered_sentence = [w for w in header if not w in stop_words]
            # print(filtered_sentence)






