#!/usr/bin/env python3
import requests
import getpass
import sys
import os

BASE_URL = 'https://www.gradescope.com'

class APIClient:
    def __init__(self):
        self.session = requests.Session()

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def log_in(self, email, password):
        url = "{base}/api/v1/user_session".format(base=BASE_URL)

        form_data = {
            "email": email,
            "password": password
        }
        r = self.post(url, data=form_data)

        self.token = r.json()['token']

    def upload_pdf_submission(self, course_id, assignment_id, student_email, filename):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def replace_pdf_submission(self, course_id, assignment_id, student_email, filename):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions/replace_pdf".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def upload_programming_submission(self, course_id, assignment_id, student_email, filenames):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = [('files[]', (filename, open(filename, 'rb'))) for filename in filenames]

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

if __name__ == '__main__':
    # Use the APIClient to upload submissions after logging in, e.g:
    # client.upload_pdf_submission(1234, 5678, 'student@example.edu', 'submission.pdf')
    # client.upload_programming_submission(1234, 5678, 'student@example.edu', ['README.md', 'src/calculator.py'])
    # this code must be called from within the submissions folder

    email = input('Gradescope Email: ')
    password = getpass.getpass('Gradescope Password: ')

    print()
    print('You can get course and assignment IDs from the URL, e.g.')
    print('https://www.gradescope.com/courses/1234/assignments/5678')
    print('course_id = 1234, assignment_id = 5678')
    print()

    course_id = input('Gradescope Course ID: ')
    assignment_id = input('Gradescope Assignment ID: ')
    merge = True

    client = APIClient()
    client.log_in(email, password)
    print('login successful')

    if merge:
        for file in os.listdir('.'):
            email = file[0:10].lower() + '@domain.com'
            client.upload_programming_submission(course_id, assignment_id, email, [file])
            print('uploaded ', file)
    else:
        for studentid in os.listdir(folder):
            email = studentid.lower()+'@domain.com'
            files = []
            for file in os.listdir('.'):
                filename = studentid + '/' + file
                files.append(filename)
            client.upload_programming_submission(course_id, assignment_id, email, files)
            print('uploaded ', studentid)
