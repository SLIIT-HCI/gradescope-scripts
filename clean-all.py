#!/usr/bin/env python

import os
import sys
import re
import time
import subprocess

def init_logs():
    global log
    log = open('clean.log', 'w')

def close_logs():
    global log
    log.close()

def student_info(student):
    print student
    student = student[0:student.find('_')]
    id = re.findall(r"\w{2}\d{8}", student)[0]
    name = student.replace(id, '').strip()
    return id.upper(), name;

def gen_students():
    global startdir
    file = open('students.csv', 'w+')
    os.chdir(startdir)
    entries = []

    for batch in os.listdir('.'):
        if os.path.isdir(batch):
            os.chdir(batch)
            for student in os.listdir('.'):
                if os.path.isdir(student):
                    id, name = student_info(student)
                    entries.append('{0},{1},{2}@my.sliit.lk,Student\n'.format(name, id, id.lower()))
            os.chdir('..')

    file.write('Name,SID,Email,Role\n')
    file.writelines(sorted(entries))
    file.close()
    print 'Student List Generated ...'

def validate_input():
    if len(sys.argv)<=1:
        print 'You must specify a folder'
        exit(1)
    global startdir
    startdir = os.path.abspath(sys.argv[1])

def rename_folders():
    global startdir, log
    os.chdir(startdir)
    for sub in os.listdir('.'):
        if os.path.isdir(sub):
            sub_dir = re.findall(r"\w{2}\d{8}", sub)[0]
            if os.path.exists(sub_dir):
                if sub != sub_dir:
                    log.write('REMOVING DUPLICATE ' + sub + '\n')
                    subprocess.call(['rm', '-rf', sub])
            else:
                os.rename(sub, sub_dir.upper())
    print 'Successfully renamed folders to student ids'

def rec_move_files(folder, basepath):
    os.chdir(folder)
    for sub in os.listdir('.'):
        if os.path.isdir(sub):
            if sub.endswith('.java'):
                sub_dir = sub[0:sub.find('.java')]
                os.rename(sub, sub_dir)
                sub = sub_dir
            rec_move_files(sub, basepath)
            rmtree(sub)
        elif sub.endswith('.java'):
            fullpath = os.path.abspath(sub)
            os.rename(fullpath, basepath+'/'+sub)
        elif sub.endswith('.txt'):
            fullpath = os.path.abspath(sub)
            sub = sub[0:sub.rfind('.')]+'.java'
            os.rename(fullpath, basepath+'/'+sub)
        else:
            os.remove(sub)
    os.chdir('..')

def move_files():
    global startdir
    os.chdir(startdir)
    for studentid in os.listdir(startdir):
        if os.path.isdir(studentid):
            basepath = os.path.abspath(studentid)
            rec_move_files(studentid, basepath)
        else:
            os.remove(studentid)
    print 'Successfully moved all java files to studentid folder'

def merge_files():
    global startdir
    os.chdir(startdir)
    for studentid in os.listdir('.'):
        for file in os.listdir(studentid):
            with open(studentid+'-merged.java','a+') as f:
                f.write(open(studentid+'/'+file, 'r').read())
                f.write('\n')
        rmtree(studentid)
    print 'Successfully merged all java files into one per submission'

def move_folders():
    global startdir
    os.chdir(startdir)
    dest_path = os.getcwd()
    for batch in os.listdir('.'):
        if os.path.isdir(batch):
            os.chdir(batch)
            for submission in os.listdir('.'):
                source_path = os.path.abspath(submission)
                os.rename(source_path, dest_path+'/'+submission)
            os.chdir('..')
            os.rmdir(batch)
    print 'Successfully moved all submission folders to base folder'

def rmtree(name):
    global log
    log.write('REMOVING ' + os.path.abspath(name) + '\n')
    subprocess.call(['rm', '-rf', name])

def rec_sweep():
    for sub in os.listdir('.'):
        if sub.startswith('.'):
            rmtree(sub)
        elif os.path.isdir(sub):
            os.chdir(sub)
            rec_sweep()
            os.chdir('..')
        elif sub.endswith('.java'):
            pass
        elif sub.endswith('.txt'):
            pass
        else:
            os.remove(sub)

def sweep():
    global startdir
    os.chdir(startdir)
    rec_sweep()
    os.chdir('..')
    print 'Successfully removed all IDE generated files'

def extract_remove(command, filename):
    global log
    log.write('EXTRACTING -' + filename + '\n')
    extract_dir = filename.replace('.','_')
    subprocess.call(command.format(exdir=extract_dir, archive=filename).split(' '), stdout=log, stderr=subprocess.PIPE)
    os.remove(filename)
    rec_extract()

def rec_extract():
    for sub in os.listdir('.'):
        if os.path.isdir(sub):
            os.chdir(sub)
            rec_extract()
            os.chdir('..')
        else:
            if (sub.endswith('.zip')):
                extract_remove('unzip -o -j -d {exdir} {archive}', sub)
                break
            elif (sub.endswith('.rar')):
                extract_remove('unrar e -o+ {archive} {exdir}', sub)
                break
            elif (sub.endswith('.jar')):
                extract_remove('jar -xvf {archive}', sub)
                break

def extract_folders():
    global startdir
    os.chdir(startdir)
    rec_extract()
    print 'Successfully extracted all zip, rar, jar files'

def list_empty_entries():
    global startdir
    os.chdir(startdir)
    os.system('clear')
    list = os.listdir('.')
    total = 0
    empty = 0
    for studentid in list:
        files = []
        for file in os.listdir(studentid):
            files.append(file)
        if len(files)==0:
            empty += 1
            print studentid, files
        total += len(files)
    print ''
    print 'Total Students:', len(list)
    print 'Total Files:', total
    print 'Empty Entries:', empty

def main():
    validate_input()
    init_logs()
    gen_students()         # generate student list
    move_folders()         # move all submission folders outside batches
    rename_folders()       # rename folders to student id numbers
    extract_folders()      # extract all zip files recursively
    sweep()                # remove all IDE generated files and folders, and non-java files
    move_files()           # moves all java files base(studentid) folder, removes empty folders
    list_empty_entries()   # list empty entries for sanity checking
    merge_files()          # merge all files inside each student folder into one file
    close_logs()

if __name__ == "__main__":
    main()
