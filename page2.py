import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image, ImageDraw
import os
from utils import send_email, to_excel, dire

def page_2():

    history_file = dire.history_path_GHM

    # Load existing history from Excel file
    if os.path.exists(history_file):
        history_df = pd.read_excel(history_file, engine='openpyxl')
    else:
        history_df = pd.DataFrame(columns=[
            'Date and Time', 'Lot Number', 'Item Type', 'MLN Machine No', 'MC Machine No', 'Cut Operator Payroll', 
            'NG Block/Lot', 'NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 'Defects', 'Judgement',
            'Shifting Amount', 'Shifting Direction', 'Quality_Case'
        ])

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
        .stSelectbox, .stTextInput, .stButton {
            margin-bottom: 0px !important;
        }
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    st.markdown(' FORM NO: GE9106JH1701-00/11')

    st.title('GHM cutting process feedback system')

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
        for key in ['lot_number', 'item_type', 'MLN_McNo', 'MC_MchNo', 'Cut_Operpayroll', 'NGNuofBLK_lot', 'NG_chip_qty_lot', 'block_number']:
            st.session_state[key] = ''
        for key in ['reason', 'defects', 'shift_direction']:
            st.session_state[key] = []
        st.session_state['block'] = 'Good'
        st.session_state['shift_amount'] = ''
        st.session_state.grid = [[False for _ in range(3)] for _ in range(3)]
        st.session_state.reset = False
        st.experimental_rerun()
    # Layout management
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"<div style='font-size:{font_size}px'>Date and Time:</div>", unsafe_allow_html=True)
        date_time = st.date_input('Date', datetime.now()).strftime('%Y-%m-%d') + ' ' + st.time_input('Time', datetime.now()).strftime('%H:%M:%S')
        
        st.markdown(f"<div style='font-size:{font_size}px'>Lot Number:</div>", unsafe_allow_html=True)
        lot_number = st.text_input('', key='lot_number')

        st.markdown(f"<div style='font-size:{font_size}px'>Item Type:</div>", unsafe_allow_html=True)
        item_type = st.text_input('', key='item_type')

        st.markdown(f"<div style='font-size:{font_size}px'>MLN Machine No:</div>", unsafe_allow_html=True)
        MLN_McNo = st.text_input('', key='MLN_McNo')

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
        # Clear Image button functionality
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

        # Grid state
        if 'grid' not in st.session_state:
            st.session_state.grid = [[False for _ in range(3)] for _ in range(3)]

        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                if cols[j].button(f'{i * 3 + j + 1}', key=f'{i}-{j}'):
                    toggle_grid(i, j)
                if st.session_state.grid[i][j]:
                    cols[j].markdown(f"<div style='width: 60px; height: 60px; background-color: rgba(255, 0, 0, 0.5); border: 1px solid black;'></div>", unsafe_allow_html=True)
                else:
                    cols[j].markdown(f"<div style='width: 60px; height: 60px; background-color: rgba(255, 255, 255, 0.5); border: 1px solid black;'></div>", unsafe_allow_html=True)

        st.markdown("<div style='background-color: yellow; text-align: center; padding: 10px; font-size: 16px;'>MLN MACHINE FRONT SIDE</div>", unsafe_allow_html=True)

    with col4:
        st.markdown(f"<div style='font-size:{font_size}px'>Defect Name:</div>", unsafe_allow_html=True)
        defect_options = ['w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 'Slant Cut', 'Pattern dent', 'Smearing', 'Partial print', 'Blunt cut', 'Others', 'Rough cut', 'VP dent','Step Shift', 'Ridge/Dent','Sample','Drop Chips']
        selected_defects = st.multiselect('Select defects', defect_options, key='defects')
        sub_col1, sub_col2, sub_col3 = st.columns(3)
        
        # Sub-column 1: Judgement
        with sub_col1:
            st.markdown(f"<div style='font-size:{font_size}px'>Judgement</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:{font_size}px'>Judgement Block A:</div>", unsafe_allow_html=True)
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
        if not (lot_number and item_type and MLN_McNo and MC_MchNo and Cut_Operpayroll and NGNuofBLK_lot and NG_chip_qty_lot and block_number and 
                confirm_date and photos and selected_reason and selected_defects and shift_amount and shift_direction and selected_process):
            st.error('Please fill all the fields and upload a photo.')
        else:
            if not os.path.exists('static/uploads/page2'):
                os.makedirs('static/uploads/page2')

            photo_paths = []
            for photo in st.session_state["uploaded_files"]:
                photo_path = f'static/uploads/page2/{photo.name}'
                with open(photo_path, 'wb') as f:
                    f.write(photo.getbuffer())
                photo_paths.append(photo_path)

            # Create a grid image based on the current grid state
            date_time_str = date_time.replace(" ", "_").replace(":", "-")
            grid_image_path = f'static/uploads/page2/grid_image_{date_time_str}.png'
            # grid_image_path = 'static/uploads/page2/grid_image.png'
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
                        f"MLN Machine No: {MLN_McNo}\n"
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
                        f"Process select: {selected_process}\n"
                        )

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
                'MLN Machine No': [MLN_McNo],
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

            history_df = pd.concat([history_df, new_entry], ignore_index=True)
            history_df.to_excel(history_file, index=False, engine='openpyxl')

    # Display history DataFrame
    st.write("### Summary History")
    st.dataframe(history_df)

    st.download_button(
        label="Download History as Excel",
        data=to_excel(history_df),
        file_name='history.xlsx',
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # # Button to clear history
    # if st.button('Clear History'):
    #     # Save current history to desktop before clearing
    #     desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    #     history_backup_file = os.path.join(desktop_path, 'history_GHM_backup.xlsx')
    #     history_df.to_excel(history_backup_file, index=False, engine='openpyxl')
    #     st.success(f'History saved to {history_backup_file}')

    #     # Clear history DataFrame
    #     history_df = pd.DataFrame(columns=[
    #         'Date and Time', 'Lot Number', 'Item Type', 'MLN Machine No', 'MC Machine No', 'Cut Operator Payroll', 
    #         'NG Block/Lot', 'NG chip Qty/Lot(pcs)', 'Block Number', 'Confirm Date', 'Reason', 'Defects', 'Judgement', 
    #         'Shifting Amount', 'Shifting Direction'
    #     ])
    #     history_df.to_excel(history_file, index=False, engine='openpyxl')
    #     st.success('History cleared and saved to desktop!')
