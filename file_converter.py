# import streamlit as st
# import pandas as pd
# from io import BytesIO

# st.set_page_config(page_title="File Converter", layout="wide")
# st.title("File Converter & Cleaner")
# st.write("This app is designed to help you convert and clean your data files. Please upload your file and select the appropriate options.")

# files = st.file_uploader("Upload your file", type=["csv", "xlsx"],accept_multiple_files=True)
# if files:
#     for file in files :
#         ext = file.name.split('.')[-1]
#         df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)

#         st.subheader(f'{file.name} - Preview')
#         st.dataframe(df.head())

# if st.checkbox (f"Remove Duplicates - {file.name}"):
#     df= df.drop_duplicates()
#     st.success("Duplicates removed successfully")   
#     st.dataframe(df.head())

        
#         if st.checkbox(f'Fill Missing values - {file.name}'):
#             df = fileno(df.select_dtypes(include=['number']).mean(),inplace=True)
#             st.success("Missing values filled successfully")
#             st.dataframe(df.head())

#             selected_columns = st.multiselect(f"Select columns to drop - {file.name}", df.columns,default=df.columns)
#             df = df[selected_columns]
#             st.dataframe(df.head())

#             if st.checkbox(f"show chart - {file.name}" and not df.select_dtypes(include=['number']).empty):
#                 st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

#                 format_choice = st.radio(f"Convert {file.name} to:",["csv","xlsx"], key=file.name)
                
#                 if st.button(f"Download {file.name} as {format_choice}"):
#                     output = BytesIO()
#                     if format_choice == 'csv':
#                         df.to_csv(output, index=False)
#                         mine = 'text/csv'
#                         new_name = file.name.replace(ext,'csv')
#                     else:
#                         df.to_excel(output, index=False, engine="openpyxl")
#                         mine = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#                     new_name = file.name.replace(ext,'xlsx')

#                     output.seek(0)
#                     st.set_download_button(new_name,data=output, mime=mine)  

#                     st.success('Processing completed!')   
import streamlit as st
import pandas as pd
from io import BytesIO

# Streamlit Page Config
st.set_page_config(page_title="File Converter", layout="wide")

# Title & Instructions
st.title("File Converter & Cleaner")
st.write("Upload your file and select the options to clean, analyze, and convert your data.")

# File Upload Section
files = st.file_uploader("Upload your file", type=["csv", "xlsx"], accept_multiple_files=True)

# Session state to store modified data
if "data" not in st.session_state:
    st.session_state.data = {}

if files:
    for file in files:
        ext = file.name.split('.')[-1]
        df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)

        # Store original data only once
        if file.name not in st.session_state.data:
            st.session_state.data[file.name] = df.copy()

        st.subheader(f'{file.name} - Data Preview')
        st.dataframe(st.session_state.data[file.name])  # ✅ Full Data Show Karega

        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            st.session_state.data[file.name] = st.session_state.data[file.name].drop_duplicates()
            st.success("✅ Duplicates Removed!")
            st.dataframe(st.session_state.data[file.name])  # ✅ Updated Data Show

        # Fill Missing Values
        if st.checkbox(f'Fill Missing Values - {file.name}'):
            df_numeric = st.session_state.data[file.name].select_dtypes(include=['number'])
            st.session_state.data[file.name].fillna(df_numeric.mean(), inplace=True)
            st.success("✅ Missing Values Filled!")
            st.dataframe(st.session_state.data[file.name])  # ✅ Updated Data Show

        # Column Selection
        selected_columns = st.multiselect(f"Select Columns to Keep - {file.name}", 
                                          st.session_state.data[file.name].columns, 
                                          default=st.session_state.data[file.name].columns)
        st.session_state.data[file.name] = st.session_state.data[file.name][selected_columns]
        st.dataframe(st.session_state.data[file.name])  # ✅ Updated Data Show

        # Show Chart (Only if there are numeric columns)
        if not st.session_state.data[file.name].select_dtypes(include=['number']).empty:
            if st.checkbox(f"Show Chart - {file.name}"):
                st.bar_chart(st.session_state.data[file.name].select_dtypes(include=['number']).iloc[:, :2])

        # File Format Conversion
        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "xlsx"], key=file.name)

        # Download Button
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == 'csv':
                st.session_state.data[file.name].to_csv(output, index=False)
                mime_type = 'text/csv'
                new_name = file.name.replace(ext, 'csv')
            else:
                st.session_state.data[file.name].to_excel(output, index=False, engine="openpyxl")
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                new_name = file.name.replace(ext, 'xlsx')

            output.seek(0)
            st.download_button(f"Download {new_name}", data=output, file_name=new_name, mime=mime_type)
            st.success('✅ Processing Completed!')
