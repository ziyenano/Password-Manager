#! /usr/bin/env bash

# set the default configure file  $HOME/.passwd.conf
CONFIG_FILE=passwd-manage.conf

. ./$CONFIG_FILE
cp $CONFIG_FILE $HOME/.$CONFIG_FILE

mkdir -p $PASSWD_FOLDER 

#zsh completion
if [[ $SHELL =~ "zsh" ]]; then
    cp ./_passwd-man $PASSWD_FOLDER
    sudo rm -f /usr/local/share/zsh/site-functions/_passwd-man
    sudo ln -s $PASSWD_FOLDER/_passwd-man /usr/local/share/zsh/site-functions/_passwd-man
fi

cp ./passwd-manage.py $PASSWD_FOLDER

cd $PASSWD_FOLDER

echo "python $PASSWD_FOLDER/passwd-manage.py \$@" > ./passwd-man
chmod u+x passwd-man
sudo rm -f /usr/local/bin/passwd-man
sudo ln -s $PASSWD_FOLDER/passwd-man /usr/local/bin/passwd-man

mkdir $PASSWD_FILE
cd ./$PASSWD_FILE
touch passwd.db

CREATE_TABLE="create table passwd_py
     (id integer primary key autoincrement, 
 	 description,
 	 passwd);"

sqlite3 passwd.db "$CREATE_TABLE"

mkdir .passwd-history
cd .passwd-history

git init
touch record passwd
echo 'record' >> .gitignore 

git add passwd .gitignore 
git commit -m 'initial operation'
