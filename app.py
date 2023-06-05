from flask import Flask, request, jsonify,render_template,redirect,session,url_for,send_file, make_response,render_template_string
from io import BytesIO
import gspread
import requests
import datetime
import pytz
import base64
import random
from PIL import Image, ImageDraw, ImageFont
import os
app = Flask(__name__)
app.secret_key=os.urandom(24)

adminusername="<Your Admin Panel Username Here>"
adminpassword="<Your Admin Panel Password Here>"
imgurclientid= "<Your Imgur Client Here>"
#Change request url with your provider's url on confirm() for sending confirmation sms


# Configuration for Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
file={
"""Create a service account and download the JSON key file from the Google Cloud Console. Make sure you have the necessary permissions for the Google Sheets API then place the JSON key file here"""
}


gc=gspread.service_account_from_dict(file)
# Google Sheet configuration
sh=gc.open_by_key("<yout sheet id>")
worksheet=sh.sheet1


@app.route('/form', methods=['GET', 'POST'])
def form():
  if request.method == 'POST':
    name = request.form.get('name')
    roll = request.form.get('roll')
    email = request.form.get('email')
    phone = request.form.get('phone')
    paid_amount = request.form.get('paid_amount')
    payment_method = request.form.get('payment_method')
    transaction_number = request.form.get('transaction_number')

    image = request.files['image']
    url = 'https://api.imgur.com/3/image'

    # Set headers with authorization
    headers = {'Authorization': 'Client-ID {}'.format(imgurclientid)}

    # Set the payload with the image file
    payload = {'image': (image.filename, image.stream, image.mimetype)}

    # Make the POST request to upload the image
    response = requests.post(url, headers=headers, files=payload)

    # Get the JSON response
    imgur_data = response.json()

    if response.status_code == 200:
      # The image was uploaded successfully

      image_url = imgur_data["data"]["link"]

    else:
      # The image was not uploaded successfully
      image_url = "https://ui-avatars.com/api/?name={}&size=512".format(
        name.replace(" ", "+"))

    dhaka_timezone = pytz.timezone('Asia/Dhaka')
    current_datetime = datetime.datetime.now(dhaka_timezone)
    formatted_datetime = current_datetime.strftime("%d/%m/%y || %H:%M")

    lis = worksheet.get_all_values()

    # Get the last value from the B column
    luid = lis[-1][1]
    digit = luid.replace("NDCG2RDWTV0", "")

    try:

      uid = "NDCG2RDWTV0" + str(int(digit) + 1)
    except Exception as e:

      uid = "NDCG2RDWTV0{}".format(random.randint(100, 999))

    # Save the data to Google Sheet
    save_to_sheet([
      formatted_datetime, uid, name, roll, paid_amount, payment_method,
      transaction_number, image_url, email, phone
    ])

    return render_template('sucess.html', uid=uid)
  return render_template('form.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
  if 'isadmin' in session:
    if session['isadmin']:
      lis = worksheet.get_all_values()
      lis.remove(lis[0])
      nlis=[]
      clis=[]
      totalcash=0
      totalbkash=0
      totalnagad=0
      totalrocket=0
      for i in lis:
        if i[10]!="confirm":
          if i[10]=="denied":
            pass
          else:
            nlis.append(i)
        
        elif i[10]=="confirm":
          if i[5]=="cash":
            totalcash+=int(i[4])
          elif i[5]=="bkash":
            totalbkash+=int(i[4])
          elif i[5]=="nagad":
            totalnagad+=int(i[4])
          elif i[5]=="rocket":
            totalrocket+=int(i[4])
          clis.append(i)
        

      totaltk=0
      for i in clis:
        totaltk+=int(i[4])
      return render_template('admin.html',lis=nlis,total=len(clis),totaltk=totaltk,totalcash=totalcash,totalbkash=totalbkash,totalnagad=totalnagad,totalrocket=totalrocket)
     
    else:
      return redirect(url_for('.login'))
  else:
    return redirect(url_for('.login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method=="POST":
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username==adminusername and password==adminpassword:
      session['isadmin']=True
      return redirect(url_for('.admin'))
    else:
      return "Invalid Credentials"
    
  else:
    return render_template('login.html')
@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('.login'))

@app.route('/confirm')
def confirm():
  if "isadmin" in session:
    name = request.args.get('id')
    first_column = worksheet.range("B1:B{}".format(worksheet.row_count))
    found_cell_list = [found for found in first_column if found.value == name]
    x=int(found_cell_list[0].row)
    worksheet.update('K{}'.format(x), 'confirm')

    name=str(worksheet.cell(x, 3).value)
    number=str(worksheet.cell(x, 10).value)
    ud=str(worksheet.cell(x, 2).value)
    message="""Dear {}!Your payment for Rag Day event of NDC Group 2 has been verified. Download your ticket from https://g2farewell.me/ticket?id={} """.format(name,ud)
    x=requests.get("http://bulksmsbd.net/api/smsapi?api_key=<Your Message Provider's API Key here>&type=text&number={}&senderid=8809617611744&message={}".format(number,message))
    #You can use different sms provider. Just change the request url with your provider's request url
    return redirect(url_for('.admin'))
  else:
    return render_template(".login")

@app.route('/deny')
def deny():
  if "isadmin" in session:
    name = request.args.get('id')
    first_column = worksheet.range("B1:B{}".format(worksheet.row_count))
    found_cell_list = [found for found in first_column if found.value == name]
    x=int(found_cell_list[0].row)
    worksheet.update('K{}'.format(x), 'denied')
    return redirect(url_for('.admin'))
  else:
    return render_template(".login")

  
    
def save_to_sheet(data):
    worksheet.append_row(data)



@app.route('/ticket')
def generate_ticket():
    date="Date: 15 June , 2023"
    time="At 3:00 PM"


    name = request.args.get('id')
    first_column = worksheet.range("B1:B{}".format(worksheet.row_count))
    found_cell_list = [found for found in first_column if found.value == name]
    lis=worksheet.get_all_values()
    arr=lis[int(found_cell_list[0].row)-1]
    print(arr)
    if arr[10]=="confirm":
      # Open the template image
      template_path = 'static/images/template.png'
      template = Image.open(template_path)

      # Create a drawing object
      draw = ImageDraw.Draw(template)

      # Define the text and font properties
      name = 'Name: {}'.format(arr[2])
      roll= 'Roll: {}'.format(arr[3])
      phone='Phone: {}'.format(arr[9])
      font_path = 'static/fonts/Anton.ttf'
      font_size = 32
      font = ImageFont.truetype(font_path, font_size)
      text_color = (255, 255, 255)  # White

      

      # Write the text on the template. You can change co ordinates respect to your template
      draw.text((55, 325), name, fill=text_color, font=font)
      draw.text((55, 375), roll, fill=text_color, font=font)
      draw.text((55, 425), phone, fill=text_color, font=font)

      font = ImageFont.truetype(font_path,42)
      draw.text((100, 530), date, fill=(255,255,255), font=font)
      font = ImageFont.truetype(font_path,36)
      draw.text((185, 580), time, fill=(255,255,255), font=font)


      font = ImageFont.truetype(font_path,56)
      draw.text((1620, 70), "Address", fill=(0,0,0), font=font)

      font = ImageFont.truetype(font_path,32)
      draw.text((1460, 160), "Big Apple Restaurant And Party Center", fill=(0,0,0), font=font)

      font = ImageFont.truetype(font_path,26)
      draw.text((1490, 220), "373/B, Shahid Baki Road, Khilgaon-Taltola, Dhaka", fill=(0,0,0), font=font)




  
      font = ImageFont.truetype(font_path,52)
      draw.text((1530, 480), "#{}".format(arr[1]), fill=(0, 0, 0), font=font)
      # Create an in-memory file-like object
      image_buffer = BytesIO()

      # Save the modified image to the buffer as PNG
      template.save(image_buffer, 'PNG')
      image_buffer.seek(0)

      # Convert the image buffer to base64
      image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')

      # Render the HTML template with the base64 image data
      

      return render_template('ticket.html', image_data=image_base64)
    else:
      return "<center><h2>Payment isn't verified yet</h2></center>"




if __name__ == '__main__':
    app.run()
