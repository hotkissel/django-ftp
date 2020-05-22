from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import wget
import ftplib

now = datetime.now()
today_date = now.strftime("%d %B %Y")


def ftp_upload(localfile, remotefile, user, project, cur_date):
    ftp = ftplib.FTP('localhost')
    ftp.login("pk", "testim")
    ftp.encoding = 'utf-8'
    fp = open(localfile, 'rb')
    ls = ftp.nlst()
    if project not in ls:
        ftp.mkd(project)
    ftp.cwd(project)
    ls = ftp.nlst()
    if cur_date not in ls:
        ftp.mkd(cur_date)
    ftp.cwd(cur_date)
    ls = ftp.nlst()
    if user not in ls:
        ftp.mkd(user)
    ftp.cwd(user)
    ftp.storbinary(f'STOR {remotefile}', fp, 1024)
    fp.close()
    ftp.close()


def downloads(request, folder='', subfolder='', subsubfolder=''):
    ftp = ftplib.FTP('localhost')
    ftp.login("pk", "testim")
    ftp.encoding = 'utf-8'
    back_btn = request.META.get('HTTP_REFERER')
    name_dir = str(request)
    print(name_dir)
    folder = name_dir[30:-2]
    print(folder)
    if '/' in folder:
        folder_ls = folder.split('/')
        count = len(folder_ls)
        print(count)
        print(folder_ls)
        counter = 0
        for i in range(count):
            if '%20' in folder_ls[counter]:
                folder_ls[counter] = folder_ls[counter].replace('%20', ' ')
            print(folder_ls[counter])
            ftp.cwd(folder_ls[counter])
            counter += 1
    else:
        ftp.cwd(folder)
    filenames = ftp.mlsd()
    return render(request, 'ftp/downloads.html', {'filenames': filenames, 'folder': folder, 'back_btn': back_btn})


def news(request):
    logs_dir = 'C:\\Program Files (x86)\\FileZilla Server\\Logs\\FileZilla Server.log'
    log = open(logs_dir, "rt")
    return render(request, 'ftp/news.html', {'log': log})


def js(request):
    return render(request, 'ftp/js/date_convert.js', {})


def main_page(request):
    return render(request, 'ftp/main.html', {})


def upload_from_computer(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = "ftp" + fs.url(filename)
        ftp_upload(uploaded_file_url, filename, "pk", "EV", today_date)
        return render(request, 'ftp/upload_from_computer.html', {
            'filename': filename, 'uploaded': uploaded_file_url
        })
    return render(request, 'ftp/upload_from_computer.html')


def upload(request):
    return render(request, 'ftp/upload.html', {})


def upload_from_url(request):
    if request.method == 'POST':
        url = request.POST.get('myurl')
        filename = wget.download(url)
        ftp_upload(filename, filename, "pk", "EV", today_date)
        return render(request, 'ftp/upload_from_url.html', {
            'filename': filename
        })
    return render(request, 'ftp/upload_from_url.html')
