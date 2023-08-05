# CloudeosApi

Cloudeos.com için python api kullanımı örnegidir, api dökümanlarından bakarak bu örneği genişletebilirsiniz.

### Mevcut istek örnekleri:
- Get Account Detail
- Get Current Balance
- Create Server
- Get Server Lists
- Destroy Server
- Create SSH Key
- Get SSH Keys
- Destroy SSH Keys
- Get Regions
- Get Packages



### Example

#### Get Account Detail:
```
from cloudeos import API


cloudeos = API("username", "password")

account_detail = cloudeos.get_accountDetail()

print(account_detail)
```


#### Create Server:
```
from cloudeos import API


cloudeos = API("username", "password")

name	 = "MyServer"
region	 = "ist2"
package  = "1c-1r-25d"
image	 = "ubuntu-16-04-x64"
ssh_keys = "MySSHKey fingerprint degeri" #key olusturulmussa veya istege bagli

create   = cloudeos.create_server(name, region, package, image, ssh_keys=ssh_keys)

print(create)
```


Diğer örnekleri Examples klasöründe bulabilir ve genişletebilirsiniz.
