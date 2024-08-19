import os
import io
import pandas as pd
from flask_mail import Mail, Message
from flask import Flask
from PIL import Image, ImageDraw
from dotenv import load_dotenv

load_dotenv()

# Common directory paths
class directory():
    src_path = os.path.dirname(__file__)
    image_path = os.path.join(src_path, 'cutfb.png')
    history_path_A1 = os.path.join(src_path, 'history_A1.xlsx')
    history_path_GHM = os.path.join(src_path, 'history_GHM.xlsx')
    history_path_KEM = os.path.join(src_path, 'history_KEM.xlsx')

dire = directory()

# Initialize Flask app for Flask-Mail
app = Flask(__name__)
# app.config.update(
#     MAIL_SERVER='172.24.128.80',
#     MAIL_PORT=25,
#     MAIL_USE_TLS=False,
#     MAIL_USE_SSL=False,
#     MAIL_USERNAME='cutting_fb@murata.com'
# )
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS') == 'True',
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL') == 'True',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
)

mail = Mail(app)

def send_email(subject, sender, recipients, body, photo_paths, grid_image_path):
    with app.app_context():
        if not isinstance(recipients, list):
            raise ValueError("recipients must be a list of email addresses")
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        for photo_path in photo_paths:
            if photo_path:
                with open(photo_path, 'rb') as fp:
                    msg.attach(photo_path, 'image/jpeg', fp.read())
        if grid_image_path:
            with open(grid_image_path, 'rb') as fp:
                msg.attach(grid_image_path, 'image/png', fp.read())
        mail.send(msg)

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data
