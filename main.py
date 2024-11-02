from flask import Flask, request, send_file
import pandas as pd
import os
'''Objective:
The objective of this assignment is to create a Python program that calculates values for
columns D, E, F, G, H, I and J based on the provided Excel formula, using the input from
column C.
Instructions:
1. Follow standard Python code style practices (PEP-8).
2. Assignment should be a .py file.
3. If external packages are required, then don’t forget to add requirements.txt file.
4. Use meaningful variable names. Code should be properly structured and readable.
5. Try to write an optimized with minimum complexity.
Input Data:
The input data is provided in an attached sheet.
Download Link: Link
Calculation Rules:
Implement the Excel formula for each of the columns D, E, F, G, H, I, J.
You can find the Excel formula by double-clicking on the cell corresponding to each
column.
Python Program:
1. Make a http endpoint using any one of the python web frameworks – FastAPI or
Flask or Django
2. Upload downloaded hma.xls file using http endpoint
3. Write a function that reads hma.xls file and takes the input from Column C,
calculates the values for columns D, E, F, G, H, I, J & export a csv which will have
calculated columns.
Bonus:
If time permits, you can explore additional functionalities like input validation, error
handling, or optimizing the code for better performance.'''

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = "./temp/"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_columns(df):

    df['D'] = 0.0
    df['E'] = 0.0
    df['F'] = 0.0
    df['G'] = ''
    df['H'] = ''
    df['I'] = ''
    df['J'] = ''
    try:
        df.loc[0:, 'C'] = df.loc[1:, 'C'].apply(lambda x: round(x, 2))
        for i in range(1, len(df)):
            df.loc[i, 'D'] = round((df.loc[i, 'C'] - df.loc[i-1, 'C']),2)
        #print(df.head(5))
        df.loc[1:, 'E'] = df.loc[1:, 'D'].apply(lambda x: round(x,2) if x > 0 else 0)
        
        
        df.loc[1:, 'F'] = df.loc[1:, 'D'].apply(lambda x: round(-x,2) if x < 0 else 0)
        first_forteen_day_Avg_Gain=0.0
        first_forteen_day_Avg_Loss=0.0
        # import pdb
        # pdb.set_trace()
        for i in range(1,16):
            first_forteen_day_Avg_Gain += round(df.loc[i,'E'],2)
            first_forteen_day_Avg_Loss += round(df.loc[i,'F'],2)

        df.loc[14,'G']=round(first_forteen_day_Avg_Gain/14.0,2)
        df.loc[14,'H']=round(first_forteen_day_Avg_Loss/14.0,2)
        
        df.loc[13,'I']='HM'
        df.loc[13,'J']='HMA'


        
        for i in range(15, len(df)):

            df.loc[i, 'G'] = round((df.loc[i-1, 'G'] * 13.0 + df.loc[i, 'E']) / 14.0,2)
            
            df.loc[i, 'H'] = round((df.loc[i-1, 'H'] * 13 + df.loc[i, 'F']),2) / 14.0
        
        df.loc[14:, 'I'] = df.loc[14:].apply(
            lambda row: round(row['G'],2) / row['H'] if row['H'] != 0 else 0.0, 
            axis=1
        )
        
        df.loc[14:, 'J'] = df.loc[14:].apply(
            lambda row: 100 if row['H'] == 0 else round(100 - (100 / (1 + row['I'])),2), 
            axis=1
        )
        for i in range(14,len(df)):
            df.loc[i, 'I'] = round(df.loc[i,'I'],2)
            df.loc[i, 'H'] = round(df.loc[i,'H'],2)
        df.rename(columns={'D': 'Change', 'E': 'Gain', 'F': 'Loss', 'G': 'Avg Gain', 'H': 'Avg Loss', 'I': 'HM', 'J': 'HMA'}, inplace=True)
    
    except Exception as e:
        print(f"Some error occured while calculating columns. ERROR: {e}")
        raise e
    return df
    

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        print("file is allowed")
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            df = pd.read_excel(filepath, usecols=[0, 1, 2], names=['A', 'B', 'C'])
            result_df = calculate_columns(df)
            
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
            result_df.to_csv(output_path, index=False)
            
            return send_file(
                output_path,
                mimetype='application/csv',
                as_attachment=True,
                download_name='processed_file.csv'
            )
            
        except Exception as e:
            return str(e), 500
        
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
            # TODO: Uncomment the below lines to automatically remove the temporary file from the 
            # if os.path.exists(output_path):
            #     os.remove(output_path)
    
    return 'Invalid file type', 400


app.run(debug=True, port=8000)