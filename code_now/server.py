import socket
import mimetypes
import smtplib
from email.mime.text import MIMEText
import psycopg2
import random
import json

sessions = {}

def connect_databse(dbname, user, password, host):
    connection = psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
        host = host
        )
    return connection

# Connect to postgres database
conn = connect_databse(dbname = "postgres", user = "postgres", password = "200253", host = "Localhost")
cur = conn.cursor()

# Check if the 'codenow' database exists
cur.execute("""SELECT EXISTS (
            SELECT datname
            FROM pg_database
            WHERE datname = 'codenow')
            """)
database_exists = cur.fetchone()[0]

# If database doesnot exist, create it
if not database_exists:
    cur.execute("CREATE DATABASE codenow")
    conn.commit()

# Connect to 'codenow' database
conn = connect_databse(dbname = "codenow", user = "postgres", password = "200253", host = "Localhost")
cur = conn.cursor()

# Check if the users table exists
cur.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'users_data'
    )
""")
users_exists = cur.fetchone()[0]

# If the table doesn't exist, create it
if not users_exists:
    cur.execute("CREATE TABLE users_data (username varchar PRIMARY KEY, email varchar, password varchar)")
    conn.commit()

# Check if the tutors table exists
cur.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'tutor_data'
    )
""")
tutor_exists = cur.fetchone()[0]

# If the table doesn't exist, create it
if not tutor_exists:
    cur.execute("CREATE TABLE tutor_data (username varchar PRIMARY KEY, email varchar, password varchar)")
    conn.commit()

# Check if the requests table exists
cur.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'requests'
    )
""")
requests_exists = cur.fetchone()[0]

# If the table doesn't exist, create it
if not requests_exists:
    cur.execute("CREATE TABLE requests (program varchar, name varchar, email varchar, phone bigint, gender varchar, education varchar, status varchar, purpose varchar, tutor varchar)")
    conn.commit()

# Check if programs table exists
cur.execute("""
    SELECT EXISTS(
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'programs'
    )
""")
progarms_exists = cur.fetchone()[0]

# If the table doesn't exist, create it
if not progarms_exists:
    cur.execute("CREATE TABLE programs(program varchar PRIMARY KEY, rating DOUBLE, num_ratings varchar, start varchar, duration varchar, price varchar, image varchar, programid int, tutor varchar)")
    conn.commit()

# Check if Enrolled table exists
cur.execute("""
    SELECT EXISTS(
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'enrolled_courses'
    )
""")
enrolled_exists = cur.fetchone()[0]

# If the table doesn't exist, create it
if not enrolled_exists:
    cur.execute("CREATE TABLE enrolled_courses(program varchar, student varchar)")
    conn.commit()

#-------------------------------------------------
#-------------------- SERVER ---------------------
#-------------------------------------------------
def run_server(host='127.0.0.1',port=8928):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server is running on http://{host}:{port}")
        print("Press Ctrl+C to stop the server.")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")

            request = client_socket.recv(2048).decode('utf-8')
            print(f"Request received:\n{request}")

            response = handleRequest(request)
            client_socket.sendall(response)
            client_socket.close()
 
def serverFile(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except:
        return f"HTTP/1.1 404 NOT FOUND\n\n file not found".encode()

def userInput(request):
    body = request.split('\r\n\r\n')[1]
    postData = body
    formData = {}
    for pair in postData.split('&'):
        key, value = pair.split('=')
        formData[key] = value
    return formData

def generate_reference_id():
    return f"#CDN-{''.join(random.choices('0123456789', k=8))}"

def sendEmail(toEmail, details, action):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("jashwanthpodduturi@gmail.com", "unmj wfai dedv btlt")

    if action == 'accept':
        msg = MIMEText(f'''Dear {details.get('name')},\n\nWe are delighted to inform you that your application for enrolling in the {details.get('course')} course has been confirmed!\nTo complete your enrollment, please proceed to make the payment.\nhttps://Localhost:8998/payment\n\nBest regards,\nCODENOW\n+91-123 456 7890''')
        msg['Subject'] = f'Application Confirmation - {details.get('course').capitalize()}'

    elif action == 'reject':
        msg = MIMEText(f'''Dear {details.get('name')},\n\nWe regret to inform you that your application for enrolling in the {details.get('course')} course has been rejected.\nThank you for your understanding.\n\nBest regards,\nCODENOW\n+91-123 456 7890''')
        msg['Subject'] = f'Application Rejected - {details.get('course').capitalize()}'

    else:
        msg = MIMEText(f'''Dear {details.get("name").replace('+', ' ')},\n\nThank you for your application to enroll in the {action} course with us.\nThis is to confirm that we have received your application, and it is currently being processed.\nYour unique reference ID for this application is: {generate_reference_id()}.\n\nBest regards,\nCODENOW\n+91-123 456 7890''')
        msg['Subject'] = 'codenow | Application Acknowledgement'
        
    msg['From'] = 'jashwanthpodduturi@gmail.com'
    msg['To'] = toEmail

    try:
        server.sendmail('jashwanthpodduturi@gmail.com', toEmail, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()


def handleRequest(request):
    global conn

    parseRequest = request.split('\n')[0].split()
    method = parseRequest[0]
    uri = parseRequest[1]

    cookie = request.split('\n')
    for line in cookie:
        if 'Cookie:' in line:
            a = line.split(':')[1].strip()
            session = a.split('=')[1]

    if uri == '/favicon.ico':
        return ''.encode()

    if method == 'GET':
        if uri == '/home':             
            if True in sessions.values():
                response = f'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n'.encode() + serverFile('codenow.html')
            else:
                response = f'HTTP/1.1 302 FOUND\r\nLocation: /login\r\n\r\n'.encode()

        elif uri == '/tutor-home':             
            if True in sessions.values():
                response = f'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n'.encode() + serverFile('tutor.html')
            else:
                response = f'HTTP/1.1 302 FOUND\r\nLocation: /login\r\n\r\n'.encode()
        
        elif uri == '/signup':
            response = f'HTTP/1.1 200 OK\r\nContent-Type:{mimetypes}\r\n\r\n'.encode() + serverFile('register.html')

        elif uri == '/login' or uri == '/':
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('s_login.html')

        elif uri == '/logintutor':
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('t_login.html')

        elif uri == '/programs':
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('programs.html')

        elif uri == '/myprograms':
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('myprograms.html')

        elif uri == '/requests':
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('requests.html')

        elif uri == '/payment':
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('payments.html')

        elif uri == '/logout':
            if True in sessions.values():
                for key, value in sessions.items():
                    sessions[key] = False
                # del sessions[cookies['session_id']]
            response = f"HTTP/1.1 302 FOUND\nLocation: /login\nSet-Cookie: session_id=; Max-Age=0\r\n\r\n".encode()

        elif uri == '/Logout':
            if True in sessions.values():
                for key, value in sessions.items():
                    sessions[key] = False
                # del sessions[cookies['session_id']]
            response = f"HTTP/1.1 302 FOUND\nLocation: /logintutor\nSet-Cookie: session_id=; Max-Age=0\r\n\r\n".encode()


        elif uri == '/api/programs':
            # conn = None  # Initialize conn outside the try block
            try:
                # Connect to PostgreSQL database
                cur = conn.cursor()

                # Execute SQL query to fetch programs
                cur.execute("SELECT * FROM programs")
                programs = cur.fetchall()

                # Send JSON response
                response = ('HTTP/1.1 200 OK\nContent-Type: application/json\n\n' + json.dumps(programs)).encode()

            except psycopg2.Error as e:
                print("Error fetching request:", e)
                error_response = {'error': 'Failed to fetch programs'}
                response = ('HTTP/1.1 500 Internal Server Error\n\n' + json.dumps(error_response)).encode()

            finally:
                if conn:
                    cur.close()

        elif uri == '/api/requests':
            try:
                # Connect to PostgreSQL database
                cur = conn.cursor()

                # Execute SQL query to fetch requests
                cur.execute(f"SELECT * FROM requests WHERE tutor = '{session}'")
                requests = cur.fetchall()

                # Send JSON response
                response = ('HTTP/1.1 200 OK\nContent-Type: application/json\n\n' + json.dumps(requests)).encode()

            except psycopg2.Error as e:
                print("Error fetching requests:", e)
                error_response = {'error': 'Failed to fetch requests'}
                response = ('HTTP/1.1 500 Internal Server Error\n\n' + json.dumps(error_response)).encode()
            finally:
                if conn:
                    cur.close()

        elif uri == '/api/myprograms':
            try:
                cur = conn.cursor()
                cur.execute(f"""SELECT p.image, p.program, e.status, p.price
                                FROM programs p
                                JOIN enrolled_courses e ON p.program = e.program
                                WHERE e.student = '{session}';""")
                myprograms = cur.fetchall()
                response =  ('HTTP/1.1 200 OK\nContent-Type: application/json\n\n' + json.dumps(myprograms)).encode()
            except psycopg2.Error as e:
                print("Error fetching requests:", e)
                error_response = {'error': 'Failed to fetch my programs'}
                response = ('HTTP/1.1 500 Internal Server Error\n\n' + json.dumps(error_response)).encode()
            finally:
                if conn:
                    cur.close()

        # elif uri == '/payment-info':
            
                    
        elif '/registration?programId=' in uri:
            response = f"HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n".encode() + serverFile('apply.html') + f"<script>document.getElementById('title').innerHTML = '{uri[24:].replace("%20", " ")}';</script>".encode()

        elif uri.endswith('.css'):
            response = (f'HTTP/1.1 200 OK\nContent-Type: text/css\n\n').encode() + serverFile(uri[1:].strip())

        elif uri.endswith('.js'): #/scrit.js
            response = (f'HTTP/1.1 200 OK\nContent-Type: text/css\n\n').encode() + serverFile(uri[1:].strip())

        elif uri.endswith('.png'):
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile(uri[1:].strip())

        elif uri.endswith('.jpg'):
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile(uri[1:].strip())

        elif uri.endswith('.woff'):
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile(uri[1:].strip())

        elif uri.endswith('.woff2?v=4.7.0'):
            response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('assets/fonts/fontawesome-webfont.woff')

        else:
            response = ('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
            '<html><head><style>body { display: flex; justify-content: center; align-items: center; height: 100vh; }</style></head>'
            '<body><img src="assets/images/404.png"></body></html>').encode()

    elif method == 'POST':
        if uri == '/tutor/register':
            formData = userInput(request)
            print(formData)
            username = formData.get('tutor_username')
            email = formData.get('tutor_email').replace('%40', '@')
            password = formData.get('tutor_password')
            
            # Connect to PostgreSQL database
            cur = conn.cursor()
            cur.execute(f"INSERT into tutor_data values('{username}', '{email}', '{password}');")
            conn.commit()            
            cur.close()

            response = (f'HTTP/1.1 302 FOUND\r\nLocation: /logintutor\r\n\r\n').encode()

        elif uri == '/student/register':
            formData = userInput(request)
            print(formData)
            username = formData.get('student_username')
            email = formData.get('student_email').replace('%40', '@')
            password = formData.get('student_password')
            
            # Connect to PostgreSQL database
            cur = conn.cursor()
            cur.execute(f"INSERT into users_data values('{username}', '{email}', '{password}');")
            conn.commit()            
            cur.close()

            response = (f'HTTP/1.1 302 FOUND\r\nLocation: /login\r\n\r\n').encode()

        elif uri == '/student-login':
            formData = userInput(request)
            print(formData)
            username = formData.get('student_username')
            password = formData.get('student_password')
            print(username, password)

            cur = conn.cursor()
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM users_data WHERE username = '{username}' AND password = '{password}') AS password_exists;")
            password_exists = cur.fetchone()[0]
            print(password_exists)
            cur.close()

            if password_exists:
                session_id = username
                sessions[session_id] = True
                print('sessions:\n',sessions)
                response = f'HTTP/1.1 302 FOUND\nLocation: /home\nSet-Cookie: session_id={session_id}\n\n'.encode()
            else:
                response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('s_login.html') + '<script>document.getElementById("invalid").innerHTML = "<p>Invalid username or password</p>";</script>'.encode()
        
        elif uri == '/tutor-login':
            formData = userInput(request)
            username = formData.get('tutor_username')
            password = formData.get('tutor_password')

            cur = conn.cursor()
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM tutor_data WHERE username = '{username}' AND password = '{password}') AS password_exists;")
            password_exists = cur.fetchone()[0]
            print(password_exists)
            cur.close()

            if password_exists:
                session_id = username
                sessions[session_id] = True
                response = f'HTTP/1.1 302 FOUND\nLocation: /tutor-home\nSet-Cookie: session_id={session_id}\n\n'.encode()
            else:
                response = (f'HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n').encode() + serverFile('t_login.html') + '<script>document.getElementById("invalid").innerHTML = "<p>Invalid username or password</p>";</script>'.encode()

        elif '/apply?programId=' in uri:
            program = uri[17:].replace('%20', ' ')
            formData = userInput(request)
            print(formData)

            # print(formData)
            # username = formData.get('name').replace('+', ' ')
            email = formData.get('email').replace('%40', '@')
            phone = formData.get('Phone')
            gender = formData.get('gender')
            education = formData.get('education')
            status = formData.get('status')
            purpose = formData.get('purpose').replace('+', ' ')

            cur = conn.cursor()
            cur.execute(f"SELECT tutor FROM programs WHERE program = '{program}'")
            tutor = cur.fetchone()[0]
            cur.execute(f"INSERT into requests values('{program}','{session}', '{email}', '{phone}','{gender}', '{education}', '{status}', '{purpose}', '{tutor}');")
            conn.commit()
            cur.close()

            try:
                # sendEmail(email, formData, program)
                response = f"HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n".encode() + serverFile('apply.html') + '<script src="after-apply.js"></script>'.encode() + f"<script>document.getElementById('title').innerHTML = '{program.replace("%20", " ")}';</script>".encode()
            except Exception as e:
                response = ('HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n<html><body><img width="800px" height="400px" src="assets/images/500.png" style="display: block; margin-left: auto; margin-right: auto;"></body></html>').encode()
        
        elif uri == '/send-email':
            body = request.split('\r\n\r\n')[1]
            formData = json.loads(body)
            email = formData.get('email')
            action = formData.get('action')
            # sendEmail(email, formData, action)

            cur = conn.cursor()
            cur.execute(f"DELETE FROM requests WHERE email = '{email}' AND program = '{formData.get('course')}'")
            conn.commit()            
            cur.close()

            response = f"HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n".encode()

        elif uri == '/enrolled':
            body = request.split('\r\n\r\n')[1]
            formData = json.loads(body)
            course = formData.get('course')
            student = formData.get('student')
            print(session)

            cur = conn.cursor()
            cur.execute(f"INSERT into enrolled_courses values('{course}', '{student}', 'pending')")
            conn.commit()            
            cur.close()

            response = f"HTTP/1.1 200 OK\nContent-Type: {mimetypes}\n\n".encode()
        
        else:
            response = ('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><img width="800px" height="400px" src="assets/images/404.png" style="display: block; margin-left: auto; margin-right: auto;"></body></html>').encode()


    return response

if __name__ == "__main__":
    run_server()
