Steps to create a new Xblock:


Make sure you have xblock sdk installed in the directory ( installation process: https://github.com/collabassess/Xblocks-in-OpenEdx/blob/master/readme.md)

1. xblock-sdk/bin/workbench-make-xblock
2. two options pop up:
    1. shortname: this name creates the directory
    2. class name: classname(should start with a capital letter and end with 'XBlock')
3. pip install -e xblockname
4. python xblock-sdk/manage.py migrate
5. python xblock-sdk/manage.py runserver
    

  
  
