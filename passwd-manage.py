from random import choice
import os, string, sys, sqlite3

def GenPassword(length = 8, chars = string.ascii_letters + string.digits + '-----'):
    return ''.join([choice(chars) for i in range(length)])

envir = os.popen(". $HOME/.passwd-manage.conf && echo $PASSWD_FOLDER && echo $PASSWD_FILE").read().split('\n') 
data_folder = envir[0] 
data_file = envir[1]
os.chdir(os.path.join(data_folder, data_file))
data_path = './passwd.db'

class Passwd:
    def __init__(self, data_path):
        self.data_path = data_path
    def insert(self):
	description = raw_input("describe the usage of password: ")
        print "\n"
        style = raw_input("[1]. specify a password  [2]. randomly generate (type 1 or 2): ")
        confirm = "no"
        if style == "1":
            while confirm != "yes":
                print "\n"
                passwd = raw_input("insert the corresponding password: ")
                print "\n" + passwd + "\n"
                confirm = raw_input("Accept this password? yes/no: ")
        elif style == "2":
            print "\n"
            length = raw_input("set the length of the new password, no more than 20: ")
            while confirm != "yes":
                passwd = GenPassword(int(length))
                print "\n" + passwd + "\n"
                confirm = raw_input("Accept this password? yes/no: ")
        else:
            sys.exit()
        if confirm == "yes":
            con = sqlite3.connect(self.data_path)
            con.execute("insert into passwd_py(description, passwd) values('%s', '%s')" %(description, passwd))
	    con.commit()
	    con.close()
            os.system("echo %s >> ./.passwd-history/record" %("insert: " + description))
	    print "\n" + "Done!"
    def update(self):
        item_id = int(raw_input("type the item id you want to update: "))
        con = sqlite3.connect(self.data_path)
        update_item = con.execute("select * from  passwd_py where id = %d" %item_id).fetchone()
        print "\n" + str(update_item[0]) + " | " + update_item[1] + " | " + update_item[2] + "\n"
        style = raw_input("[1]. specify a password  [2]. randomly generate (type 1 or 2): ")
        confirm = "no"
        if style == "1":
            while confirm != "yes":
                print "\n"
                passwd = raw_input("insert the corresponding password: ")
                print "\n" + passwd + "\n"
                confirm = raw_input("Accept this password? yes/no: ")
        elif style == "2":
            print "\n"
            length = raw_input("set the length of the new password, no more than 20: ")
            while confirm != "yes":
                passwd = GenPassword(int(length))
                print "\n" + passwd + "\n"
                confirm = raw_input("Accept this password? yes/no: ")
        else:
            sys.exit()
        if confirm == "yes":
            con.execute("update passwd_py set passwd = '%s' where id = %d" %(passwd, item_id))
            con.commit()
            print "\n" + update_item[2] + " ==> " +  passwd
            print "\n" + "Done!"
            os.system("echo %s >> ./.passwd-history/record" %("update: " + update_item[1]))
        con.close()
    def delete(self):
        item_id = int(raw_input("type the item id you want to delete: "))
        con = sqlite3.connect(self.data_path)
        del_item = con.execute("select * from  passwd_py where id = %d" %item_id).fetchone()
        print "\n" + str(del_item[0]) + " | " + del_item[1] + " | " + del_item[2] + '\n'
        confirm = raw_input("delete this password? yes/no: ")
        if confirm == "yes":
            con.execute("delete from passwd_py  where id = %d" %item_id)
            con.commit()
            os.system("echo %s >> ./.passwd-history/record" %("delete: " + del_item[1]))
            print "\n" + "Done!"
        con.close()
    def commit(self):
        os.system("sqlite3 -header %s 'select * from passwd_py' > ./.passwd-history/passwd" %self.data_path)
        os.system("cd ./.passwd-history/ && git commit -a -F record" )
        os.system("echo '' > ./.passwd-history/record" )
    def show(self, tag = ''):
        if tag == '':
            print os.popen("sqlite3 -header %s 'select * from passwd_py'" %self.data_path).read() 
        else:
            print os.popen("cd ./.passwd-history/ && git show  %s" %tag).read()
    def log(self):
            print os.popen("cd ./.passwd-history/ && git log --pretty=oneline").read()

if __name__ == "__main__":
    pas = Passwd(data_path)
    usage = '''usage: passwd-man
        insert            insert a new item
        update            update some item's password
        delete            delete an item 
        commit            submit the modifications
        log               list all the commits
        show [commit-id]  show all the passwords [historical modifications] ''' 
    if len(sys.argv) == 1:
        print usage
    else:
        if sys.argv[1] == "insert":
            pas.insert()
        elif sys.argv[1] == "update":
            pas.update()
        elif sys.argv[1] == "del":
            pas.delete()
        elif sys.argv[1] == "commit":
            pas.commit()
        elif sys.argv[1] == "log":
            pas.log()
        elif sys.argv[1] == "show" and len(sys.argv) == 2:
            pas.show()
        elif sys.argv[1] == "show" and len(sys.argv) == 3:
            pas.show(sys.argv[2])
        else:
            print usage
