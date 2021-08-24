# import zipfile
# with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
#    zip_ref.extractall(directory_to_extract_to)

nstudy_data = dict()
nstudy_data['highlight_filename'] = "export_5534963e-049d-453a-9dab-93b911e9ece1_highlight_2021-08-04T18_13_46.716Z.csv"
nstudy_data['terms_filename'] = "export_5534963e-049d-453a-9dab-93b911e9ece1_term_2021-08-04T18_16_02.505Z.csv"
nstudy_data['notes_filename'] = "export_5534963e-049d-453a-9dab-93b911e9ece1_note_2021-08-04T18_14_43.718Z.csv"
user_id = "8e588dfd-c08a-4bb8-8a76-756dd4dab060"

def get_notes_analysis(notes_filename,user_id): # takes notes file and returns metrics computed on user created notes
  import pandas as pd
  notes_alldata = pd.read_csv('data/'+notes_filename)
  # filter out notes data for current user id
  notes_data = notes_alldata.loc[notes_alldata['userid']==user_id,:].copy()
  # filter out created notes
  notes_created = notes_data.loc[notes_data['event_name']=='create-note',:]
  # get number of notes created
  note_sum = notes_created.shape[0]
  # get a list of the types of notes created
  note_types_string_list =  list(set([row for row in notes_created['data_1'] if len(row)>1]))
  # filter out set-tags events
  notes_tags = notes_data.loc[notes_data['event_name']=='set-tags']
  # get number of set tags events
  notes_tag_sum = notes_tags.shape[0]
  # get a list of unique note tags created by user
  notes_tag_string_list = list(set([tuple(row) for row in notes_tags['data_1'] if len(row)>1]))
  #print(notes_tag_sum,notes_tag_string_list)
  return (note_sum,note_types_string_list,notes_tag_sum, notes_tag_string_list)

def get_highlights_analysis(highlight_filename,user_id): # takes highlights file and returns metrics computed on user created highlights
  import pandas as pd
  # get all highlight data passed by nstudy
  highlight_alldata = pd.read_csv('data/'+highlight_filename)
  # filter out data for current user only
  highlight_data = highlight_alldata.loc[highlight_alldata['userid']==user_id,:].copy()
  # delete the rest of the data
  try:
    del highlight_alldata
  except:
    pass
  # get the number of highlights created
  highlight_sum = highlight_data.loc[highlight_data['event_name']=='create-highlight'].shape[0]
  # get the number of tags created in highlights
  highlight_tags = highlight_data.loc[highlight_data['event_name']=='set-tags']
  highlight_tag_sum = highlight_tags.shape[0]
  # get the list of unique highlight tags
  highlight_tag_string_list = [tuple(eval(row)) for row in highlight_tags['data_1'] if len(row)>1]
  return (highlight_sum, highlight_tag_sum, highlight_tag_string_list)

def get_terms_analysis(terms_filename,user_id): # takes terms file and returns metrics computed on user created terms
  import pandas as pd
  # get all terms data passed by nstudy
  terms_alldata = pd.read_csv('data/'+terms_filename)
  # filter to terms data for current user
  terms_data = terms_alldata.loc[terms_alldata['userid']==user_id].copy()
  # get number of terms created by user
  term_sum = terms_data.loc[terms_data['event_name']=='create-term'].shape[0]
  # filter to the tags created by user
  terms_tags = terms_data.loc[terms_data['event_name']=='set-tags',:]
  # get the number of tags created by the user
  terms_tag_sum = terms_tags.shape[0]
  # get the list of unique tags created by the user
  terms_tag_string_list = [tuple(eval(row)) for row in terms_tags['data_1'] if len(row)>1]
  #print(terms_tag_sum,terms_tag_string_list)
  return (term_sum, terms_tag_sum,terms_tag_string_list)

def get_analysis_report(nstudy_data,user_id): # creates the feedback text to be printed in webpage
  import pandas as pd
  # assuming nstudy_data has the data in a dict format - this can be changed
  highlight_filename = nstudy_data['highlight_filename']
  terms_filename = nstudy_data['terms_filename']
  notes_filename = nstudy_data['notes_filename']
  # getting highlight metrics
  (highlight_sum, highlight_tag_sum, highlight_tag_string_list) = get_highlights_analysis(highlight_filename,user_id)

  # getting terms metrics
  (term_sum, terms_tag_sum,terms_tag_string_list) = get_terms_analysis(terms_filename,user_id)

  # getting notes metrics
  (note_sum,note_types_string_list,notes_tag_sum, notes_tag_string_list)= get_notes_analysis(notes_filename,user_id)

  # getting total number of unique tags
  total_tag_count = highlight_tag_sum + terms_tag_sum + notes_tag_sum

  # getting list of unique tags created by user
  list_unique_tags =  list(set(highlight_tag_string_list + terms_tag_string_list + notes_tag_string_list))

  # creating feedback text to be displayed based on computed metrics
  paragraph = "Students who studied the texts in a similar way to you and did well on the final assignment completed
  on average 5 more highlights compared to your "+str(highlight_sum)+" highlights.\nSections they focused on were
  X,Y and Z.\nYou used "+str(list_unique_tags)+" unique tags to classify information and they used 4 more
  unique tags than you did.\nYou used "+str(note_sum)+" notes, including "+str(notes_tag_string_list)+
  " and they created 2 more notes than you did. They identified on average 3 more terms and you created "
  +str(term_sum)+" terms."
  #print(paragraph)
  return paragraph
