import io
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from HttpRunnerManager.settings import EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD


def send_email_reports(receiver, html_report_path):
    if '@sina.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.sina.com'
    elif '@163.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.163.com'
    else:
        smtp_server = 'smtp.mxhichina.com'
    subject = "接口自动化测试报告"
    with io.open(html_report_path, 'r', encoding='utf-8') as stream:
        send_file = stream.read()
    att = MIMEText(send_file, "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = "attachment;filename = TestReports.html"
    dirs = r"D:\project\HttpRunnerManager-master\reports"
    file_lists = os.listdir(dirs)
    file_lists.sort(key=lambda fn: os.path.getmtime(dirs + "\\" + fn)
    if not os.path.isdir(dirs + "\\" + fn)
    else 0)
    file = os.path.join(dirs, file_lists[-1])
    with open(file, 'r', encoding='utf-8') as f:
        bs = BeautifulSoup(f.read(), "html.parser")
    totality = int(bs.find('span', class_="strong").string)
    failure = int(bs.find_all("span", class_="strong")[1].text)
    success = totality - failure
    data = bs.find('span', class_="label suite-start-time blue darken-3").text
    times = bs.find_all("div", class_="panel-lead")[5].text
    body = MIMEText("""
        <h4 style="color: dodgerblue">定时任务邮件发送，详情请下载附件查看</h4><br><hr>
        执行时间:<li style="color: #FF8888">{}</li>
        用例总耗时:<li style="color: #FF8888">{}</li>
        用例执行总数量:<li style="color: #FF8888">{}</li>
        成功用例数量:<li style="color: #00FF00">{}</li>
        失败用例数量:<li style="color: #FF0000 ">{}</li>
        """.format(data, times, totality, success, failure), _subtype='html', _charset='utf-8')
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['from'] = EMAIL_SEND_USERNAME
    msg['to'] = receiver
    msg.attach(att)
    msg.attach(body)
    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.starttls()
    smtp.login(EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD)
    smtp.sendmail(EMAIL_SEND_USERNAME, receiver.split(','), msg.as_string())
    smtp.quit()
    smtp.close()


if __name__ == '__main__':
    send_email_reports('bomingzheng@126.com, smtp.mxhichina.com',
                       r'D:\project\HttpRunnerManager-master\reports\1633759502.html')
