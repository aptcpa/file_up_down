# coding utf-8
from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse

def index(request):
	if request.session.get('login_id'):
		user=request.session.get('login_id')
		loged_in=True
	else:
		user=''
		loged_in=False
	return render(request,'index.html',{'user':user,'loged_in':loged_in})

def login(request):
	if request.session.get('login_id'):
		return redirect('/')
	if request.method == 'POST':
		if request.session.get('login_id'):
			return redirect(request.META.get('HTTP_REFERER','/'))
		from app.models import Users
		user = request.POST.get('user')
		password = request.POST.get('password')
		if Users.objects.filter(user=user,password=password):
			request.session['login_id']=user
			return redirect(request.session['login_from'])
		else:
			return HttpResponse('账号或密码错误!')
	else:
		request.session['login_from']=request.META.get('HTTP_REFERER','/')
		return render(request,'login.html')

def logout(request):
	request.session.flush()
	return redirect(request.META.get('HTTP_REFERER','/'))


def receive(request):
	if request.session.get('login_id'):
		user=request.session.get('login_id')
	else:
		return HttpResponse('上传文件请先登录!')
	if request.method == 'POST':# 获取对象
		if request.POST.get('passwd') != password:
			return HttpResponse('密码不正确,取消上传!')
		obj = request.FILES.get('file')
		import os
		# 上传文件的文件名
		output_name =os.path.join(os.getcwd(),'upload',obj.name)
		if not os.path.exists(os.path.dirname(output_name)):
			os.makedirs(os.path.dirname(output_name))
		f = open(output_name,'wb')
		for chunk in obj.chunks():
			f.write(chunk)
		f.close()
		return  HttpResponse('上传成功.<br><br>' + output_name)
	return render(request, 'upload.html',{'user':user})

provide_path ='/root/file_up_down'
def send(request):
	import os
	org_path=os.path.abspath(request.path)
	path_prev = os.path.abspath(os.path.join(org_path,'..'))
	path = org_path.replace('/download','')
	if path =='':
		path='/'

	if request.session.get('login_id'):
		user=request.session.get('login_id')
		loged_in=True
	else:
		user=''
		loged_in=False
	if os.path.isfile(provide_path+path):
		if not loged_in:
			return HttpResponse('下载文件请先登录!')
		from django.http import FileResponse
		file=open(provide_path+path,'rb')
		response=FileResponse(file)
		response['Content-Type']='application/octet-stream'
		response['Content-Disposition']='attachment;filename="{}"'.format(os.path.basename(path))
		return response
	else:
		if os.path.exists(provide_path+path):
			import datetime
			for dir,sub_dir,file_name in os.walk(provide_path+path):
				dirs_name =sorted(sub_dir)
				files_name=sorted(file_name)
				break
			len_name=50
			len_modify=19
			len_size=20
			dirs =[]
			for a in dirs_name:
				d1 =len_name - len(a)
				if d1 <=0:
					d1 =1
				d2 = datetime.datetime.utcfromtimestamp(os.path.getmtime(provide_path+path+'/'+a)).strftime('%Y-%m-%d %H:%M:%S')
				xxx =' '*d1 + d2 + ' '*(len_size-1) + '-'
				templist=[a,xxx]
				dirs.append(templist)

			files =[]
			for b in files_name:
				f1 = len_name - len(b)
				if f1 <= 0:
					f1 =1
				f2 = datetime.datetime.utcfromtimestamp(os.path.getmtime(provide_path+path+'/'+b)).strftime('%Y-%m-%d %H:%M:%S')
				f3 = os.path.getsize(provide_path+path+'/'+b)
				f3_len = len_size - len(str(f3))
				if f3_len <= 0:
					f3_len = 1
				yyy =' '*f1 + f2 + ' '*f3_len + str(f3)
				templist=[b,yyy]
				files.append(templist)
				


			context={'org_path':org_path,'path':path,
					'path_prev':path_prev,'dirs':dirs,
					'files':files,'user':user,'loged_in':loged_in
					}
			return render(request,'download.html',context)
		else:
			return HttpResponse('page not found '+provide_path+path)