import requests
import json
import mysql.connector
from mysql.connector import Error

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class challenge:
    def __init__(self) -> None:
        self.URL = 'https://jsonplaceholder.typicode.com/posts/'

    def fetcher(self):
        # Fetching data
        try:
            # Send GET request to the API
            response = requests.get(self.URL)

            if response.status_code == 200:
                self.data = json.loads(response.text)
            else:
                print('API Error:', response.status_code)

        except requests.exceptions.RequestException as e:
            # Handle the request exception
            print('Request Exception:', str(e))     
    
    def data_processing(self):
        # Data processing
        # Number of posts by each user 
        self.counts = {}
        for post in self.data:
            user_id = post['userId']
            if user_id in self.counts.keys():
                self.counts[user_id] += 1
            else:
                self.counts[user_id] = 1

        print(self.counts)

    def storing(self):
        try:
            # Establish a connection to the MySQL server
            connection = mysql.connector.connect(
                host='db4free.net',
                database='post_db',
                user='tempintern',
                password='Tempintern@36'
            )

            if connection.is_connected():
                # Execute your MySQL queries
                cursor = connection.cursor()

                try:
                    for i in self.data:
                        cursor.execute(f'insert into posts values({i["userId"]},{i["id"]},"{i["title"]}","{i["body"]}")')
                        connection.commit()
                except Error as e:
                    print(e)

                try:
                    for i in self.counts:
                        cursor.execute(f'insert into count values({i},{self.counts[i]})')
                        connection.commit()
                except Error as e:
                    print(e)
                
                # self.mailing()
                # cursor.execute(f'select * from posts')
                # rows = cursor.fetchall()

                # Process the fetched data
                # for row in rows:
                #     print(row)

        except Error as e:
            print("Error connecting to MySQL:", e)

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed.")


    def mailing(self):
        sender_email = 'tempintern36@gmail.com'
        receiver_email = 'tempintern36@gmail.com'
        subject = 'DataBase connected and Data Stored'
        message = 'This mail is to inform that the database was connected successfully and data is stored on the database.'

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, 'plain'))

        # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'tempintern36@gmail.com'
        smtp_password = 'Tempintern@36'

        try:
            # Create a secure connection to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print('Email sent successfully.')

        except smtplib.SMTPException as e:
            print('Error sending email:', str(e))

        finally:
            # Close the SMTP connection
            server.quit()


c = challenge()
c.fetcher()
c.data_processing()
c.storing()