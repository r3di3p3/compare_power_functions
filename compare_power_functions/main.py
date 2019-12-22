'''
Created on 22 déc. 2019

@author: redZA
'''


from time import time_ns
from _io import open
from  tkinter import Tk,Entry,Label,Button
from tkinter import messagebox
from idlelib import window
from _overlapped import NULL
from test.test_enum import threading
from time import sleep

#variable
x_min = 1
x_max = 100
x_step = 10

n_min = 1
n_max = 10
n_step = 1

outfilename = "data.csv"

nb_opr = 0
current_opr = 0

#windows entry
tf_nstep=tf_vnma=tf_vnmi=tf_xstep=tf_vxma=tf_vxmi=tf_tfout = NULL
#label infos
label_stat_prc = label_stat = label_operation =NULL
#bool for statue
iSWorking = False
#Threads
#Thread Create data file
th_job = NULL
#Thread for update the state (value%)
th_statue = NULL
'''
    Calcule x^n using a loop
    IN : x , n
    OUT : time
'''
def power(x,n):
    time = time_ns()
    rest = 1 
    while(n > 0):
        rest = x * rest 
        n = n - 1 
    return (time_ns() - time)

'''
    return the result  of x ^ n/2 
    IN : x , n
    OUT : power (x^n/2)
'''
def power_fast(x,n):
    if(n == 1):
        return x 
    elif(n&1 == 0):
        r = power_fast(x, n >> 1)
        r = r * r 
        return r 
    elif(n&1 == 1):
        r = power_fast(x, n >> 1)
        r = r * r * x 
        return r 

'''
   return the computation time of x ^ n using Algorithme Square and multiply
    IN : x, n
    OUT : time
'''
def power_fast_calculted_time(x,n):
    start_time = time_ns()
    power_fast(x, n)
    return time_ns() - start_time

'''
    update the label of number of operations
    IN : label to show update
    OUT : void
'''
def update_information_operation():
    global x_max,x_min,x_step,n_max,n_min,n_step,nb_opr,label_operation 
    if(get_entry_data_and_update_values() == False):
        label_operation.config(text="Error")
        label_operation.update_idletasks()
        return False
    else:
        nb_opr = ((x_max - x_min)//x_step +1) * ((n_max-n_min)//n_step +1)
        label_operation.config(text=str(nb_opr))
        label_operation.update_idletasks()
        return True
 
'''
    update the values of the variables used from the inputs of the graphical interface
    return True for no errors
    return False for a errors
    IN : Void
    OUT : Bool 
'''   
def get_entry_data_and_update_values():
    global x_max,x_min,x_step,n_max,n_min,n_step,nb_opr,tf_nstep,tf_vnma,tf_vnmi,tf_xstep,tf_vxma,tf_vxmi,tf_tfout,outfilename
    try:
        x_max = int(tf_vxma.get())
        x_min = int(tf_vxmi.get())
        x_step = int(tf_xstep.get())
        n_max = int(tf_vnma.get())
        n_min = int(tf_vnmi.get())
        n_step = int(tf_nstep.get())
        
    except ValueError as ex :
        messagebox.showerror("Error", "The value entered is not an integer\nError : %s"% ex)
        return False
    except Exception as ex:
        messagebox.showerror("Error", "Error :%s"%(ex))
        return False
    if(x_max < x_min):
        messagebox.showerror("Error", "X max need to be > X min")
        return False
    elif(n_max < n_min):
        messagebox.showerror("Error", "N max need to be > N min")
        return False
    elif(n_step == 0):
        messagebox.showerror("Error", "N steps need to be > 0")
        return False
    elif(x_step == 0):
        messagebox.showerror("Error", "X steps need to be > 0")
        return False
    outfilename = tf_tfout.get()
    return True

'''

'''
def update_statue():
    global stopWorking,label_stat_prc,current_opr,label_stat,nb_opr
    while(iSWorking):
        sleep(0.01)
        label_stat.config(text=str(current_opr))
        label_stat.update_idletasks()
        try:
            label_stat_prc.config(text=str(round((current_opr/nb_opr)*100,2))+ "%",)
            label_stat_prc.update_idletasks()
        except Exception:
            continue
    label_stat.config(text=str(current_opr))
    label_stat.update_idletasks()
    try:
        label_stat_prc.config(text=str(round((current_opr/nb_opr)*100,2))+ "%",)
        label_stat_prc.update_idletasks()
    except Exception as e :
        e = NULL
        
'''
    Create Thread for the job , and stop threads 
    In : void
    OUT : Void
'''        
def start_calul_operations():
    global th_job,th_statue,label_stat_prc,label_operation,iSWorking,current_opr
    if( update_information_operation() == False):
        return
    if(iSWorking == True):
        iSWorking = False
        #th_job._stop()
        th_statue._stop()
        label_stat_prc.config(bg="red")
        return 
    else:
        current_opr = 0 
        iSWorking = True
        #create thread for the job 
        th_job = threading.Thread(target=create_data_file)
        #create thread update values
        th_statue = threading.Thread(target=update_statue)
        #start
        th_job.start()
        th_statue.start()
        label_stat_prc.config(bg="green")
        
'''
    Create the graphical interface
    IN : void
    OUT : void
'''
def main_windows():
    global x_max,x_min,x_step,n_max,n_min,n_step,nb_opr,tf_nstep,tf_vnma,tf_vnmi,tf_xstep,tf_vxma,tf_vxmi,tf_tfout,outfilename,label_stat,label_stat_prc,label_operation
    
    windows_ = Tk()
    windows_.config(width=500,height=250)
    windows_.title("compare power functions")
    #create labels, entry, buttons
    label_vxma = Label(windows_, text="X max value :")
    label_vxma.place(x=20,y=10)
    tf_vxma = Entry(windows_)
    tf_vxma.place(x=100,y=10)
    label_vxmi = Label(windows_,text="X min Value :")
    label_vxmi.place(x=20,y=40)
    tf_vxmi = Entry(windows_)
    tf_vxmi.place(x=100,y=40)
    label_xstep = Label(windows_, text="X steps :")
    label_xstep.place(x=20,y=70)
    tf_xstep = Entry(windows_)
    tf_xstep.place(x=100,y=70)
    
    label_vnma = Label(windows_, text="N max value :")
    label_vnma.place(x=230,y=10)
    tf_vnma = Entry(windows_)
    tf_vnma.place(x=310,y=10)
    label_vnmi = Label(windows_, text="N min value :")
    label_vnmi.place(x=230,y=40)
    tf_vnmi = Entry(windows_)
    tf_vnmi.place(x=310,y=40)
    label_nstep = Label(windows_, text="N steps :")
    label_nstep.place(x=230,y=70)
    tf_nstep = Entry(windows_)
    tf_nstep.place(x=310,y=70)
    label_fileout = Label(windows_, text="Out file name :")
    label_fileout.place(x=20,y=100)
    tf_tfout = Entry(windows_)
    tf_tfout.place(x=100,y=100)
    label_operation = Label(windows_, text="----------------")
    label_operation.place(x=130,y=140)
    label_operatio0n = Label(windows_, text="Nbr of operations : ")
    label_operatio0n.place(x=20,y=140)
    label_stat = Label(windows_, text ="void")
    label_stat.place(x=130,y=180)
    label_stat0 = Label(windows_, text ="Current operation :")
    label_stat0.place(x=20,y=180)
    label_stat_prc = Label(windows_, text ="-%",bg="red")
    label_stat_prc.place(x=120,y=200)
    
    aide = Label(windows_, text ="Created by redzack 12/2019",bg="red")
    aide.place(x=200,y=220)
    
    button_start = Button(windows_,text="Start/Stop",command=start_calul_operations)
    button_start.place(x=300,y=140)
    button_info = Button(windows_,text="Update",command=update_information_operation)
    
    button_info.place(x=300,y=190)
    
    #update entry value 
    tf_nstep.insert(0, str(n_step))
    tf_vnma.insert(0, str(n_max))
    tf_vnmi.insert(0,str(n_min))
    tf_xstep.insert(0, str(x_step))
    tf_vxma.insert(0, str(x_max))
    tf_vxmi.insert(0, str(x_min))
    tf_tfout.insert(0, outfilename)
    windows_.mainloop()

'''
    Create a file(csv) for value of x, n, the time required to calculate x ^ n with loop,Algorithme Square and multiply
    sperator '\t'
    IN : void 
    OUT : void
    
'''
def create_data_file():
    global x_max,x_min,x_step,n_max,n_min,n_step,nb_opr,current_opr,outfilename,iSWorking,label_stat_prc
    out = open(outfilename,"w")
    #out.write("x_value\tn_value\tfast_way_time\tnormal_way_time\n")
    x = x_min
    n = n_min
    while(x <= x_max):
        while(n <= n_max):
            t1 = power_fast_calculted_time(x, n)
            t2 = power(x, n)
            line = str(x) +"\t"+str(n)+"\t"+str(t1)+"\t"+str(t2)+"\n"
            out.write(line)
            n = n + n_step
            current_opr = current_opr + 1
            if(iSWorking == False):
                label_stat_prc.config(bg="red")
                messagebox.showerror("Work", "STOP") 
                return 
        out.write("\n")
        x = x + x_step
        n = n_min
    
    out.close()
    iSWorking = False
    messagebox.showinfo("Work", "Job Done [%s], thank you"%current_opr)
    
main_windows()
