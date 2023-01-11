import os
from io import BytesIO

from django.contrib import messages
from django.http import HttpResponseRedirect

import datetime
import docx
from django.shortcuts import render, redirect

from PIL import Image
from docx import Document

from djangoProject import settings


def index(request):
    return render(request, 'index.html')


def letter(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'letter.html')


def upload_photo(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        if photo:
            # check that it's a valid image file
            if not photo.content_type.startswith('image'):
                messages.success(request, 'Thats Not a Photo!')
            else:
                # store the file in your static folder
                with open('media/upload_folder/' + 'tempphoto.png', 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)
                messages.success(request, 'File uploaded !')

        else:
            messages.success(request, 'No file was selected')
    return render(request, 'letter.html')


def replace_pic(filepath, photo):
    document = Document(filepath)
    for paragraph in document.paragraphs:
        if 'pic' in paragraph.text:
            # insert the photo
            # Save the PIL Image object to a BytesIO object
            with Image.open(photo) as img:
                buffer = BytesIO(photo)
                img.save(buffer, 'PNG')
            # Add the image to the document
            document.add_picture(buffer, width=photo.width, height=photo.height)
            buffer.seek(0)
            # Replace 'pic' with image
            paragraph.text = paragraph.text.replace('pic', '')
    document.save('static/docx/modified_document1.docx')


def letter(request):
    if request.method == 'POST':
        today = datetime.date.today()
        date_string = today.strftime("%d/%m/%Y")
        username = request.POST['full_name']
        useremail = request.POST['email']
        userphone = request.POST['phone_number']
        company_name = request.POST['company_name']
        company_address = request.POST['company_address']
        company_id = request.POST['company_id']

        if request.POST['spam_type'] == 'email':
            type_address = useremail
            received = "מייל"
            dev = "כתובת מייל"
        else:
            type_address = userphone
            received = "מסרון"
            dev = "טלפון"

        if request.POST['unsubscribed_button'] == 'false':
            could_you_unsubscribe = "אם לא די בכך, הרי שהמסרון ממילא לא עומד בדרישות החוק הצורניות בכך שאין בו אפשרות הסרה כדין."
        else:
            could_you_unsubscribe = " "

            # Get the number of messages

        num_messages = int(request.POST['num_messages'])
        dates_and_times = []
        date_of_message = [''] * num_messages
        time_of_message = [''] * num_messages
        for i in range(num_messages):
            date_of_message[i] = request.POST['message_{}_date'.format(i)]
            time_of_message[i] = request.POST['message_{}_time'.format(i)]
            dates_and_times.append((date_of_message[i], time_of_message[i]))
        date_of_message = ""
        time_of_message = ""
        messages = ""
        for date, time in dates_and_times[:1:1]:
            messages += f"ביום {date}  בשעה {time}\n"
        for date, time in dates_and_times[1::1]:
            messages += f"ביום {date}  בשעה {time}             \n"

        print(dates_and_times)  # Output:

        keywords = {
            "da1te": date_string,
            "UserName": username,
            "UserEmail": useremail,
            "UserPhone": userphone,
            "dev": dev,
            "1515": type_address,
            "received": received,
            "date_of_message": messages,
            "could_you_unsubscrive": could_you_unsubscribe,
            "company_name": company_name,
            "Company_address": company_address,
            "company_id": company_id,

        }

        # Filename of the template
        document = docx.Document()
        template_filename = 'static/docx/template.docx'

        # Open the temp file
        document = docx.Document(template_filename)

        # Replace keywords in the contents
        for paragraph in document.paragraphs:
            for run in paragraph.runs:
                for key, value in keywords.items():
                    run.text = run.text.replace(key, value)

        for paragraph in document.paragraphs:
            # Iterate over the runs in the paragraph
            for run in paragraph.runs:
                # Set the font to Arial
                run.font.name = "Arial"
        document.save('static/docx/modified_document.docx')
        filepath = 'static/docx/modified_document.docx'
        photo = os.path.join(settings.MEDIA_ROOT, 'upload_folder', 'tempphoto.png')
        img = Image.open(photo)

        replace_pic(filepath, photo)



        download_success = True
        # document.save('static/docx/modified_document.docx')
        return render(request, 'form.html', {'download_success': download_success})
        print("Finished replacing keywords in temp file.")
    else:
        # Set the download_success flag to False
        download_success = False

        # Save the modified Word document
    return render(request, 'letter.html')


def home(request):
    return render(request, 'home.html')


def form(request):
    # Set the download_success flag to True
    download_success = True

    # Render the form template
    return render(request, 'form.html', {'download_success': download_success})


from django.http import HttpResponse


def download_file(request):
    if request.method == 'POST':
        # Process form submission

        # File path
        file_path = 'static/docx/modified_document.docx'

        # Open the file in binary mode
        with open(file_path, 'rb') as f:
            # Read the file content
            file_content = f.read()

        # Create the HttpResponse object with the file content
        response = HttpResponse(file_content,
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        # Set the Content-Disposition header to attachment
        response['Content-Disposition'] = 'attachment; filename="modified_document.docx"'

        # Set the download_success flag to True
        download_success = True

        # Return the HttpResponse object
        return response
    else:
        # Set the download_success flag to False
        download_success = False

    # Render the form template
    return render(request, 'form.html', {'download_success': download_success})
