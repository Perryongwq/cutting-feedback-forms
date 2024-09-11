import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image, ImageDraw
import base64
import io
import os
from utils import send_email, to_excel, dire

# Function to render Page 3
def page_3():
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
        background-color: rgba(255, 240, 0, 1);
    }
    .toggle-box {
        padding-bottom: 0px;
    }
    </style>
    """

    # Load existing history from Excel file into session state if not already present
    history_file = dire.history_path_KEM
    if 'history_df_page3' not in st.session_state:
        if os.path.exists(history_file):
            st.session_state.history_df_page3 = pd.read_excel(history_file, engine='openpyxl')
        else:
            st.session_state.history_df_page3 = pd.DataFrame(columns=[
            'Date and Time', 'Lot Number', 'Item Type', 'ERST Machine No', 'MC Machine No', 'Cut Operator Payroll', 
            'NG Block/Lot', 'NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 'Defects', 'Judgement Block',
            'Shifting Amount', 'Shifting Direction',  'Quality Case'
            ])

    # Initialize grid state
    if 'grid' not in st.session_state:
        st.session_state.grid = [[False for _ in range(6)] for _ in range(6)]

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

    # st.markdown(' FORM NO: GE9106JO1701-00/10 / Appendix 7.17')
    st.title('B1 KEM cutting process feedback system')

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
        for key in ['lot_number', 'item_type', 'ERST_McNo', 'MC_MchNo', 'Cut_Operpayroll', 'NGNuofBLK_lot', 'NG_chip_qty_lot', 'block_number']:
            st.session_state[key] = ''
        for key in ['reason', 'defects', 'shift_direction']:
            st.session_state[key] = []
        for key in ['block']:
            st.session_state[key] = 'Good'
        for key in ['shift_amount']:
            st.session_state[key] = ''
        st.session_state.grid = [[False for _ in range(6)] for _ in range(6)]
        st.session_state.reset = False
        st.experimental_rerun()

    # Layout management
    col1, col2, col3, col4 = st.columns([1, 1, 2, 2])

    with col1:
        st.markdown(f"<div style='font-size:{font_size}px'>Date and Time:</div>", unsafe_allow_html=True)
        date_time = st.date_input('Date', datetime.now()).strftime('%Y-%m-%d') + ' ' + st.time_input('Time', datetime.now()).strftime('%H:%M:%S')
        
        st.markdown(f"<div style='font-size:{font_size}px'>Lot Number:</div>", unsafe_allow_html=True)
        lot_number = st.text_input('', key='lot_number', max_chars=10)

        st.markdown(f"<div style='font-size:{font_size}px'>Item Type:</div>", unsafe_allow_html=True)
        item_type = st.text_input('', key='item_type')

        st.markdown(f"<div style='font-size:{font_size}px'>ERST Machine No:</div>", unsafe_allow_html=True)
        ERST_McNo = st.text_input('', key='ERST_McNo')

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
        st.markdown(f"<div style='font-size:{font_size}px'>Reason:</div>", unsafe_allow_html=True)
        Reason_options = ['After Repair', 'After Shut Down', 'Change item', 'Others']
        selected_reason = st.multiselect('Select reason', Reason_options, key='reason')

        # Nested columns for Select All and Deselect All buttons
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            if st.button('Select All'):
                st.session_state.grid = [[True for _ in range(6)] for _ in range(6)]
        with col3_2:
            if st.button('Deselect All'):
                st.session_state.grid = [[False for _ in range(6)] for _ in range(6)]

        st.markdown("<div style='background-color: yellow; text-align: center; padding: 10px; font-size: 16px;'>ERST MACHINE BACKSIDE</div>", unsafe_allow_html=True)

        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                if cols[j].button(f'{i * 3 + j + 1}', key=f'{i}-{j}'):
                    toggle_grid(i, j)
                if st.session_state.grid[i][j]:
                    cols[j].markdown(f"<div style='width: 60px; height: 60px; background-color: rgba(255, 0, 0, 0.5); border: 1px solid black;'></div>", unsafe_allow_html=True)
                else:
                    cols[j].markdown(f"<div style='width: 60px; height: 60px; background-color: rgba(255, 255, 255, 0.5); border: 1px solid black;'></div>", unsafe_allow_html=True)

        st.markdown("<div style='background-color: yellow; text-align: center; padding: 10px; font-size: 16px;'>ERST MACHINE FRONT SIDE</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"<div style='font-size:{font_size}px; margin-right: 50px;'>Defect Name:</div>", unsafe_allow_html=True)
        defect_options = ['w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 'Slant Cut', 'Pattern dent', 'Dragging', 'Smearing', 'Partial print', 'Blunt cut', 'Others', 'Rough cut', 'VP dent', 'Line', 'Step Shift', 'Ridge/Dent']
        selected_defects = st.multiselect('Select defects', defect_options, key='defects')
        sub_col1, sub_col2, sub_col3 = st.columns(3)
        
        # Sub-column 1: Judgement
        with sub_col1:
            st.markdown(f"<div style='font-size:{font_size}px; margin-right: 50px;'>Judgement</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:{font_size}px; margin-right: 50px;'> Block :</div>", unsafe_allow_html=True)
            colorize_selectbox("", ['Good', 'NG'], key='block')
        # Sub-column 2: Shifting amount (micron)
        with sub_col2:
            st.markdown(f"<div style='font-size:{font_size}px'>Shifting Amount (micron)</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:{font_size}px'>Block :</div>", unsafe_allow_html=True)
            shift_amount = st.text_input('', key='shift_amount')


        # Sub-column 3: Shifting direction or mode
        with sub_col3:
            st.markdown(f"<div style='font-size:{font_size}px'>Shifting Direction or Mode</div>", unsafe_allow_html=True)
            direction_options = ['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good']
            st.markdown(f"<div style='font-size:{font_size}px'>Block A:</div>", unsafe_allow_html=True)
            shift_direction = st.multiselect('', direction_options, key='shift_direction')


        st.markdown(f"<div style='font-size:{font_size}px'>Quality Case:</div>", unsafe_allow_html=True)
        Quality_Case = ['open','close']
        selected_Case = st.selectbox('Select Case', Quality_Case, key='Case')

        st.markdown(f"<div style='font-size:{font_size}px'>Process Selection:</div>", unsafe_allow_html=True)
        process_options = ['Stacking Feedback', 'Cutting Feedback']
        selected_process = st.multiselect('Select Process', process_options, key='process')

    if st.button('Send Email'):
        if not (lot_number and item_type and ERST_McNo and MC_MchNo and Cut_Operpayroll and NGNuofBLK_lot and NG_chip_qty_lot and block_number and 
                confirm_date and photos and selected_reason and selected_defects and shift_amount and shift_direction and selected_process):
            st.error('Please fill all the fields and upload a photo.')
        else:
            if not os.path.exists('static/uploads/page3'):
                os.makedirs('static/uploads/page3')

            photo_paths = []
            for photo in st.session_state["uploaded_files"]:
                photo_path = f'static/uploads/page3/{photo.name}'
                with open(photo_path, 'wb') as f:
                    f.write(photo.getbuffer())
                photo_paths.append(photo_path)

            # Create a unique grid image path based on the date and time
            date_time_str = date_time.replace(" ", "_").replace(":", "-")
            grid_image_path = f'static/uploads/page3/grid_image_{date_time_str}.png'
            image = Image.new('RGB', (360, 360), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            for i in range(3):
                for j in range(3):
                    shape = [(j * 30, i * 30), (j * 30 + 30, i * 30 + 30)]
                    fill = "red" if st.session_state.grid[i][j] else "white"
                    draw.rectangle(shape, outline="black", fill=fill)
            
            image.save(grid_image_path)

            # Create the judgements dictionary
            judgements = {
                'block': st.session_state.block,
            }

            email_body = (f"Date and Time: {date_time}\n"
                        f"Lot Number: {lot_number}\n"
                        f"Item Type: {item_type}\n"
                        f"ERST Machine No: {ERST_McNo}\n"
                        f"MC Machine No: {MC_MchNo}\n"
                        f"Cut Operator Payroll: {Cut_Operpayroll}\n"
                        f"NG Block/Lot: {NGNuofBLK_lot}\n"
                        f"NG chip Qty/Lot(pcs): {NG_chip_qty_lot}\n"
                        f"Block Number: {block_number}\n"
                        f"Confirm Date: {confirm_date}\n"
                        f"Reason: {', '.join(selected_reason)}\n"
                        f"Defects: {', '.join(selected_defects)}\n"
                        f"Judgement Block: {judgements['block']}\n"
                        f"Shifting Amount: {shift_amount}\n"
                        f"Shifting Direction: {', '.join(shift_direction)}\n" 
                        f"Quality Case: {selected_Case}\n"
                        f"Process select: {', '.join(selected_process)}\n"
                        )

            # send_email('Details Submitted - B1 KEM Cutting Feedback', 'cutting_fb@murata.com', ['perry.ong@murata.com'], email_body, photo_paths, grid_image_path)
            send_email(
                'Details Submitted - B1 KEM Cutting Feedback', 
                'cutting_fb@murata.com', 
                [
                    'perry.ong@murata.com',
                    # 'mahesh.subramanian@murata.com'
                    # 'k.gopinath@murata.com',
                    # 'kumarsamy.mascow@murata.com',
                    # 'logenthan.ramachenderan@murata.com',
                    # 'ramesh.jayabalan@murata.com',s
                    # 'yogakumaran.krishnan@murata.com',
                    # 'reluvanullah.s@murata.com'
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
                'ERST Machine No': [ERST_McNo],
                'MC Machine No': [MC_MchNo],
                'Cut Operator Payroll': [Cut_Operpayroll],
                'NG Block/Lot': [NGNuofBLK_lot],
                'NG chip Qty/Lot(pcs)': [NG_chip_qty_lot],
                'Block Number': [block_number],
                'Confirm Date': [confirm_date],
                'Reason': [', '.join(selected_reason)],
                'Defects': [', '.join(selected_defects)],
                'Judgement Block': [judgements['block']],
                'Shifting Amount': [shift_amount],
                'Shifting Direction': [', '.join(shift_direction)],
                'Quality Case': [selected_Case],
                'Process select': [selected_process]
            })

            st.session_state.history_df_page3 = pd.concat([st.session_state.history_df_page3, new_entry], ignore_index=True)
            st.session_state.history_df_page3.to_excel(history_file, index=False, engine='openpyxl')

    # Write the CSS to the Streamlit app
    st.markdown(css, unsafe_allow_html=True)

    # Display history DataFrame
    st.write("### Summary History")
    st.dataframe(st.session_state.history_df_page3)

    st.download_button(
        label="Download History as Excel",
        data=to_excel(st.session_state.history_df_page3),
        file_name='history_B1.xlsx',
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
