##Password-Manager


### Introduction

A lightweight tool for password management, including insert, update and delete operations. It support randomly generating  passwords when you take insert or update operation. Also, it provides the function of viewing the historical modifications.

### Dependence

* Git
* Sqlite3 


### Installation

```
git clone https://github.com/ziyenano/Password-Manager.git
```
Enter the directory, and note that, the default path your password stored in is **$HOME/.passwd-manage/passwd/**. If you want to change the path,  modify the environment variables in **passwd-manage.conf**, and run

```
./initialize.sh
```



### Usage
```
passwd-man
        insert            insert a new item
        update            update some item's password
        delete            delete an item
        commit            submit the modifications
        log               list all the commits
        show [commit-id]  show all the passwords [historical modifications]
```

* You'd better run **passwd-man commit** to submit the current version before you take update or delete operation. 
* Run **passwd-man log** to list all the commit-id, and view the corresponding historical modifications by the command **passwd-man show commit-id**. It may be very useful when you want to find the passwords that were deleted or updated. 

### Manage Multiple Files
* If you want to add a new password file, as mentioned above, modify the environment variables in **passwd-manage.conf**, and run the **./initialize.sh** script again.
* If more than one password files were created, manage different password file by modifying **\$HOME/.passwd-manage.conf**, and in this case, **do not** run the **./initialize.sh** script.


