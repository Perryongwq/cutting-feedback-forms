import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image, ImageDraw
import base64
import io
import os
from utils import send_email, to_excel, dire

# Function to render Page 1
def page_1():
    # Load the image and convert to base64
    background_image_path = dire.image_path
    image = Image.open(background_image_path)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Define CSS to control the image size and alignment
    css = """
    <style>
    .minimized-image {
        max-width: 100000px;  /* Set the maximum width */
        height: auto;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stSelectbox, .stTextInput, .stButton, .stDateInput, .stTimeInput, .stFileUploader {
        margin-bottom: 10px !important;
        height: 50px;
    }
    .stSelectbox > div, .stTextInput > div, .stButton > div, .stDateInput > div, .stTimeInput > div, .stFileUploader > div {
        display: flex;
        align-items: center;
    }
    .stSelectbox > div > div, .stTextInput > div > div, .stButton > div > div, .stDateInput > div > div, .stTimeInput > div > div, .stFileUploader > div > div {
        width: 100%;
    }
    .grid-box {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 50px;
        height: 50px;
        border: 1px solid black;
        margin-bottom: 1px;  
        margin-top: -30px;     
    }
    .grid-box.A {
        background-color: rgba(255, 0, 0, 0.5);
    }
    .grid-box.B {
        background-color: rgba(0, 255, 0, 0.5);
    }
    .grid-box.C {
        background-color: rgba(0, 0, 255, 0.5);
    }
    .grid-box.D {
        background-color: rgba(255, 255, 0, 1);
    }
    .toggle-box {
        padding-bottom: 0px;
    }
    </style>
    """

    # Load existing history from Excel file into session state if not already present
    history_file = dire.history_path_A1
    if 'history_df_page1' not in st.session_state:
        if os.path.exists(history_file):
            st.session_state.history_df_page1 = pd.read_excel(history_file, engine='openpyxl')
        else:
            st.session_state.history_df_page1 = pd.DataFrame(columns=[
                'Date and Time', 'Lot Number', 'Item Type', 'GSX Machine No', 'MC Machine No', 'Cut Operator Payroll', 
                'NG Block/Lot','NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 'Defects', 'Judgement Block A', 
                'Judgement Block B', 'Judgement Block C', 'Judgement Block D', 'Shifting Amount A', 'Shifting Amount B', 
                'Shifting Amount C', 'Shifting Amount D', 'Shifting Direction A', 'Shifting Direction B', 
                'Shifting Direction C', 'Shifting Direction D', 'Quality Case'
            ])

    if 'reset' not in st.session_state:
        st.session_state.reset = False

    def toggle_grid(row, col):
        st.session_state.grid[row][col] = not st.session_state.grid[row][col]

    def get_color(result):
        return 'green' if result == 'Good' else 'red'

    def colorize_selectbox(label, options, key):
        selected_option = st.selectbox(label, options, key=key)
        if selected_option == 'Good':
            color = 'green'
        else:
            color = 'red'
        st.markdown(f"<style>div[data-baseweb='select']>div{{border-color: {color};}}</style>", unsafe_allow_html=True)

    # Define font size
    font_size = 14

    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    st.markdown(' FORM NO: GE9106JO1701-00/10 / Appendix 7.17')
    st.title('A1 cutting process feedback system')

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    if st.button('Clear', key='clear_button'):
        st.session_state.reset = True
        st.session_state["file_uploader_key"] += 1
        st.session_state["uploaded_files"] = []
        st.experimental_rerun()



    if st.session_state.reset:
        for key in ['lot_number', 'item_type', 'GSX_McNo', 'MC_MchNo', 'Cut_Operpayroll', 'NGNuofBLK_lot', 'NG_chip_qty_lot', 'block_number']:
            st.session_state[key] = ''
        for key in ['reason', 'defects', 'shift_direction_a', 'shift_direction_b', 'shift_direction_c', 'shift_direction_d']:
            st.session_state[key] = []
        for key in ['block_a', 'block_b', 'block_c', 'block_d']:
            st.session_state[key] = 'Good'
        for key in ['shift_amount_a', 'shift_amount_b', 'shift_amount_c', 'shift_amount_d']:
            st.session_state[key] = ''
        st.session_state.grid = [[False for _ in range(6)] for _ in range(6)]
        st.session_state.reset = False
        st.experimental_rerun()

    # Layout management
    col1, col2, col3, col4 = st.columns([1, 1, 2, 2])

    with col1:
        st.markdown(f"<div style='font-size:{20}px'><b>Reason:</b></div>", unsafe_allow_html=True)
        Reason_options = ['After Repair', 'After Shut Down', 'Change item', 'Others']
        selected_reason = st.multiselect('Select reason', Reason_options, key='reason')

        st.markdown(f"<div style='font-size:{font_size}px'>Date and Time:</div>", unsafe_allow_html=True)
        date_time = st.date_input('Date', datetime.now()).strftime('%Y-%m-%d') + ' ' + st.time_input('Time', datetime.now()).strftime('%H:%M:%S')
        
        st.markdown(f"<div style='font-size:{font_size}px'>Lot Number:</div>", unsafe_allow_html=True)
        lot_number = st.text_input('', key='lot_number', max_chars=10)

        st.markdown(f"<div style='font-size:{font_size}px'>Item Type:</div>", unsafe_allow_html=True)
        item_type = st.text_input('', key='item_type')

        st.markdown(f"<div style='font-size:{font_size}px'>GSX Machine No:</div>", unsafe_allow_html=True)
        GSX_McNo = st.text_input('', key='GSX_McNo')

        st.markdown(f"<div style='font-size:{font_size}px'>MC Machine No:</div>", unsafe_allow_html=True)
        MC_MchNo = st.text_input('', key='MC_MchNo')
        

    with col2:
        st.markdown(f"<div style='font-size:{font_size}px'>Cut Operator Payroll:</div>", unsafe_allow_html=True)
        Cut_Operpayroll = st.text_input('', key='Cut_Operpayroll')
        
        st.markdown(f"<div style='font-size:{font_size}px'>NG Block/Lot:</div>", unsafe_allow_html=True)
        NGNuofBLK_lot = st.text_input('', key='NGNuofBLK_lot')

        st.markdown(f"<div style='font-size:{font_size}px'>NG chip Qty/Lot(pcs):</div>", unsafe_allow_html=True)
        NG_chip_qty_lot = st.text_input('', key='NG_chip_qty_lot')

        st.markdown(f"<div style='font-size:{font_size}px'>Block Number:</div>", unsafe_allow_html=True)
        block_number = st.text_input('', key='block_number')
        
        st.markdown(f"<div style='font-size:{font_size}px'>Confirm Date:</div>", unsafe_allow_html=True)
        confirm_date = st.date_input('', datetime.now()).strftime('%Y-%m-%d')

        st.markdown(f"<div style='font-size:{font_size}px'>Photo:</div>", unsafe_allow_html=True)
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0

        if "uploaded_files" not in st.session_state:
            st.session_state["uploaded_files"] = []

        photos = st.file_uploader(
            "",
            type=['jpg', 'jpeg', 'png'],
            key=st.session_state["file_uploader_key"],
            accept_multiple_files=True
        )

        if photos:
            st.session_state["uploaded_files"] = photos

        if st.button("Clear uploaded files"):
            st.session_state["file_uploader_key"] += 1
            st.session_state["uploaded_files"] = []
            st.experimental_rerun()

        st.write("Uploaded files:", [photo.name for photo in st.session_state["uploaded_files"]])

    with col3:


        # Nested columns for Select All and Deselect All buttons
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            if st.button('Select All'):
                st.session_state.grid = [[True for _ in range(6)] for _ in range(6)]
        with col3_2:
            if st.button('Deselect All'):
                st.session_state.grid = [[False for _ in range(6)] for _ in range(6)]

        # Grid state
        if 'grid' not in st.session_state:
            st.session_state.grid = [[False for _ in range(6)] for _ in range(6)]

        st.markdown("<div style='background-color: yellow; text-align: center; padding: 10px; font-size: 16px;'>GSX MACHINE BACKSIDE</div>", unsafe_allow_html=True)
        grid_labels = [["A"]*3 + ["B"]*3, ["A"]*3 + ["B"]*3, ["A"]*3 + ["B"]*3,
                ["C"]*3 + ["D"]*3, ["C"]*3 + ["D"]*3, ["C"]*3 + ["D"]*3]
        for i in range(6):
            cols = st.columns(6)
            if i ==2:
                st.markdown("<hr style='border-color: black; margin-bottom:-150px'>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)  
            for j in range(6):
                cell_style = ""
                if j == 2:  # Cells before j==3, to create a vertical line effect
                    cell_style = "border-right: 2px solid black; height: 50px;"


                if cols[j].button(f'{i*6 + j + 1}', key=f'grid-{i}-{j}'):
                    toggle_grid(i, j)
                label = grid_labels[i][j]
                if st.session_state.grid[i][j]:
                    cols[j].markdown(f"<div class='grid-box {label}'>{label}</div>", unsafe_allow_html=True)
                else:
                    cols[j].markdown(f"<div class='grid-box'>{label}</div>", unsafe_allow_html=True)

        st.markdown("<div style='background-color: yellow; text-align: center; padding: 10px; font-size: 16px;'>GSX MACHINE FRONT SIDE</div>", unsafe_allow_html=True)
    
    
    with col4:
        st.markdown(f"<div style='font-size:{font_size}px; margin-right: 50px;'>Defect Name:</div>", unsafe_allow_html=True)
        defect_options = ['w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 'Slant Cut', 'Pattern dent', 'Dragging', 'Smearing', 'Partial print', 'Blunt cut', 'Others', 'Rough cut', 'VP dent', 'Line', 'Step Shift', 'Ridge/Dent']
        selected_defects = st.multiselect('Select defects', defect_options, key='defects')
        sub_col1, sub_col2, sub_col3 = st.columns(3)
        
        # Sub-column 1: Judgement
        with sub_col1:
            st.markdown(f"<div style='font-size:{font_size}px; margin-right: 50px;'>Judgement</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:{font_size}px; margin-right: 50px;'> Block A:</div>", unsafe_allow_html=True)
            colorize_selectbox("", ['Good', 'NG'], key='block_a')
            st.markdown(f"<div style='font-size:{font_size}px'> Block B:</div>", unsafe_allow_html=True)
            colorize_selectbox("", ['Good', 'NG'], key='block_b')
            st.markdown(f"<div style='font-size:{font_size}px'> Block C:</div>", unsafe_allow_html=True)
            colorize_selectbox("", ['Good', 'NG'], key='block_c')
            st.markdown(f"<div style='font-size:{font_size}px'> Block D:</div>", unsafe_allow_html=True)
            colorize_selectbox("", ['Good', 'NG'], key='block_d')

        # Sub-column 2: Shifting amount (micron)
        with sub_col2:
            st.markdown(f"<div style='font-size:{font_size}px'>Shifting Amount (micron)</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:{font_size}px'>Block A:</div>", unsafe_allow_html=True)
            shift_amount_a = st.text_input('', key='shift_amount_a')
            st.markdown(f"<div style='font-size:{font_size}px'>Block B:</div>", unsafe_allow_html=True)
            shift_amount_b = st.text_input('', key='shift_amount_b')
            st.markdown(f"<div style='font-size:{font_size}px'>Block C:</div>", unsafe_allow_html=True)
            shift_amount_c = st.text_input('', key='shift_amount_c')
            st.markdown(f"<div style='font-size:{font_size}px'>Block D:</div>", unsafe_allow_html=True)
            shift_amount_d = st.text_input('', key='shift_amount_d')

        # Sub-column 3: Shifting direction or mode
        with sub_col3:
            st.markdown(f"<div style='font-size:{font_size}px'>Shifting Direction or Mode</div>", unsafe_allow_html=True)
            direction_options = ['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good']
            st.markdown(f"<div style='font-size:{font_size}px'>Block A:</div>", unsafe_allow_html=True)
            shift_direction_a = st.multiselect('', direction_options, key='shift_direction_a')
            st.markdown(f"<div style='font-size:{font_size}px'>Block B:</div>", unsafe_allow_html=True)
            shift_direction_b = st.multiselect('', direction_options, key='shift_direction_b')
            st.markdown(f"<div style='font-size:{font_size}px'>Block C:</div>", unsafe_allow_html=True)
            shift_direction_c = st.multiselect('', direction_options, key='shift_direction_c')
            st.markdown(f"<div style='font-size:{font_size}px'>Block D:</div>", unsafe_allow_html=True)
            shift_direction_d = st.multiselect('', direction_options, key='shift_direction_d')

        st.markdown(f"<div style='font-size:{font_size}px'>Quality Case:</div>", unsafe_allow_html=True)
        Quality_Case = ['open','close']
        selected_Case = st.selectbox('Select Case', Quality_Case, key='Case')

        st.markdown(f"<div style='font-size:{font_size}px'>Process Selection:</div>", unsafe_allow_html=True)
        process_options = ['Stacking Feedback', 'Cutting Feedback']
        selected_process = st.multiselect('Select Process', process_options, key='process')
        
    if st.button('Send Email'):
        if not (lot_number and item_type and GSX_McNo and MC_MchNo and Cut_Operpayroll and NGNuofBLK_lot and NG_chip_qty_lot and block_number and 
                confirm_date and photos and selected_reason and selected_defects and shift_amount_a and shift_amount_b and shift_amount_c and 
                shift_amount_d and shift_direction_a and shift_direction_b and shift_direction_c and shift_direction_d and selected_process):
            st.error('Please fill all the fields and upload a photo.')
        else:
            if not os.path.exists('static/uploads/page1'):
                os.makedirs('static/uploads/page1')

            photo_paths = []
            for photo in st.session_state["uploaded_files"]:
                photo_path = f'static/uploads/page1/{photo.name}'
                with open(photo_path, 'wb') as f:
                    f.write(photo.getbuffer())
                photo_paths.append(photo_path)

            # Create a grid image based on the current grid state
            date_time_str = date_time.replace(" ", "_").replace(":", "-")
            grid_image_path = f'static/uploads/page1/grid_image_{date_time_str}.png'
            # grid_image_path = 'static/uploads/page1/grid_image.png'
            image = Image.new('RGB', (360, 360), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            for i in range(6):
                for j in range(6):
                    shape = [(j * 60, i * 60), (j * 60 + 60, i * 60 + 60)]
                    fill = "red" if st.session_state.grid[i][j] else "white"
                    draw.rectangle(shape, outline="black", fill=fill)
            
            image.save(grid_image_path)

            # Create the judgements dictionary
            judgements = {
                'block_a': st.session_state.block_a,
                'block_b': st.session_state.block_b,
                'block_c': st.session_state.block_c,
                'block_d': st.session_state.block_d
            }

            email_body = (f"Reason: {', '.join(selected_reason)}\n"
                        f"Date and Time: {date_time}\n"
                        f"Lot Number: {lot_number}\n"
                        f"Item Type: {item_type}\n"
                        f"GSX Machine No: {GSX_McNo}\n"
                        f"MC Machine No: {MC_MchNo}\n"
                        f"Cut Operator Payroll: {Cut_Operpayroll}\n"
                        f"NG Block/Lot: {NGNuofBLK_lot}\n"
                        f"NG chip Qty/Lot(pcs): {NG_chip_qty_lot}\n"
                        f"Block Number: {block_number}\n"
                        f"Confirm Date: {confirm_date}\n"
                        f"Defects: {', '.join(selected_defects)}\n"
                        f"Judgement Block A: {judgements['block_a']}\n"
                        f"Judgement Block B: {judgements['block_b']}\n"
                        f"Judgement Block C: {judgements['block_c']}\n"
                        f"Judgement Block D: {judgements['block_d']}\n"
                        f"Shifting Amount A: {shift_amount_a}\n"
                        f"Shifting Amount B: {shift_amount_b}\n"
                        f"Shifting Amount C: {shift_amount_c}\n"
                        f"Shifting Amount D: {shift_amount_d}\n"
                        f"Shifting Direction A: {shift_direction_a}\n"
                        f"Shifting Direction B: {shift_direction_b}\n"
                        f"Shifting Direction C: {shift_direction_c}\n"
                        f"Shifting Direction D: {shift_direction_d}\n"
                        f"Quality Case: {selected_Case}\n"
                        f"Process select: {selected_process}\n"
                        )

            # send_email('Details Submitted- A1 Cutting Feedback', 'cutting_fb@murata.com', ['mahesh.subramanian@murata.com'], email_body, photo_path, grid_image_path)
            send_email(
                'Details Submitted - A1 Cutting Feedback', 
                'cutting_fb@murata.com', 
                [
                    'perry.ong@murata.com', 
                    'mahesh.subramanian@murata.com',
                    'jianfeng.yin@murata.com', 
                    'k.gopinath@murata.com',
                    'keigo.inata@murata.com', 
                    'kumarsamy.mascow@murata.com', 
                    'kursi.hanifaansarulla@murata.com', 
                    'freddy.fong@murata.com', 
                    'lemuel.viernes@murata.com', 
                    'muklesur.rahman@murata.com', 
                    'norzairey.binzainal@murata.com', 
                    'ramesh.jayabalan@murata.com', 
                    'ramkumar.venk@murata.com', 
                    'reluvanullah.s@murata.com', 
                    'gg.sankar@murata.com',
                    'yingping.foo@murata.com', 
                    'gurunathan.kum@murata.com', 
                    'sellamuthu.shamugam@murata.com', 
                    'woontak.tang@murata.com', 
                    'shooni.khor@murata.com', 
                    'chyansiang.goh@murata.com', 
                    'zhengpiau.tay@murata.com',
                    'logenthan.ramachenderan@murata.com',
                    'yogakumaran.krishnan@murata.com',
                    'junhui.zou@murata.com',
                    'kaidi.yau@murata.com',
                    'menghui.choy@murata.com',
                    'thiruppathi.balamurugan@murata.com',
                    'xudong.pan@murata.com',
                    'hywell.chong@murata.com'
                ], 
                email_body, 
                photo_paths, 
                grid_image_path
            )
            st.success('Email sent successfully!')

            # Add the new entry to the history DataFrame
            new_entry = pd.DataFrame({
                'Date and Time': [date_time],
                'Lot Number': [lot_number],
                'Item Type': [item_type],
                'GSX Machine No': [GSX_McNo],
                'MC Machine No': [MC_MchNo],
                'Cut Operator Payroll': [Cut_Operpayroll],
                'NG Block/Lot': [NGNuofBLK_lot],
                'NG chip Qty/Lot(pcs)': [NG_chip_qty_lot],
                'Block Number': [block_number],
                'Confirm Date': [confirm_date],
                'Reason': [', '.join(selected_reason)],
                'Defects': [', '.join(selected_defects)],
                'Judgement Block A': [judgements['block_a']],
                'Judgement Block B': [judgements['block_b']],
                'Judgement Block C': [judgements['block_c']],
                'Judgement Block D': [judgements['block_d']],
                'Shifting Amount A': [shift_amount_a],
                'Shifting Amount B': [shift_amount_b],
                'Shifting Amount C': [shift_amount_c],
                'Shifting Amount D': [shift_amount_d],
                'Shifting Direction A': [shift_direction_a],
                'Shifting Direction B': [shift_direction_b],
                'Shifting Direction C': [shift_direction_c],
                'Shifting Direction D': [shift_direction_d],
                'Quality Case': [selected_Case],
                'Process select': [selected_process]
            })

            st.session_state.history_df_page1 = pd.concat([st.session_state.history_df_page1, new_entry], ignore_index=True)
            st.session_state.history_df_page1.to_excel(history_file, index=False, engine='openpyxl')

    # Write the CSS to the Streamlit app
    st.markdown(css, unsafe_allow_html=True)

    # Display the image using HTML with the specified CSS class
    st.markdown(f'<img src="data:image/png;base64,{img_str}" class="minimized-image"/>', unsafe_allow_html=True)

    # Display history DataFrame
    st.write("### Summary History")
    st.dataframe(st.session_state.history_df_page1)

    st.download_button(
        label="Download History as Excel",
        data=to_excel(st.session_state.history_df_page1),
        file_name='history_A1.xlsx',
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    # # Login state management
    # if 'login' not in st.session_state:
    #     st.session_state.login = False

    # if st.session_state.login:
    #     # Button to clear history
    #     if st.button('Clear History'):
    #         st.session_state.confirm_clear = True

    # if 'confirm_clear' in st.session_state and st.session_state.confirm_clear:
    #     st.warning("Are you sure you want to clear the history?")
    #     if st.button('Yes, clear history'):
    #         # Save current history to desktop before clearing
    #         downloads_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    #         history_backup_file = os.path.join(downloads_path, 'history_A1_backup.xlsx')
    #         st.session_state.history_df_page3.to_excel(history_backup_file, index=False, engine='openpyxl')
    #         st.success(f'History saved to {history_backup_file}')

    #         # Clear history DataFrame
    #         history_df = pd.DataFrame(columns=[
    #             'Date and Time', 'Lot Number', 'Item Type', 'ERST Machine No', 'MC Machine No', 'Cut Operator Payroll', 
    #             'NG Block/Lot', 'NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 'Defects', 'Judgement Block A', 
    #             'Judgement Block B', 'Judgement Block C', 'Judgement Block D', 
    #             'Shifting Amount A', 'Shifting Amount B', 'Shifting Amount C', 'Shifting Amount D', 
    #             'Shifting Direction A', 'Shifting Direction B', 'Shifting Direction C', 'Shifting Direction D'
    #         ])
    #         history_df.to_excel(history_file, index=False, engine='openpyxl')
    #         st.success('History cleared and saved to desktop!')
    #         del st.session_state.confirm_clear

    #     if st.button('Cancel'):
    #         del st.session_state.confirm_clear

    # else:
    #     # Password input for clearing history
    #     password = st.text_input("Enter password to clear history:", type="password")
    #     if st.button("Login"):
    #         if password == "murata":
    #             st.session_state.login = True
    #             st.experimental_rerun()
    #         else:
    #             st.error("Incorrect password")


    # # Button to load history
    # if st.button('Load History'):
    #     # Path to the history backup file in Downloads
    #     downloads_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    #     history_backup_file = os.path.join(downloads_path, 'history_A1_backup.xlsx')
    #     history_file_path = dire.history_path_A1
        
    #     if os.path.exists(history_backup_file):
    #         # Read the history from the backup file
    #         new_history_df = pd.read_excel(history_backup_file, engine='openpyxl')
            
    #         # Check if history.xlsx exists and read it
    #         if os.path.exists(history_file_path):
    #             existing_history_df = pd.read_excel(history_file_path, engine='openpyxl')
    #             # Append new data
    #             history_df = existing_history_df.append(new_history_df, ignore_index=True)
    #         else:
    #             history_df = new_history_df
            
    #         # Write the updated DataFrame to history.xlsx in the specific folder
    #         history_df.to_excel(history_file_path, engine='openpyxl', index=False)
            
    #         # Load history into session state DataFrame
    #         st.session_state.history_df = history_df
    #         st.success('History loaded and appended successfully!')
    #     else:
    #         st.error('History backup file does not exist.')
