# %%define functions
import os
import pandas as pd
from utils.file_utils import FileUtils
from utils.utils import Utils


def system_accuracy(results_json_path, source_of_truth_path) -> dict:
    #Define sumatory
    accuracy_sumatory=0

    sumatory_ocr_openai=[]
    sumatory_ocr_google=[]
    sumatory_ocr_aws_textract=[]
    sumatory_ocr_aws_parser=[]
    sumatory_entity_recognition_regex=[]
    sumatory_entity_recognition_openai=[]

    main_data=[]
    # Create a list and read all results in a loop
    all_results_files = FileUtils.list_text_files(results_json_path)
    results_count = len(all_results_files)
    if results_count < 1:
        return "Error: There is no file in the results path."
    for results in all_results_files:
        #Define variables
        found_count = 0
        fields_sot_count = 0
        document_source_of_truth = None
        temp_data=[]

        file_path = os.path.join(results_json_path, results)
        brut_result_json = FileUtils.read(file_path)
        brut_result_json = Utils.to_dict(brut_result_json)

        # Get name of document
        result_json_name = brut_result_json["name"].upper().strip()
        temp_data.append(result_json_name)
        # Get type of document
        result_json_type = brut_result_json["content"]
        temp_data.append(result_json_type)
        # Get ocr of document
        result_json_ocr = brut_result_json["ocr"]
        temp_data.append(result_json_ocr)
        # Get entity_recognition of document
        result_json_ent_rec = brut_result_json["entity_recognition"]
        temp_data.append(result_json_ent_rec)

        # Get source of truth
        source_file_name = result_json_type.strip() + "_source_of_truth.json"
        source_file_path = os.path.join(source_of_truth_path, source_file_name)
        source_of_truth = FileUtils.read(source_file_path)
        source_of_truth = source_of_truth.upper()
        source_of_truth = Utils.to_dict(source_of_truth)
        
        # Get result json
        result_json = brut_result_json["values"]
        result_json = Utils.decode_text(result_json)
        if result_json == "":
            print ("The result json is empty or does not exist...")
        if "null" or "NULL" or "Null" in result_json:
            result_json = result_json.replace("null", '"NA"')
        result_json_values = Utils.to_dict(result_json.upper())
        
        bool_nested_dict = False
        for valor in result_json_values.values():
            if isinstance(valor, dict):
                bool_nested_dict = True

        # Find document source of truth
        document_source_of_truth = source_of_truth.get(result_json_name,None)
        if document_source_of_truth is None:
            print(
                f"Error: The document {result_json_name} does not exists in the source of truth."
            )
        else:
            # print(f"document_source_of_truth:{document_source_of_truth}")
            for key, value in document_source_of_truth.items():
                fields_sot_count += 1
                if bool_nested_dict == False:
                    if result_json_values.get(key):
                        validate_json_value = str(result_json_values.get(key)).strip()
                        if str(value) in str(validate_json_value):
                            found_count += 1
                    else:
                        for json_key in result_json_values.keys():
                            if key in json_key:
                                validate_json_value = str(result_json_values.get(json_key)).strip()
                                if str(value) in str(validate_json_value):
                                    found_count += 1
                                    break
                else:
                    class Found(Exception): pass
                    try:
                        for json_key, nest_key in result_json_values.items():
                            if isinstance(nest_key, dict):
                                if result_json_values[json_key].get(key):
                                    validate_json_value = str(result_json_values[json_key].get(key)).strip()
                                    if str(value) in str(validate_json_value):
                                        found_count += 1
                                        raise Found
                                else:
                                    for values_results_json in result_json_values[json_key].values():
                                        if str(value) in str(values_results_json):
                                            found_count += 1
                                            raise Found
                            else:
                                if result_json_values.get(json_key):
                                    validate_json_value = str(result_json_values.get(json_key)).strip()
                                    if str(value) in str(validate_json_value):
                                        found_count += 1
                                        raise Found
                                elif key in json_key:
                                    validate_json_value = str(result_json_values.get(json_key)).strip()
                                    if str(value) in str(validate_json_value):
                                        found_count += 1
                                        raise Found
                    except Found:
                        continue

            accuracy = found_count / fields_sot_count
            temp_data.append(fields_sot_count)
            temp_data.append(found_count)
            temp_data.append(accuracy)
            main_data.append(tuple(temp_data))

            if result_json_ocr == 'openai':
                sumatory_ocr_openai.append(accuracy)
            elif result_json_ocr == 'google':
                sumatory_ocr_google.append(accuracy)
            elif result_json_ocr == 'aws_textract':
                sumatory_ocr_aws_textract.append(accuracy)
            elif result_json_ocr == 'aws_parser':
                sumatory_ocr_aws_parser.append(accuracy)
            
            if result_json_ent_rec == 'txt_extraction' or result_json_ent_rec == 'json_extraction':
                sumatory_entity_recognition_regex.append(accuracy)
            elif result_json_ent_rec =='chat_completions':
                sumatory_entity_recognition_openai.append(accuracy)
                

            accuracy_sumatory += accuracy
    
    total_accuracy=accuracy_sumatory/results_count
    print (f'\nTotal Accuracy:{str(round(total_accuracy,2))}')

    columns = ['# DOCUMENTS','OCR','ACCURACY']
    data_df =[(len(sumatory_ocr_openai),'OPEN AI',sum(sumatory_ocr_openai)/len(sumatory_ocr_openai))]
    data_df.append((len(sumatory_ocr_google),'GOOGLE',sum(sumatory_ocr_google)/len(sumatory_ocr_google)))
    data_df.append((len(sumatory_ocr_aws_textract),'AWS TEXTRACT',sum(sumatory_ocr_aws_textract)/len(sumatory_ocr_aws_textract)))
    data_df.append((len(sumatory_ocr_aws_parser),'AWS PARSER',sum(sumatory_ocr_aws_parser)/len(sumatory_ocr_aws_parser)))
    df = pd.DataFrame(data_df,columns=columns)
    df = df.round(2)
    # df = df.style.highlight_max(subset=['OCR','ACCURACY'],color="lightgreen").highlight_min(subset=['OCR','ACCURACY'],color="red")
    # df = df.to_string(index=False)
    # print (f'\n{df}\n')
    
    columns2 = ['# DOCUMENTS','EXTRACTION METHOD','ACCURACY']
    data_df2 =[(len(sumatory_entity_recognition_openai),'OPEN AI CC',sum(sumatory_entity_recognition_openai)/len(sumatory_entity_recognition_openai))]
    data_df2.append((len(sumatory_entity_recognition_regex),'REGEX',sum(sumatory_entity_recognition_regex)/len(sumatory_entity_recognition_regex)))
    df2 = pd.DataFrame(data_df2,columns=columns2)
    df2 = df2.round(2)
    # df2 = df2.style.highlight_max(subset=['EXTRACTION METHOD','ACCURACY'],color="lightgreen").highlight_min(subset=['EXTRACTION METHOD','ACCURACY'],color="red")
    # df2 = df2.to_string(index=False)
    # print (f'\n{df2}\n')

    columns3 = ['NAME DOC','TYPE DOC','OCR','ENT RECOG','# FIELDS','# FOUND FIELDS', 'ACCURACY']
    df3 = pd.DataFrame(main_data,columns=columns3)
    df3 = df3.round(2)
    # df3 = df3.style.highlight_max(subset=['# FIELDS','# FOUND FIELDS', 'ACCURACY'],color="lightgreen").highlight_min(subset=['# FIELDS','# FOUND FIELDS', 'ACCURACY'],color="red")
    # print (f'\n{df3}\n')
    try:
        with pd.ExcelWriter(os.getcwd()+"/df_results/accuracy_df.xlsx") as w:
            df.to_excel(w,sheet_name='A1', index=False, startrow=0,startcol=1)
            df2.to_excel(w,sheet_name='A1', index=False, startrow=len(df)+2,startcol=1)
            df3.to_excel(w,sheet_name='ALL DOCSACCURACY RESULTS', index=False, startrow=1,startcol=1)
    except Exception as e:
        return(f"Error:{e}, Failed to creating excel...")
                    
#%% Testeo
folder_base_path = os.getcwd()
results_folder = os.path.join(folder_base_path, "4_results")
source_truth_folder = os.path.join(folder_base_path, "source_of_truth")

system_accuracy(results_folder, source_truth_folder)