import static
import os
import shutil
import datetime
import docx
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.core.files import File

from django.contrib.staticfiles.finders import find
from django.http import HttpResponse

from djangoProject import settings
from django.http import FileResponse


def index(request):
    return render(request, 'index.html')


def letter(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'letter.html')


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
            received = "an email"
            dev = "email address"
        else:
            type_address = userphone
            received = "a message"
            dev = "phone"

        if request.POST['unsubscribed_button'] == 'false':
            could_you_unsubscribe = "אם לא די בכך, הרי שהמסרון ממילא לא עומד בדרישות החוק הצורניות בכך שאין בו אפשרות הסרה כדין."
        else:
            could_you_unsubscribe = " "

            # Get the number of messages

        num_messages = int(request.POST['num_messages'])
        date_of_message = []
        time_of_message = []
        dates_and_times = []
        if num_messages == 1:
            date_of_message = request.POST['message_0_date']
            time_of_message = request.POST['message_0_time']
            print(date_of_message)
        else:
            date_of_message = [''] * num_messages
            time_of_message = [''] * num_messages
            for i in range(num_messages):
                date_of_message[i] = request.POST['message_{}_date'.format(i)]
                time_of_message[i] = request.POST['message_{}_time'.format(i)]
                dates_and_times.append((date_of_message[i], time_of_message[i]))
            date_of_message = []
            time_of_message = []
            for date, time in dates_and_times:
                date_of_message += f"ביום {date} "
                time_of_message += f"בשעה {time} "
            print(dates_and_times)  # Output:

        keywords = {
            "da1te": date_string,
            "UserName": username,
            "UserEmail": useremail,
            "UserPhone": userphone,
            "dev": dev,
            "1515": type_address,
            "received": received,
            "date_of_message": date_of_message,
            "time_of_message": time_of_message,
            "could_you_unsubscrive": could_you_unsubscribe,
            "company_name": company_name,
            "Company_address": company_address,
            "company_id": company_id,

        }

        # Filename of the template
        document = docx.Document()
        # document.save('static/docx/temp.docx')
        template_filename = 'static/docx/template.docx'
        # temp_filename = 'static/docx/temp.docx'
        #
        # # Copy the template file to a new temp file
        # shutil.copy(template_filename, temp_filename)

        # Open the temp file
        document = docx.Document(template_filename)

        # Replace keywords in the contents
        for paragraph in document.paragraphs:
            for run in paragraph.runs:
                for key, value in keywords.items():
                    run.text = run.text.replace(key, value)
        download_success = True
        document.save('static/docx/modified_document.docx')
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
        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
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
