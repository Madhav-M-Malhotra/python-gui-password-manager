import tkinter, importlib
import customtkinter as ctk
from PIL import Image
import mysql.connector
import re, pyperclip
import random, smtplib
import hashlib
from Crypto.Protocol.KDF import PBKDF2

ctk.set_default_color_theme("green")

#MySQL connection
sql= mysql.connector.connect(
  host="localhost",
  user="root", 
  passwd=""#enter your mysql password
)
my_con = sql.cursor()
my_con.execute("Create database if not exists safepassX")
my_con.execute("Use safepassX")
my_con.execute("create table if not exists user_info(email varchar(1000),masterpass varchar(1000),status int)")
sql.commit()

#flag variables
create_show_pass_flag=0
confirm_show_pass_flag=0
new_confirm_show_pass_flag=0
new_show_pass_flag=0
reset_show_pass_flag=0
add_show_pass_flag=0
show_pass_flag=0
edit_show_pass_flag=0
salt=b'\xd7q\x989C\xc4o0y\xd2mJ*6\xdf\x02\xcc\xdes\xe1\xa86f\x9a\xa0\xe5+cT\x05\xafq'

#Main App
def main_application():
    global global_mail
    global global_pass
    app_win=ctk.CTk()
    app_win.title("SafePassX")
    app_win.geometry("700x346")

    topframe=ctk.CTkFrame(master=app_win,width=710,height=80,corner_radius=0,fg_color="green")
    topframe.place(x=0,y=0)

    logo=ctk.CTkLabel(master=topframe, text="SafePassX",font=('Agency FB',62,'bold'),text_color="white")
    logo.place(x=250,y=0)

    def add_pass():
        table=re.sub(r"\W+",'',global_mail)
        app_win.iconify()
        add_win=ctk.CTkToplevel()
        add_win.title("Add Passwd")
        add_win.geometry("400x355")

        title=ctk.CTkLabel(master=add_win, text="Add New Password", font=('Century Gothic',40,'bold'),text_color='green')
        title.place(x=14,y=5)

        c_lable=ctk.CTkLabel(master=add_win, text="Catogary    :", font=("Agency FB",30,'bold'))
        c_lable.place(x=10,y=90)
        c_menu_var=ctk.StringVar()
        c_menu=ctk.CTkOptionMenu(master=add_win, values=['Mail', 'Social Media', 'E-Commerce', 'Streaming', 'Professional', 'Education', 'Gaming', 'Personal'], variable=c_menu_var, width=220, dropdown_fg_color='#00ab41', dropdown_text_color='white', dropdown_hover_color='#21D375', dropdown_font=('calibri',18), font=('calibri',18))
        c_menu.place(x=150,y=100)
        a_lable=ctk.CTkLabel(master=add_win, text="Application :", font=("Agency FB",30,'bold'))
        a_lable.place(x=10,y=140)
        a_entry_var=ctk.StringVar()
        a_entry=ctk.CTkEntry(master=add_win, textvariable=a_entry_var, width=220)
        a_entry.place(x=150,y=148)
        u_lable=ctk.CTkLabel(master=add_win, text="User-id      :", font=("Agency FB",30,'bold'))
        u_lable.place(x=10,y=190)
        u_entry_var=ctk.StringVar()
        u_entry=ctk.CTkEntry(master=add_win, textvariable=u_entry_var, width=220)
        u_entry.place(x=150,y=198)
        p_lable=ctk.CTkLabel(master=add_win, text="Password  :", font=("Agency FB",30,'bold'))
        p_lable.place(x=10,y=240)
        p_entry_var=ctk.StringVar()
        p_entry=ctk.CTkEntry(master=add_win, textvariable=p_entry_var, width=220, show='*')
        p_entry.place(x=150,y=248)
        def show_pass():
            global add_show_pass_flag
            if add_show_pass_flag==0:
                p_entry.configure(show='')
                add_show_pass_flag+=1
            else:
                p_entry.configure(show='*')
                add_show_pass_flag-=1
        view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
        view=ctk.CTkButton(master=add_win,image=view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:show_pass())
        view.place(x=335,y=251)

        def new_pass():
            add_cat=c_menu_var.get()
            add_app=a_entry_var.get().upper()
            add_id=u_entry_var.get()
            add_pass=p_entry_var.get()
            if ((len(add_cat)!=0) and (len(add_app)!=0) and (len(add_id)!=0) and (len(add_pass)!=0)):
                add_win.iconify()
                flag=0
                if len(add_pass)>=10:
                    flag+=1
                for i in add_pass:
                    if i.isupper():
                        flag+=1
                        break
                for i in add_pass:
                    if i in "0123456789":
                        flag+=1
                        break
                for i in add_pass:
                    l=['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}',']','|','',':',';','"',"'",'<',',','>','.','?','/','\\']
                    if i in l:
                        flag+=1
                        break
                if flag!=4:
                    advice_win=ctk.CTkToplevel(add_win)
                    advice_win.title("Password strength")
                    advice_win.geometry("450x120")

                    l1=ctk.CTkLabel(advice_win, text='We advice you to have a stronger password.\nInfact, we can generate one for you.',font=("Century Gothic",20,'bold'))
                    l1.place(x=5,y=5)
                    
                    def generate():
                        advice_win.destroy()
                        generate=ctk.CTkToplevel(add_win)
                        generate.title("Password Generation")
                        generate.geometry("250x135")
                
                        generate_label=ctk.CTkLabel(master=generate,text="Generated Password",font=('Century Gothic',20,"bold"))
                        generate_label.place(x=20,y=10)
                        def generate_pass():
                            uppercase_letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            lowercase_letters="abcdefghijklmnopqrstuvwxyz"
                            numbers="0123456789"
                            symbols="()[]{},;:.-_/\\?+*#"
                            all=uppercase_letters+lowercase_letters+numbers+symbols
                            password="".join(random.sample(all, 12))
                            return password
                        generate_entery_var=ctk.StringVar()
                        generate_entery=ctk.CTkEntry(master=generate,textvariable=generate_entery_var,justify="center",width=120)
                        generate_entery.insert(0,generate_pass())
                        generate_entery.configure(state="disabled")
                        generate_entery.place(x=15,y=50)
                        def regenerate():
                            generate_entery.configure(state='normal')
                            generate_entery.delete(0,'end')
                            generate_entery.insert(0,generate_pass())
                            generate_entery.configure(state="disabled")
                        regenerate_img=ctk.CTkImage(Image.open("input/regenerate.jpg"),size=(18,18))
                        regenerate_button=ctk.CTkButton(master=generate,image=regenerate_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=regenerate)
                        regenerate_button.place(x=145,y=51)
                        def copy():
                            pyperclip.copy(generate_entery_var.get())
                        copy_button=ctk.CTkButton(master=generate,text="Copy",width=50,corner_radius=6,command=copy)
                        copy_button.place(x=185,y=51)
                        def confirm_verify():
                            generate.destroy()
                            generate_pass=generate_entery_var.get()
                            global salt
                            key=PBKDF2(global_pass, salt, dkLen=32)
                            my_con.execute("Insert into {} values(%s, %s, AES_ENCRYPT(%s, %s), AES_ENCRYPT(%s, %s))".format(table), (add_cat, add_app, add_id, key, generate_pass, key))
                            sql.commit()
                            verified_win=ctk.CTkToplevel(add_win)
                            verified_win.title("Verified")
                            verified_win.geometry("315x100")
                            verified_label=ctk.CTkLabel(master=verified_win,text="Password Added Successfully",font=('Century Gothic',20,"bold"))
                            verified_label.place(x=12,y=5)
                            def switch():
                                app_win.deiconify()
                                add_win.destroy()
                            verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                            verified_button.place(x=105,y=50)
                            verified_win.mainloop()
                        generate_button=ctk.CTkButton(master=generate,text="Add",width=50,corner_radius=6,command=confirm_verify)
                        generate_button.place(x=100,y=95)
                        generate.mainloop()
                    b1=ctk.CTkButton(advice_win, text='Generate New', corner_radius=6, font=('clibri',20), command=generate)
                    b1.place(x=50,y=70)
                    
                    def confirm():
                        advice_win.destroy()
                        confirm=ctk.CTkToplevel(add_win)
                        confirm.title("Password Verfication")
                        confirm.geometry("250x135")
                
                        confirm_label=ctk.CTkLabel(master=confirm,text="Confirm Password",font=('Century Gothic',20,"bold"))
                        confirm_label.place(x=35,y=10)
                        confirm_entery_var=ctk.StringVar()
                        confirm_entery=ctk.CTkEntry(master=confirm,textvariable=confirm_entery_var,width=220,show="*")
                        confirm_entery.place(x=15,y=50)
                        def confirm_verify():
                            confirm.destroy()
                            confirm_pass=confirm_entery_var.get()
                            if confirm_pass==add_pass:
                                global salt
                                key=PBKDF2(global_pass, salt, dkLen=32)
                                my_con.execute("Insert into {} values(%s, %s, AES_ENCRYPT(%s, %s), AES_ENCRYPT(%s, %s))".format(table), (add_cat, add_app, add_id, key, add_pass, key))
                                sql.commit()
                                verified_win=ctk.CTkToplevel(add_win)
                                verified_win.title("Verified")
                                verified_win.geometry("315x100")
                                verified_label=ctk.CTkLabel(master=verified_win,text="Password Added Successfully",font=('Century Gothic',20,"bold"))
                                verified_label.place(x=12,y=5)
                                def switch():
                                    app_win.deiconify()
                                    add_win.destroy()
                                verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                verified_button.place(x=105,y=50)
                                verified_win.mainloop()
                            else:
                                failed_win=ctk.CTkToplevel(add_win)
                                failed_win.title("Verifaction Failed")
                                failed_win.geometry("230x100")
                                failed_label=ctk.CTkLabel(master=failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                                failed_label.place(x=26,y=5)
                                def switch():
                                    failed_win.destroy()
                                    add_win.deiconify()
                                    p_entry.delete(0,'end')
                                failed_button=ctk.CTkButton(master=failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                failed_button.place(x=65,y=50)
                                failed_win.mainloop()
                        confirm_button=ctk.CTkButton(master=confirm,text="Add",width=50,corner_radius=6,command=confirm_verify)
                        confirm_button.place(x=100,y=95)
                        confirm.mainloop()
                    b2=ctk.CTkButton(advice_win, text='Continue', corner_radius=6, font=('clibri',20), command=confirm)
                    b2.place(x=250,y=70)

                    advice_win.mainloop()                        
                else:
                    confirm_win=ctk.CTkToplevel(add_win)
                    confirm_win.title("Password Verfication")
                    confirm_win.geometry("250x135")
            
                    confirm_label=ctk.CTkLabel(master=confirm_win,text="Confirm Password",font=('Century Gothic',20,"bold"))
                    confirm_label.place(x=35,y=10)
                    confirm_entery_var=ctk.StringVar()
                    confirm_entery=ctk.CTkEntry(master=confirm_win,textvariable=confirm_entery_var,width=220,show="*")
                    confirm_entery.place(x=15,y=50)
                    def confirm_verify():
                        confirm_win.destroy()
                        confirm_pass=confirm_entery_var.get()
                        if confirm_pass==add_pass:
                            global salt
                            key=PBKDF2(global_pass, salt, dkLen=32)
                            my_con.execute("Insert into {} values(%s, %s, AES_ENCRYPT(%s, %s), AES_ENCRYPT(%s, %s))".format(table), (add_cat, add_app, add_id, key, add_pass, key))
                            sql.commit()
                            verified_win=ctk.CTkToplevel(add_win)
                            verified_win.title("Verified")
                            verified_win.geometry("315x100")
                            verified_label=ctk.CTkLabel(master=verified_win,text="Password Added Successfully",font=('Century Gothic',20,"bold"))
                            verified_label.place(x=12,y=5)
                            def switch():
                                app_win.deiconify()
                                add_win.destroy()
                            verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                            verified_button.place(x=105,y=50)
                            verified_win.mainloop()
                        
                        else:
                            failed_win=ctk.CTkToplevel(add_win)
                            failed_win.title("Verifaction Failed")
                            failed_win.geometry("230x100")
                            failed_label=ctk.CTkLabel(master=failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                            failed_label.place(x=26,y=5)
                            def switch():
                                failed_win.destroy()
                                add_win.deiconify()
                                p_entry.delete(0,'end')
                            failed_button=ctk.CTkButton(master=failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                            failed_button.place(x=65,y=50)
                            failed_win.mainloop()
                    confirm_button=ctk.CTkButton(master=confirm_win,text="Add",width=50,corner_radius=6,command=confirm_verify)
                    confirm_button.place(x=100,y=95)
                    confirm_win.mainloop()

        add_button=ctk.CTkButton(master=add_win, text='Proceed', width=140, corner_radius=6, font=("Agency FB",30,'bold'), command=new_pass)
        add_button.place(x=130,y=295)

        def clear():
            add_win.destroy()
            app_win.deiconify()
        add_win.protocol('WM_DELETE_WINDOW',clear)

        add_win.mainloop()

    def edit_pass():
        table=re.sub(r"\W+",'',global_mail)
        app_win.iconify()
        edit_win=ctk.CTkToplevel()
        edit_win.title("Edit Passwd")
        edit_win.geometry("400x305")

        title=ctk.CTkLabel(master=edit_win, text="Edit Password", font=('Century Gothic',40,'bold'),text_color='green')
        title.place(x=70,y=5)

        c_lable=ctk.CTkLabel(master=edit_win, text="Catogary    :", font=("Agency FB",30,'bold'))
        c_lable.place(x=10,y=90)
        c_menu_var=ctk.StringVar()
        c_menu=ctk.CTkOptionMenu(master=edit_win, values=['Mail', 'Social Media', 'E-Commerce', 'Streaming', 'Professional', 'Education', 'Gaming', 'Personal'], variable=c_menu_var, width=220, dropdown_fg_color='#00ab41', dropdown_text_color='white', dropdown_hover_color='#21D375', dropdown_font=('calibri',18), font=('calibri',18))
        c_menu.place(x=150,y=100)
        a_lable=ctk.CTkLabel(master=edit_win, text="Application :", font=("Agency FB",30,'bold'))
        a_lable.place(x=10,y=140)
        a_entry_var=ctk.StringVar()
        a_entry=ctk.CTkEntry(master=edit_win, textvariable=a_entry_var, width=220)
        a_entry.place(x=150,y=148)
        u_lable=ctk.CTkLabel(master=edit_win, text="User-id      :", font=("Agency FB",30,'bold'))
        u_lable.place(x=10,y=190)
        u_entry_var=ctk.StringVar()
        u_entry=ctk.CTkEntry(master=edit_win, textvariable=u_entry_var, width=220)
        u_entry.place(x=150,y=198)

        def new_pass():
            edit_app=a_entry_var.get().upper()
            edit_id=u_entry_var.get()
            global salt
            key=PBKDF2(global_pass, salt, dkLen=32)
            my_con.execute("Select user_id,convert(AES_DECRYPT(user_id, %s) using utf8) as id from {} where app=%s".format(table),(key, edit_app))
            flag=0
            for entery in my_con:
                if entery[1]==edit_id:
                    edit_id=entery[0]
                    flag+=1
                    break
            my_con.fetchall()
            if (flag==1):
                edit_win.iconify()
                new=ctk.CTkToplevel(edit_win)
                new.title("New Password")
                new.geometry("250x135")
        
                new_label=ctk.CTkLabel(master=new,text="Enter New Password",font=('Century Gothic',20,"bold"))
                new_label.place(x=30,y=10)
                new_entry_var=ctk.StringVar()
                new_entry=ctk.CTkEntry(master=new,textvariable=new_entry_var,width=220,show="*")
                new_entry.place(x=15,y=50)
                def show_pass():
                    global edit_show_pass_flag
                    if edit_show_pass_flag==0:
                        new_entry.configure(show='')
                        edit_show_pass_flag+=1
                    else:
                        new_entry.configure(show='*')
                        edit_show_pass_flag-=1
                view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
                view=ctk.CTkButton(master=new,image=view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:show_pass())
                view.place(x=200,y=53)
                def new_verify():
                    new.destroy()
                    edit_pass=new_entry_var.get()
                    flag=0
                    if len(edit_pass)>=10:
                        flag+=1
                    for i in edit_pass:
                        if i.isupper():
                            flag+=1
                            break
                    for i in edit_pass:
                        if i in "0123456789":
                            flag+=1
                            break
                    for i in edit_pass:
                        l=['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}',']','|','',':',';','"',"'",'<',',','>','.','?','/','\\']
                        if i in l:
                            flag+=1
                            break
                    if flag!=4:
                        advice_win=ctk.CTkToplevel(edit_win)
                        advice_win.title("Password strength")
                        advice_win.geometry("450x120")

                        l1=ctk.CTkLabel(advice_win, text='We advice you to have a stronger password.\nInfact, we can generate one for you.',font=("Century Gothic",20,'bold'))
                        l1.place(x=5,y=5)
                        
                        def generate():
                            advice_win.destroy()
                            generate=ctk.CTkToplevel(edit_win)
                            generate.title("Password Generation")
                            generate.geometry("250x135")
                    
                            generate_label=ctk.CTkLabel(master=generate,text="Generated Password",font=('Century Gothic',20,"bold"))
                            generate_label.place(x=20,y=10)
                            def generate_pass():
                                uppercase_letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                lowercase_letters="abcdefghijklmnopqrstuvwxyz"
                                numbers="0123456789"
                                symbols="()[]{},;:.-_/\\?+*#"
                                all=uppercase_letters+lowercase_letters+numbers+symbols
                                password="".join(random.sample(all, 12))
                                return password
                            generate_entery_var=ctk.StringVar()
                            generate_entery=ctk.CTkEntry(master=generate,textvariable=generate_entery_var,justify="center",width=120)
                            generate_entery.insert(0,generate_pass())
                            generate_entery.configure(state="disabled")
                            generate_entery.place(x=15,y=50)
                            def regenerate():
                                generate_entery.configure(state='normal')
                                generate_entery.delete(0,'end')
                                generate_entery.insert(0,generate_pass())
                                generate_entery.configure(state="disabled")
                            regenerate_img=ctk.CTkImage(Image.open("input/regenerate.jpg"),size=(18,18))
                            regenerate_button=ctk.CTkButton(master=generate,image=regenerate_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=regenerate)
                            regenerate_button.place(x=145,y=51)
                            def copy():
                                pyperclip.copy(generate_entery_var.get())
                            copy_button=ctk.CTkButton(master=generate,text="Copy",width=50,corner_radius=6,command=copy)
                            copy_button.place(x=185,y=51)
                            def confirm_verify():
                                generate.destroy()
                                generate_pass=generate_entery_var.get()
                                global salt
                                key=PBKDF2(global_pass, salt, dkLen=32)
                                my_con.execute("Update {} set pass=AES_ENCRYPT(%s, %s) where app=%s and user_id=%s".format(table), (generate_pass, key, edit_app, edit_id))
                                sql.commit()
                                verified_win=ctk.CTkToplevel(edit_win)
                                verified_win.title("Verified")
                                verified_win.geometry("315x100")
                                verified_label=ctk.CTkLabel(master=verified_win,text="Password Edited Successfully",font=('Century Gothic',20,"bold"))
                                verified_label.place(x=20,y=5)
                                def switch():
                                    app_win.deiconify()
                                    edit_win.destroy()
                                verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                verified_button.place(x=105,y=50)
                                verified_win.mainloop()
                            generate_button=ctk.CTkButton(master=generate,text="Apply",width=50,corner_radius=6,command=confirm_verify)
                            generate_button.place(x=100,y=95)
                            generate.mainloop()
                        b1=ctk.CTkButton(advice_win, text='Generate New', corner_radius=6, font=('clibri',20), command=generate)
                        b1.place(x=50,y=70)
                        
                        def confirm():
                            advice_win.destroy()
                            confirm=ctk.CTkToplevel(edit_win)
                            confirm.title("Password Verfication")
                            confirm.geometry("250x135")
                    
                            confirm_label=ctk.CTkLabel(master=confirm,text="Confirm Password",font=('Century Gothic',20,"bold"))
                            confirm_label.place(x=35,y=10)
                            confirm_entery_var=ctk.StringVar()
                            confirm_entery=ctk.CTkEntry(master=confirm,textvariable=confirm_entery_var,width=220,show="*")
                            confirm_entery.place(x=15,y=50)
                            def confirm_verify():
                                confirm.destroy()
                                confirm_pass=confirm_entery_var.get()
                                if confirm_pass==edit_pass:
                                    global salt
                                    key=PBKDF2(global_pass, salt, dkLen=32)
                                    my_con.execute("Update {} set pass=AES_ENCRYPT(%s, %s) where app=%s and user_id=%s".format(table), (edit_pass, key, edit_app, edit_id))
                                    sql.commit()
                                    verified_win=ctk.CTkToplevel(edit_win)
                                    verified_win.title("Verified")
                                    verified_win.geometry("315x100")
                                    verified_label=ctk.CTkLabel(master=verified_win,text="Password Edited Successfully",font=('Century Gothic',20,"bold"))
                                    verified_label.place(x=20,y=5)
                                    def switch():
                                        app_win.deiconify()
                                        edit_win.destroy()
                                    verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                    verified_button.place(x=105,y=50)
                                    verified_win.mainloop()
                                else:
                                    failed_win=ctk.CTkToplevel(edit_win)
                                    failed_win.title("Verifaction Failed")
                                    failed_win.geometry("230x100")
                                    failed_label=ctk.CTkLabel(master=failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                                    failed_label.place(x=26,y=5)
                                    def switch():
                                        failed_win.destroy()
                                        edit_win.deiconify()
                                    failed_button=ctk.CTkButton(master=failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                    failed_button.place(x=65,y=50)
                                    failed_win.mainloop()
                            confirm_button=ctk.CTkButton(master=confirm,text="Apply",width=50,corner_radius=6,command=confirm_verify)
                            confirm_button.place(x=100,y=95)
                            confirm.mainloop()
                        b2=ctk.CTkButton(advice_win, text='Continue', corner_radius=6, font=('clibri',20), command=confirm)
                        b2.place(x=250,y=70)

                        advice_win.mainloop()
                    else:
                        confirm_win=ctk.CTkToplevel(edit_win)
                        confirm_win.title("Password Verfication")
                        confirm_win.geometry("250x135")
                
                        confirm_label=ctk.CTkLabel(master=confirm_win,text="Confirm Password",font=('Century Gothic',20,"bold"))
                        confirm_label.place(x=35,y=10)
                        confirm_entery_var=ctk.StringVar()
                        confirm_entery=ctk.CTkEntry(master=confirm_win,textvariable=confirm_entery_var,width=220,show="*")
                        confirm_entery.place(x=15,y=50)
                        def confirm_verify():
                            confirm_win.destroy()
                            confirm_pass=confirm_entery_var.get()
                            if confirm_pass==edit_pass:
                                global salt
                                key=PBKDF2(global_pass, salt, dkLen=32)
                                my_con.execute("Update {} set pass=AES_ENCRYPT(%s, %s) where app=%s and user_id=%s".format(table), (edit_pass, key, edit_app, edit_id))
                                sql.commit()
                                verified_win=ctk.CTkToplevel(edit_win)
                                verified_win.title("Verified")
                                verified_win.geometry("315x100")
                                verified_label=ctk.CTkLabel(master=verified_win,text="Password Edited Successfully",font=('Century Gothic',20,"bold"))
                                verified_label.place(x=20,y=5)
                                def switch():
                                    app_win.deiconify()
                                    edit_win.destroy()
                                verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                verified_button.place(x=105,y=50)
                                verified_win.mainloop()
                            
                            else:
                                failed_win=ctk.CTkToplevel(edit_win)
                                failed_win.title("Verifaction Failed")
                                failed_win.geometry("230x100")
                                failed_label=ctk.CTkLabel(master=failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                                failed_label.place(x=26,y=5)
                                def switch():
                                    failed_win.destroy()
                                    edit_win.deiconify()
                                failed_button=ctk.CTkButton(master=failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                failed_button.place(x=65,y=50)
                                failed_win.mainloop()
                        confirm_button=ctk.CTkButton(master=confirm_win,text="Apply",width=50,corner_radius=6,command=confirm_verify)
                        confirm_button.place(x=100,y=95)
                        confirm_win.mainloop()
                new_button=ctk.CTkButton(master=new,text="Proceed",width=50,corner_radius=6,command=new_verify)
                new_button.place(x=100,y=95)
                new.mainloop()

        edit_button=ctk.CTkButton(master=edit_win, text='Proceed', width=140, corner_radius=6, font=("Agency FB",30,'bold'), command=new_pass)
        edit_button.place(x=130,y=245)

        def clear():
            edit_win.destroy()
            app_win.deiconify()
        edit_win.protocol('WM_DELETE_WINDOW',clear)

        edit_win.mainloop()

    def delete_pass():
        table=re.sub(r"\W+",'',global_mail)
        app_win.iconify()
        delete_win=ctk.CTkToplevel()
        delete_win.title("Delete Passwd")
        delete_win.geometry("400x305")

        title=ctk.CTkLabel(master=delete_win, text="Delete Password", font=('Century Gothic',40,'bold'),text_color='green')
        title.place(x=40,y=5)

        c_lable=ctk.CTkLabel(master=delete_win, text="Catogary    :", font=("Agency FB",30,'bold'))
        c_lable.place(x=10,y=90)
        c_menu_var=ctk.StringVar()
        c_menu=ctk.CTkOptionMenu(master=delete_win, values=['Mail', 'Social Media', 'E-Commerce', 'Streaming', 'Professional', 'Education', 'Gaming', 'Personal'], variable=c_menu_var, width=220, dropdown_fg_color='#00ab41', dropdown_text_color='white', dropdown_hover_color='#21D375', dropdown_font=('calibri',18), font=('calibri',18))
        c_menu.place(x=150,y=100)
        a_lable=ctk.CTkLabel(master=delete_win, text="Application :", font=("Agency FB",30,'bold'))
        a_lable.place(x=10,y=140)
        a_entry_var=ctk.StringVar()
        a_entry=ctk.CTkEntry(master=delete_win, textvariable=a_entry_var, width=220)
        a_entry.place(x=150,y=148)
        u_lable=ctk.CTkLabel(master=delete_win, text="User-id      :", font=("Agency FB",30,'bold'))
        u_lable.place(x=10,y=190)
        u_entry_var=ctk.StringVar()
        u_entry=ctk.CTkEntry(master=delete_win, textvariable=u_entry_var, width=220)
        u_entry.place(x=150,y=198)

        def delete():
            delete_app=a_entry_var.get().upper()
            delete_id=u_entry_var.get()
            global salt
            key=PBKDF2(global_pass, salt, dkLen=32)
            my_con.execute("Select user_id,convert(AES_DECRYPT(user_id, %s) using utf8) as id from {} where app=%s".format(table),(key, delete_app))
            flag=0
            for entery in my_con:
                if entery[1]==delete_id:
                    delete_id=entery[0]
                    flag+=1
                    break
            my_con.fetchall()
            if (flag==1):
                delete_win.iconify()
                confirm_win=ctk.CTkToplevel(delete_win)
                confirm_win.title("delete")

                l1=ctk.CTkLabel(confirm_win, text='Are you sure you want to delete\ndata related to '+u_entry_var.get()+' ?',font=("Century Gothic",20,'bold'))
                l1.grid(row=0,column=0, columnspan=2, padx=10, pady=10)

                def yes():
                    confirm_win.destroy()
                    my_con.execute("Delete from {} where app=%s and user_id=%s".format(table), (delete_app, delete_id))
                    sql.commit()
                    verified_win=ctk.CTkToplevel(delete_win)
                    verified_win.title("Deleted")
                    verified_win.geometry("315x100")
                    verified_label=ctk.CTkLabel(master=verified_win,text="Password Deleted Successfully",font=('Century Gothic',20,"bold"))
                    verified_label.place(x=12,y=5)
                    def switch():
                        app_win.deiconify()
                        delete_win.destroy()
                    verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                    verified_button.place(x=105,y=50)
                    verified_win.mainloop()

                b1=ctk.CTkButton(confirm_win, text='YES', corner_radius=6, font=('clibri',20), command=yes)
                b1.grid(row=1, column=0, pady=10)

                def no():
                    delete_win.destroy()
                    app_win.deiconify()

                b2=ctk.CTkButton(confirm_win, text='NO', corner_radius=6, font=('clibri',20), command=no)
                b2.grid(row=1,column=1, pady=10)

                confirm_win.mainloop()

        delete_button=ctk.CTkButton(master=delete_win, text='Proceed', width=140, corner_radius=6, font=("Agency FB",30,'bold'), command=delete)
        delete_button.place(x=130,y=245)

        def clear():
            delete_win.destroy()
            app_win.deiconify()
        delete_win.protocol('WM_DELETE_WINDOW',clear)

        delete_win.mainloop()

    def my_account():
        app_win.iconify()
        account_win=ctk.CTkToplevel(app_win)
        account_win.title("My Account")
        account_win.geometry("600x300")

        title=ctk.CTkLabel(master=account_win, text="MY ACCOUNT", font=('Arial Rounded MT Bold',50,'bold'),text_color='green')
        title.place(x=125,y=5)

        l1=ctk.CTkLabel(master=account_win, text="Logged-in as", font=("Agency FB",40,'bold'))
        l1.place(x=10,y=70)
        l2=ctk.CTkLabel(master=account_win, text='"'+global_mail+'"', font=("Agency FB",40,'bold'))
        l2.place(x=200,y=70)

        def change_pass():
            account_win.iconify()
            otp=""
            for i in range(6):
                otp+=str(random.randint(0,9))
            #mailing OTP
            server=smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login('','')#first parameter is the gmail id through which email is to be sent and second is the google app password for the id
            mail_msg="Your SafePassX email verification OTP is "+otp+'.'
            server.sendmail("",global_mail,mail_msg)#first parameter is the gmail id through which email is to be sent
            server.quit()
            #print(otp)
            mail_verify=ctk.CTkToplevel(app_win)
            mail_verify.title("Email Verfication")
            mail_verify.geometry("250x135")
    
            mail_verify_label=ctk.CTkLabel(master=mail_verify,text="Enter OTP To Verify",font=('Century Gothic',20,"bold"))
            mail_verify_label.place(x=35,y=10)
            mail_verify_entery_var=ctk.StringVar()
            mail_verify_entery=ctk.CTkEntry(master=mail_verify,textvariable=mail_verify_entery_var,width=100,justify='center',font=('Century Gothic',20,"bold"))
            mail_verify_entery.place(x=75,y=50)
            def email_otp_verify():
                mail_verify.destroy()
                if mail_verify_entery_var.get()==otp:
                    reset_win=ctk.CTkToplevel(app_win)
                    reset_win.title("Reset Password")
                    reset_win.geometry("520x300")
                    reset_title=ctk.CTkLabel(master=reset_win,text="Reset Password",font=('Century Gothic',30,"bold"),text_color="green")
                    reset_title.place(x=10,y=5)
                    newpass=ctk.CTkLabel(master=reset_win,text="Create New:",font=('Century Gothic',20,"bold"))
                    newpass.place(x=10,y=50)
                    newpass_entery_var=ctk.StringVar()
                    newpass_entery=ctk.CTkEntry(master=reset_win,textvariable=newpass_entery_var,width=220,show="*")
                    newpass_entery.place(x=135,y=50)
                    def verify_new_masterpass():
                        verify_create_masterpass_flag=0
                        cust_create_masterpass=newpass_entery_var.get()
                        if len(cust_create_masterpass)>=12:
                            verify_create_masterpass_flag+=1
                        for i in cust_create_masterpass:
                            if i.isupper():
                                verify_create_masterpass_flag+=1
                                break
                        for i in cust_create_masterpass:
                            if i in "0123456789":
                                verify_create_masterpass_flag+=1
                                break
                        for i in cust_create_masterpass:
                            l=['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}',']','|','',':',';','"',"'",'<',',','>','.','?','/','\\']
                            if i in l:
                                verify_create_masterpass_flag+=1
                                break
                        reset_win.iconify()
                        if verify_create_masterpass_flag==4:
                            create_masterpass_verified_win=ctk.CTkToplevel(reset_win)
                            create_masterpass_verified_win.title("Masterpass Accepted")
                            create_masterpass_verified_win.geometry("290x100")
                            create_masterpass_verified_label=ctk.CTkLabel(master=create_masterpass_verified_win,text="MasterPassword Accepted",font=('Century Gothic',20,"bold"))
                            create_masterpass_verified_label.place(x=16,y=5)
                            def switch():
                                create_masterpass_verified_win.destroy()
                                reset_win.deiconify()
                                newpass_create_checkbox.configure(variable=var1)
                                newpass_entery.configure(state="disabled")
                                new_button.configure(state="disabled")
                                new_view.configure(state="disabled")
                                newpass_confirm_entery.configure(state="normal")
                                newpass_confirm_button.configure(state="normal")
                            create_masterpass_verified_button=ctk.CTkButton(master=create_masterpass_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                            create_masterpass_verified_button.place(x=95,y=50)
                            create_masterpass_verified_win.mainloop()
                        else:
                            create_masterpass_failed_win=ctk.CTkToplevel(reset_win)
                            create_masterpass_failed_win.title("Masterpass Rejected")
                            create_masterpass_failed_win.geometry("290x100")
                            create_masterpass_failed_label=ctk.CTkLabel(master=create_masterpass_failed_win,text="MasterPassword Rejected",font=('Century Gothic',20,"bold"))
                            create_masterpass_failed_label.place(x=20,y=5)
                            def switch():
                                create_masterpass_failed_win.destroy()
                                reset_win.deiconify()
                                newpass_entery.delete(0,"end")
                            create_masterpass_failed_button=ctk.CTkButton(master=create_masterpass_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                            create_masterpass_failed_button.place(x=95,y=50)
                            create_masterpass_failed_win.mainloop()

                    #passwd show/hide
                    def new_show_pass():
                        global new_show_pass_flag
                        if new_show_pass_flag==0:
                            newpass_entery.configure(show='')
                            new_show_pass_flag+=1
                        else:
                            newpass_entery.configure(show='*')
                            new_show_pass_flag-=1
                    new_view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
                    new_view=ctk.CTkButton(master=reset_win,image=new_view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:new_show_pass())
                    new_view.place(x=320,y=53)
                    new_button=ctk.CTkButton(master=reset_win,text="Verify",width=50,corner_radius=6,command=verify_new_masterpass)
                    new_button.place(x=360,y=50)
                    var1=ctk.StringVar(value="on")
                    var2=ctk.StringVar(value="off")
                    newpass_create_checkbox=ctk.CTkCheckBox(master=reset_win,text="",variable=var2,onvalue="on",offvalue="off",state="disabled")
                    newpass_create_checkbox.place(x=450,y=50)
                    
                    newpass_req1=ctk.CTkLabel(master=reset_win,text="* Atleast 12 characters",font=('Century Gothic',18,"bold"),text_color="green")
                    newpass_req1.place(x=10,y=80)
                    newpass_req2=ctk.CTkLabel(master=reset_win,text="* Atleast 1 uppercase letter",font=('Century Gothic',18,"bold"),text_color="green")
                    newpass_req2.place(x=10,y=110)
                    newpass_req3=ctk.CTkLabel(master=reset_win,text="* Atleast 1 number",font=('Century Gothic',18,"bold"),text_color="green")
                    newpass_req3.place(x=10,y=140)
                    newpass_req4=ctk.CTkLabel(master=reset_win,text="* Atleast 1 symbol",font=('Century Gothic',18,"bold"),text_color="green")
                    newpass_req4.place(x=10,y=170)

                    newpass_confirm=ctk.CTkLabel(master=reset_win,text="Confirm:",font=('Century Gothic',20,"bold"))
                    newpass_confirm.place(x=30,y=210)
                    newpass_confirm_entery_var=ctk.StringVar()
                    newpass_confirm_entery=ctk.CTkEntry(master=reset_win,textvariable=newpass_confirm_entery_var,width=220,show="*",state="disabled")
                    newpass_confirm_entery.place(x=135,y=210)

                    def verify_confirm_masterpass():
                        cust_confirm_masterpass=newpass_confirm_entery_var.get()
                        cust_create_masterpass=newpass_entery_var.get()
                        reset_win.iconify()
                        if cust_confirm_masterpass==cust_create_masterpass:
                            confirm_masterpass_verified_win=ctk.CTkToplevel(reset_win)
                            confirm_masterpass_verified_win.title("Confirmation Successful")
                            confirm_masterpass_verified_win.geometry("290x100")
                            confirm_masterpass_verified_label=ctk.CTkLabel(master=confirm_masterpass_verified_win,text="Confirmation Successful",font=('Century Gothic',20,"bold"))
                            confirm_masterpass_verified_label.place(x=27,y=5)
                            def switch():
                                confirm_masterpass_verified_win.destroy()
                                reset_win.deiconify()
                                newpass_confirm_checkbox.configure(variable=var1)
                                newpass_confirm_entery.configure(state="disabled")
                                newpass_confirm_button.configure(state="disabled")
                                confirm_view.configure(state="disabled")
                                new_submit.configure(state="normal")
                            confirm_masterpass_verified_button=ctk.CTkButton(master=confirm_masterpass_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                            confirm_masterpass_verified_button.place(x=95,y=50)
                            confirm_masterpass_verified_win.mainloop()
                        else:
                            confirm_masterpass_failed_win=ctk.CTkToplevel(reset_win)
                            confirm_masterpass_failed_win.title("Confirmation Failed")
                            confirm_masterpass_failed_win.geometry("290x100")
                            confirm_masterpass_failed_label=ctk.CTkLabel(master=confirm_masterpass_failed_win,text="Confirmation Failed",font=('Century Gothic',20,"bold"))
                            confirm_masterpass_failed_label.place(x=50,y=5)
                            def switch():
                                confirm_masterpass_failed_win.destroy()
                                reset_win.deiconify()
                                newpass_create_checkbox.configure(variable=var2)
                                newpass_entery.configure(state="normal")
                                new_button.configure(state="normal")
                                newpass_entery.delete(0,"end")
                                newpass_confirm_entery.delete(0,"end")
                                newpass_confirm_entery.configure(state="disabled")
                                newpass_confirm_button.configure(state="disabled")
                            new_view.configure(state="normal")
                            confirm_masterpass_failed_button=ctk.CTkButton(master=confirm_masterpass_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                            confirm_masterpass_failed_button.place(x=95,y=50)
                            confirm_masterpass_failed_win.mainloop()

                    #passwd show/hide
                    def confirm_show_pass():
                        global new_confirm_show_pass_flag
                        if new_confirm_show_pass_flag==0:
                            newpass_confirm_entery.configure(show='')
                            new_confirm_show_pass_flag+=1
                        else:
                            newpass_confirm_entery.configure(show='*')
                            new_confirm_show_pass_flag-=1
                    confirm_view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
                    confirm_view=ctk.CTkButton(master=reset_win,image=confirm_view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:confirm_show_pass())
                    confirm_view.place(x=320,y=213)
                    newpass_confirm_button=ctk.CTkButton(master=reset_win,text="Verify",width=50,corner_radius=6,command=verify_confirm_masterpass,state="disabled")
                    newpass_confirm_button.place(x=360,y=210)
                    newpass_confirm_checkbox=ctk.CTkCheckBox(master=reset_win,text="",variable=var2,onvalue="on",offvalue="off",state="disabled")
                    newpass_confirm_checkbox.place(x=450,y=210)

                    def reset():
                        reset_win.destroy()
                        cust_masterpass=newpass_entery_var.get()

                        h=hashlib.new("SHA256")
                        h.update(cust_masterpass.encode())
                        sql_pass=h.hexdigest()
                        h=hashlib.new("SHA256")
                        h.update(global_mail.encode())
                        sql_mail=h.hexdigest()

                        my_con.execute("Update user_info set masterpass='{}' where email='{}'".format(sql_pass,sql_mail))
                        sql.commit()

                        pass_reset_win=ctk.CTkToplevel(app_win)
                        pass_reset_win.title("Reset Successful")
                        pass_reset_win.geometry("290x100")
                        register_label=ctk.CTkLabel(master=pass_reset_win,text="Reset Successful",font=('Century Gothic',20,"bold"))
                        register_label.place(x=67,y=5)
                        def switch():
                            pass_reset_win.destroy()
                            account_win.deiconify()
                        register_button=ctk.CTkButton(master=pass_reset_win,text="OK",width=100,corner_radius=6,command=switch)
                        register_button.place(x=95,y=50)
                        pass_reset_win.mainloop()
                    
                    new_submit=ctk.CTkButton(master=reset_win,width=100,text="Reset",corner_radius=6,command=reset,state="disabled")
                    new_submit.place(x=200,y=255)

                    reset_win.mainloop()

                else:
                    mail_failed_win=ctk.CTkToplevel(app_win)
                    mail_failed_win.title("Verification Failed")
                    mail_failed_win.geometry("230x100")
                    mail_failed_label=ctk.CTkLabel(master=mail_failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                    mail_failed_label.place(x=26,y=5)
                    def switch():
                        mail_failed_win.destroy()
                        account_win.deiconify()
                    mail_failed_button=ctk.CTkButton(master=mail_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                    mail_failed_button.place(x=65,y=50)
                    mail_failed_win.mainloop()
            mail_verify_button=ctk.CTkButton(master=mail_verify,text="Verify",width=50,corner_radius=6,command=email_otp_verify)
            mail_verify_button.place(x=100,y=95)
    
            def timeup():
                if mail_verify.winfo_exists()==1:
                    mail_verify.destroy()
                    timeup_win=ctk.CTkToplevel(app_win)
                    timeup_win.title("Time Exceeded")
                    timeup_win.geometry("230x100")
                    timeup_label=ctk.CTkLabel(master=timeup_win,text="Time Limit Exceeded",font=('Century Gothic',20,"bold"))
                    timeup_label.place(x=17,y=5)
                    def switch():
                        timeup_win.destroy()
                        account_win.deiconify()
                    timeup_button=ctk.CTkButton(master=timeup_win,text="Try Again",width=100,corner_radius=6,command=switch)
                    timeup_button.place(x=65,y=50)
                    timeup_win.mainloop()
            mail_verify.after(60000,lambda:timeup())

            def clear():
                mail_verify.destroy()
                account_win.deiconify()
            mail_verify.protocol('WM_DELETE_WINDOW',clear)

            mail_verify.mainloop()

        l3=ctk.CTkLabel(master=account_win, text=">> Change Masterpass", font=("Agency FB",40,'bold'), text_color="#125488")
        l3.place(x=10,y=130)
        l3.bind('<Button>', lambda e:change_pass())

        def delete_account():
            account_win.iconify()
            confirm_win=ctk.CTkToplevel(account_win)
            confirm_win.title("delete")

            l1=ctk.CTkLabel(confirm_win, text='Are you sure you want to delete your account?\nOnce deleted the account or any related data would not be recoverable.',font=("Century Gothic",20,'bold'))
            l1.grid(row=0,column=0, columnspan=2, padx=10, pady=10)

            def yes():
                table=re.sub(r"\W+",'',global_mail)
                confirm_win.destroy()
                h=hashlib.new("SHA256")
                h.update(global_mail.encode())
                sql_mail=h.hexdigest()
                my_con.execute("Drop table {}".format(table))
                my_con.execute("Delete from user_info where email='{}'".format(sql_mail))
                sql.commit()
                verified_win=ctk.CTkToplevel(account_win)
                verified_win.title("Deleted")
                verified_win.geometry("315x100")
                verified_label=ctk.CTkLabel(master=verified_win,text="Account Deleted Successfully",font=('Century Gothic',20,"bold"))
                verified_label.place(x=12,y=5)
                def switch():
                    app_win.destroy()
                    pyperclip.copy('')
                    sign_in()
                verified_button=ctk.CTkButton(master=verified_win,text="OK",width=100,corner_radius=6,command=switch)
                verified_button.place(x=105,y=50)
                verified_win.mainloop()

            b1=ctk.CTkButton(confirm_win, text='YES', corner_radius=6, font=('clibri',20), command=yes)
            b1.grid(row=1, column=0, pady=10)

            def no():
                confirm_win.destroy()
                account_win.deiconify()

            b2=ctk.CTkButton(confirm_win, text='NO', corner_radius=6, font=('clibri',20), command=no)
            b2.grid(row=1,column=1, pady=10)

            confirm_win.mainloop()

        l4=ctk.CTkLabel(master=account_win, text=">> Delete Account", font=("Agency FB",40,'bold'), text_color="#125488")
        l4.place(x=10,y=180)
        l4.bind('<Button>', lambda e:delete_account())

        def logout():
            account_win.iconify()
            confirm_win=ctk.CTkToplevel(account_win)
            confirm_win.title("logout")

            l1=ctk.CTkLabel(confirm_win, text='Are you sure you want to logout?',font=("Century Gothic",20,'bold'))
            l1.grid(row=0,column=0, columnspan=2, padx=10, pady=10)

            def yes():
                app_win.destroy()
                pyperclip.copy('')
                sign_in()

            b1=ctk.CTkButton(confirm_win, text='YES', corner_radius=6, font=('clibri',20), command=yes)
            b1.grid(row=1, column=0, pady=10)

            def no():
                confirm_win.destroy()
                account_win.deiconify()

            b2=ctk.CTkButton(confirm_win, text='NO', corner_radius=6, font=('clibri',20), command=no)
            b2.grid(row=1,column=1, pady=10)

            confirm_win.mainloop()

        l5=ctk.CTkLabel(master=account_win, text=">> Logout", font=("Agency FB",40,'bold'), text_color="#125488")
        l5.place(x=10, y=228)
        l5.bind('<Button>',lambda e:logout())

        def clear():
            account_win.destroy()
            app_win.deiconify()
        account_win.protocol('WM_DELETE_WINDOW',clear)

        account_win.mainloop()

    #Main Function Buttons
    ADD=ctk.CTkButton(master=app_win, text="ADD", corner_radius=0, font=('Agency FB',40,'bold'), fg_color="green", width=230, height=70, border_color="white", border_width=2, command=add_pass)
    ADD.place(x=0,y=80)
    EDIT=ctk.CTkButton(master=app_win, text="EDIT", corner_radius=0, font=('Agency FB',40,'bold'), fg_color="green", width=230, height=70,border_color="white",border_width=2, command=edit_pass)
    EDIT.place(x=0,y=145)
    DELETE=ctk.CTkButton(master=app_win, text="DELETE", corner_radius=0, font=('Agency FB',40,'bold'), fg_color="green", width=230, height=70,border_color="white",border_width=2, command=delete_pass)
    DELETE.place(x=0,y=210)
    ACCOUNT=ctk.CTkButton(master=app_win, text="MY ACCOUNT", corner_radius=0, font=('Agency FB',40,'bold'), fg_color="green", width=230, height=70,border_color="white",border_width=2, command=my_account)
    ACCOUNT.place(x=0,y=275)

    lable=ctk.CTkLabel(master=app_win, text="Password Categories", font=('Agency FB',40,'bold'))
    lable.place(x=240,y=85)

    def generate(cat):
        table=re.sub(r"\W+",'',global_mail)
        my_con.execute("Select Distinct category from {}".format(table))
        flag=0
        for category in my_con:
            for c in category:
                if c==cat:
                    flag+=1
        if flag!=0:
            app_win.iconify()
            f=open("generated.py",'w')
            f.write("import customtkinter as ctk")
            f.write("\nimport pyperclip")
            my_con.execute("Select count(*) from {} where category='{}'".format(table,cat))
            for num in my_con:
                for i in range(num[0]):
                    f.write("\nflag"+str(i+2)+"=0")                                     
            f.write("\ndef display_pass():")
            f.write("\n\tdisplay_win=ctk.CTk()")
            f.write("\n\tdisplay_win.title('"+cat+"')")
            f.write("\n\ttitle=ctk.CTkLabel(master=display_win, text='"+cat.upper()+"', font=('Agency FB',72,'bold'), text_color='green')")
            f.write("\n\ttitle.grid(row=0, column=0, columnspan=5)")
            l=["\n\tc1=ctk.CTkButton(master=display_win, text='Application', font=('Agency FB',45,'bold'), width=220, corner_radius=6)",
            "\n\tc1.grid(row=1,column=0,padx=10,pady=10)",
            "\n\tc2=ctk.CTkButton(master=display_win, text='User-id', font=('Agency FB',45,'bold'), width=220, corner_radius=6)",
            "\n\tc2.grid(row=1,column=1,padx=10,pady=10)",
            "\n\tc3=ctk.CTkButton(master=display_win, text='Password', font=('Agency FB',45,'bold'), width=220, corner_radius=6)",
            "\n\tc3.grid(row=1,column=2,padx=10,pady=10)"]
            f.writelines(l)

            global salt
            key=PBKDF2(global_pass, salt, dkLen=32)
            my_con.execute("Select app,convert(AES_DECRYPT(user_id, %s) using utf8) as id,convert(AES_DECRYPT(pass, %s) using utf8) as passwd from {} where category='{}' order by app ASC".format(table,cat),(key,key))
            f.write("\n\tdef copy(x):\n\t\t\tpyperclip.copy(x)")
            row_num=2
            for data in my_con:
                f.write("\n\tc_lable"+str(row_num)+"=ctk.CTkLabel(display_win, text='"+data[0]+"', font=('Agency FB',40))\n\tc_lable"+str(row_num)+".grid(row="+str(row_num)+",column=0,padx=5,pady=5)")
                f.write("\n\tu_lable"+str(row_num)+"=ctk.CTkLabel(display_win, text='"+data[1]+"', font=('Agency FB',40))\n\tu_lable"+str(row_num)+".grid(row="+str(row_num)+",column=1,padx=5,pady=5)")
                f.write("\n\tentry"+str(row_num)+"=ctk.CTkEntry(display_win,justify='center',width=220,show='*')")
                f.write("\n\tentry"+str(row_num)+".insert(0,'"+data[2]+"')\n\tentry"+str(row_num)+".configure(state='disabled')\n\tentry"+str(row_num)+".grid(row="+str(row_num)+",column=2,padx=5,pady=5)")
                f.write("\n\tdef show_pass"+str(row_num)+"():\n\t\tglobal flag"+str(row_num)+"\n\t\tif flag"+str(row_num)+"==0:\n\t\t\tentry"+str(row_num)+".configure(show='')\n\t\t\tview"+str(row_num)+".configure(text='hide')\n\t\t\tflag"+str(row_num)+"+=1\n\t\telse:\n\t\t\tentry"+str(row_num)+".configure(show='*')\n\t\t\tview"+str(row_num)+".configure(text='show')\n\t\t\tflag"+str(row_num)+"-=1")
                f.write("\n\tview"+str(row_num)+"=ctk.CTkButton(display_win,text='show',width=50,corner_radius=6,command=lambda:show_pass"+str(row_num)+"())\n\tview"+str(row_num)+".grid(row="+str(row_num)+",column=3)")
                f.write("\n\tcb"+str(row_num)+"=ctk.CTkButton(display_win,text='copy',width=50,corner_radius=6,command=lambda:copy('"+data[2]+"'))\n\tcb"+str(row_num)+".grid(row="+str(row_num)+",column=4)")

                row_num+=1

            f.write("\n\tdef close():")
            f.write("\n\t\tdisplay_win.quit()\n\t\tdisplay_win.destroy()")
            f.write("\n\tdisplay_win.protocol('WM_DELETE_WINDOW',close)")
            f.write("\n\tdisplay_win.mainloop()")
            f.write("\n\treturn")
            f.close()
            import generated
            importlib.reload(generated)
            generated.display_pass()
            f=open("generated.py",'w')
            f.close()
            app_win.deiconify()

    mail_cat=ctk.CTkButton(master=app_win, text="Mail", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("Mail"))
    mail_cat.place(x=240,y=157)
    social_cat=ctk.CTkButton(master=app_win, text="Social Media", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("Social Media"))
    social_cat.place(x=395,y=157)
    commerce_cat=ctk.CTkButton(master=app_win, text="E-Commerce", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("E-Commerce"))
    commerce_cat.place(x=550,y=157)

    streaming_cat=ctk.CTkButton(master=app_win, text="Streaming", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("Streaming"))
    streaming_cat.place(x=240,y=222)
    professional_cat=ctk.CTkButton(master=app_win, text="Professional", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("Professional"))
    professional_cat.place(x=395,y=222)
    education_cat=ctk.CTkButton(master=app_win, text="Education", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("Education"))
    education_cat.place(x=550,y=222)

    gaming_cat=ctk.CTkButton(master=app_win, text="Gaming", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("Gaming"))
    gaming_cat.place(x=315,y=287)
    personal_cat=ctk.CTkButton(master=app_win, text="Personal", font=('Agency FB',30), width=140, corner_radius=6, command=lambda:generate("Personal"))
    personal_cat.place(x=475,y=287)

    def clear():
        pyperclip.copy('')
        app_win.destroy()
    app_win.protocol('WM_DELETE_WINDOW',clear)

    app_win.mainloop()

def sign_in():
    #log-in window
    login=ctk.CTk()
    login.title("SafePassX")
    login.geometry("580x440")

    #Creating an account
    def create_one():
        creation=ctk.CTkToplevel(login)
        creation.title("Create new account")
        creation.geometry('580x540')
        login.iconify()

        regis_lable=ctk.CTkLabel(master=creation,text="Create Account", font=('Century Gothic',28,"bold"))
        regis_lable.place(x=30,y=20)
        
        #Personal-info Verifaction Frame
        create_info=ctk.CTkFrame(master=creation,width=520,height=160,corner_radius=15,border_width=2,border_color='black')
        create_info.place(x=29,y=60)

        info_title=ctk.CTkLabel(master=create_info,text="E-Mail Verification",font=('Century Gothic',20,"bold"),text_color="green")
        info_title.place(x=10,y=5)

        info_email=ctk.CTkLabel(master=create_info,text="Email:",font=('Century Gothic',20,"bold"))
        info_email.place(x=10,y=75)
        info_email_entery_var=ctk.StringVar()
        info_email_entery=ctk.CTkEntry(master=create_info,textvariable=info_email_entery_var,width=220)
        info_email_entery.place(x=80,y=75)
        
        def verify_email():
            cust_email=info_email_entery_var.get()
            h=hashlib.new("SHA256")
            h.update(cust_email.encode())
            check_email=h.hexdigest()
            pattern=re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}")
            if pattern.match(cust_email):
                creation.iconify()
                my_con.execute("Select count(*) from user_info where email='{}'".format(check_email))
                for mail_exists in my_con:
                    if mail_exists[0]==1:
                        mail_exists_win=ctk.CTkToplevel(creation)
                        mail_exists_win.title("Email Exists")
                        mail_exists_win.geometry("290x100")
                        mail_exists_str='''An account with this email
    already exists'''
                        mail_exists_label=ctk.CTkLabel(master=mail_exists_win,text=mail_exists_str,font=('Century Gothic',20,"bold"))
                        mail_exists_label.place(x=17,y=5)
                        def switch():
                            mail_exists_win.destroy()
                            login.deiconify()
                            creation.destroy()
                        mail_exists_button=ctk.CTkButton(master=mail_exists_win,text="OK",width=100,corner_radius=6,command=switch)
                        mail_exists_button.place(x=95,y=60)
                        mail_exists_win.mainloop()
                    else:
                        otp=""
                        for i in range(6):
                            otp+=str(random.randint(0,9))
                        #mailing OTP
                        server=smtplib.SMTP("smtp.gmail.com",587)
                        server.starttls()
                        server.login('','')#first parameter is the gmail id through which email is to be sent and second is the google app password for the id
                        mail_msg="Your SafePassX email verification OTP is "+otp+'.'
                        server.sendmail("",cust_email,mail_msg)#first parameter is the gmail id through which email is to be sent
                        server.quit()
                        #print(otp)
                        mail_verify=ctk.CTkToplevel(creation)
                        mail_verify.title("Email Verfication")
                        mail_verify.geometry("250x135")
                
                        mail_verify_label=ctk.CTkLabel(master=mail_verify,text="Enter OTP To Verify",font=('Century Gothic',20,"bold"))
                        mail_verify_label.place(x=35,y=10)
                        mail_verify_entery_var=ctk.StringVar()
                        mail_verify_entery=ctk.CTkEntry(master=mail_verify,textvariable=mail_verify_entery_var,width=100,justify='center',font=('Century Gothic',20,"bold"))
                        mail_verify_entery.place(x=75,y=50)
                        def email_otp_verify():
                            mail_verify.destroy()
                            if mail_verify_entery_var.get()==otp:
                                mail_verified_win=ctk.CTkToplevel(creation)
                                mail_verified_win.title("Email Verified")
                                mail_verified_win.geometry("250x100")
                                mail_verified_label=ctk.CTkLabel(master=mail_verified_win,text="Verification Successful",font=('Century Gothic',20,"bold"))
                                mail_verified_label.place(x=16,y=5)
                                def switch():
                                    mail_verified_win.destroy()
                                    creation.deiconify()
                                    info_email_checkbox.configure(variable=var1)
                                    info_email_entery.configure(state="disabled")
                                    info_email_button.configure(state="disabled")
                                    masterpass_create_entery.configure(state="normal")
                                    masterpass_create_button.configure(state="normal")
                                mail_verified_button=ctk.CTkButton(master=mail_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                mail_verified_button.place(x=75,y=50)
                                mail_verified_win.mainloop()
                            else:
                                mail_failed_win=ctk.CTkToplevel(creation)
                                mail_failed_win.title("Verifaction Failed")
                                mail_failed_win.geometry("230x100")
                                mail_failed_label=ctk.CTkLabel(master=mail_failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                                mail_failed_label.place(x=26,y=5)
                                def switch():
                                    mail_failed_win.destroy()
                                    creation.deiconify()
                                    info_email_entery.delete(0,'end')
                                mail_failed_button=ctk.CTkButton(master=mail_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                mail_failed_button.place(x=65,y=50)
                                mail_failed_win.mainloop()
                        mail_verify_button=ctk.CTkButton(master=mail_verify,text="Verify",width=50,corner_radius=6,command=email_otp_verify)
                        mail_verify_button.place(x=100,y=95)
                
                        def timeup():
                            if mail_verify.winfo_exists()==1:
                                mail_verify.destroy()
                                timeup_win=ctk.CTkToplevel(creation)
                                timeup_win.title("Time Exceeded")
                                timeup_win.geometry("230x100")
                                timeup_label=ctk.CTkLabel(master=timeup_win,text="Time Limit Exceeded",font=('Century Gothic',20,"bold"))
                                timeup_label.place(x=17,y=5)
                                def switch():
                                    timeup_win.destroy()
                                    creation.deiconify()
                                    info_email_entery.delete(0,'end')
                                timeup_button=ctk.CTkButton(master=timeup_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                timeup_button.place(x=65,y=50)
                                timeup_win.mainloop()
                        mail_verify.after(60000,lambda:timeup())

                        mail_verify.mainloop()
                
        info_email_button=ctk.CTkButton(master=create_info,text="Verify",width=50,corner_radius=6,command=verify_email)
        info_email_button.place(x=320,y=75)
        var1=ctk.StringVar(value="on")
        var2=ctk.StringVar(value="off")
        info_email_checkbox=ctk.CTkCheckBox(master=create_info,text="",variable=var2,onvalue="on",offvalue="off",state="disabled")
        info_email_checkbox.place(x=410,y=75)

        #MasterPasswd frame
        create_masterpass=ctk.CTkFrame(master=creation,width=520,height=260,corner_radius=15,border_width=2,border_color='black')
        create_masterpass.place(x=29,y=225)

        masterpass_title=ctk.CTkLabel(master=create_masterpass,text="MasterPassword",font=('Century Gothic',20,"bold"),text_color="green")
        masterpass_title.place(x=10,y=5)

        masterpass_create=ctk.CTkLabel(master=create_masterpass,text="Create:",font=('Century Gothic',20,"bold"))
        masterpass_create.place(x=10,y=50)
        masterpass_create_entery_var=ctk.StringVar()
        masterpass_create_entery=ctk.CTkEntry(master=create_masterpass,textvariable=masterpass_create_entery_var,width=220,show="*",state="disabled")
        masterpass_create_entery.place(x=95,y=50)

        def verify_create_masterpass():
            verify_create_masterpass_flag=0
            cust_create_masterpass=masterpass_create_entery_var.get()
            if len(cust_create_masterpass)>=12:
                verify_create_masterpass_flag+=1
            for i in cust_create_masterpass:
                if i.isupper():
                    verify_create_masterpass_flag+=1
                    break
            for i in cust_create_masterpass:
                if i in "0123456789":
                    verify_create_masterpass_flag+=1
                    break
            for i in cust_create_masterpass:
                l=['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}',']','|','',':',';','"',"'",'<',',','>','.','?','/','\\']
                if i in l:
                    verify_create_masterpass_flag+=1
                    break
            creation.iconify()
            if verify_create_masterpass_flag==4:
                create_masterpass_verified_win=ctk.CTkToplevel(creation)
                create_masterpass_verified_win.title("Masterpass Accepted")
                create_masterpass_verified_win.geometry("290x100")
                create_masterpass_verified_label=ctk.CTkLabel(master=create_masterpass_verified_win,text="MasterPassword Accepted",font=('Century Gothic',20,"bold"))
                create_masterpass_verified_label.place(x=16,y=5)
                def switch():
                    create_masterpass_verified_win.destroy()
                    creation.deiconify()
                    masterpass_create_checkbox.configure(variable=var1)
                    masterpass_create_entery.configure(state="disabled")
                    masterpass_create_button.configure(state="disabled")
                    create_view.configure(state="disabled")
                    masterpass_confirm_entery.configure(state="normal")
                    masterpass_confirm_button.configure(state="normal")
                create_masterpass_verified_button=ctk.CTkButton(master=create_masterpass_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                create_masterpass_verified_button.place(x=95,y=50)
                create_masterpass_verified_win.mainloop()
            else:
                create_masterpass_failed_win=ctk.CTkToplevel(creation)
                create_masterpass_failed_win.title("Masterpass Rejected")
                create_masterpass_failed_win.geometry("290x100")
                create_masterpass_failed_label=ctk.CTkLabel(master=create_masterpass_failed_win,text="MasterPassword Rejected",font=('Century Gothic',20,"bold"))
                create_masterpass_failed_label.place(x=20,y=5)
                def switch():
                    create_masterpass_failed_win.destroy()
                    creation.deiconify()
                    masterpass_create_entery.delete(0,"end")
                create_masterpass_failed_button=ctk.CTkButton(master=create_masterpass_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                create_masterpass_failed_button.place(x=95,y=50)
                create_masterpass_failed_win.mainloop()

        #passwd show/hide
        def create_show_pass():
            global create_show_pass_flag
            if create_show_pass_flag==0:
                masterpass_create_entery.configure(show='')
                create_show_pass_flag+=1
            else:
                masterpass_create_entery.configure(show='*')
                create_show_pass_flag-=1
        create_view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
        create_view=ctk.CTkButton(master=create_masterpass,image=create_view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:create_show_pass())
        create_view.place(x=280,y=53)
        masterpass_create_button=ctk.CTkButton(master=create_masterpass,text="Verify",width=50,corner_radius=6,command=verify_create_masterpass,state="disabled")
        masterpass_create_button.place(x=320,y=50)
        masterpass_create_checkbox=ctk.CTkCheckBox(master=create_masterpass,text="",variable=var2,onvalue="on",offvalue="off",state="disabled")
        masterpass_create_checkbox.place(x=410,y=50)

        masterpass_req1=ctk.CTkLabel(master=create_masterpass,text="* Atleast 12 characters",font=('Century Gothic',18,"bold"),text_color="green")
        masterpass_req1.place(x=10,y=80)
        masterpass_req2=ctk.CTkLabel(master=create_masterpass,text="* Atleast 1 uppercase letter",font=('Century Gothic',18,"bold"),text_color="green")
        masterpass_req2.place(x=10,y=110)
        masterpass_req3=ctk.CTkLabel(master=create_masterpass,text="* Atleast 1 number",font=('Century Gothic',18,"bold"),text_color="green")
        masterpass_req3.place(x=10,y=140)
        masterpass_req4=ctk.CTkLabel(master=create_masterpass,text="* Atleast 1 symbol",font=('Century Gothic',18,"bold"),text_color="green")
        masterpass_req4.place(x=10,y=170)

        masterpass_confirm=ctk.CTkLabel(master=create_masterpass,text="Confirm:",font=('Century Gothic',20,"bold"))
        masterpass_confirm.place(x=10,y=210)
        masterpass_confirm_entery_var=ctk.StringVar()
        masterpass_confirm_entery=ctk.CTkEntry(master=create_masterpass,textvariable=masterpass_confirm_entery_var,width=220,show="*",state="disabled")
        masterpass_confirm_entery.place(x=95,y=210)
        
        def verify_confirm_masterpass():
            cust_confirm_masterpass=masterpass_confirm_entery_var.get()
            cust_create_masterpass=masterpass_create_entery_var.get()
            creation.iconify()
            if cust_confirm_masterpass==cust_create_masterpass:
                confirm_masterpass_verified_win=ctk.CTkToplevel(creation)
                confirm_masterpass_verified_win.title("Confirmation Successful")
                confirm_masterpass_verified_win.geometry("290x100")
                confirm_masterpass_verified_label=ctk.CTkLabel(master=confirm_masterpass_verified_win,text="Confirmation Successful",font=('Century Gothic',20,"bold"))
                confirm_masterpass_verified_label.place(x=27,y=5)
                def switch():
                    confirm_masterpass_verified_win.destroy()
                    creation.deiconify()
                    masterpass_confirm_checkbox.configure(variable=var1)
                    masterpass_confirm_entery.configure(state="disabled")
                    masterpass_confirm_button.configure(state="disabled")
                    confirm_view.configure(state="disabled")
                    create_submit.configure(state="normal")
                confirm_masterpass_verified_button=ctk.CTkButton(master=confirm_masterpass_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                confirm_masterpass_verified_button.place(x=95,y=50)
                confirm_masterpass_verified_win.mainloop()
            else:
                confirm_masterpass_failed_win=ctk.CTkToplevel(creation)
                confirm_masterpass_failed_win.title("Confirmation Failed")
                confirm_masterpass_failed_win.geometry("290x100")
                confirm_masterpass_failed_label=ctk.CTkLabel(master=confirm_masterpass_failed_win,text="Confirmation Failed",font=('Century Gothic',20,"bold"))
                confirm_masterpass_failed_label.place(x=50,y=5)
                def switch():
                    confirm_masterpass_failed_win.destroy()
                    creation.deiconify()
                    masterpass_create_checkbox.configure(variable=var2)
                    masterpass_create_entery.configure(state="normal")
                    masterpass_create_button.configure(state="normal")
                    masterpass_create_entery.delete(0,"end")
                    masterpass_confirm_entery.delete(0,"end")
                    masterpass_confirm_entery.configure(state="disabled")
                    masterpass_confirm_button.configure(state="disabled")
                    create_view.configure(state="normal")
                confirm_masterpass_failed_button=ctk.CTkButton(master=confirm_masterpass_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                confirm_masterpass_failed_button.place(x=95,y=50)
                confirm_masterpass_failed_win.mainloop()

        #passwd show/hide
        def confirm_show_pass():
            global confirm_show_pass_flag
            if confirm_show_pass_flag==0:
                masterpass_confirm_entery.configure(show='')
                confirm_show_pass_flag+=1
            else:
                masterpass_confirm_entery.configure(show='*')
                confirm_show_pass_flag-=1
        confirm_view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
        confirm_view=ctk.CTkButton(master=create_masterpass,image=confirm_view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:confirm_show_pass())
        confirm_view.place(x=280,y=213)
        masterpass_confirm_button=ctk.CTkButton(master=create_masterpass,text="Verify",width=50,corner_radius=6,command=verify_confirm_masterpass,state="disabled")
        masterpass_confirm_button.place(x=320,y=210)
        masterpass_confirm_checkbox=ctk.CTkCheckBox(master=create_masterpass,text="",variable=var2,onvalue="on",offvalue="off",state="disabled")
        masterpass_confirm_checkbox.place(x=410,y=210)

        def register():
            cust_mail=info_email_entery_var.get()
            cust_masterpass=masterpass_create_entery_var.get()

            h=hashlib.new("SHA256")
            h.update(cust_mail.encode())
            sql_mail=h.hexdigest()
            h=hashlib.new("SHA256")
            h.update(cust_masterpass.encode())
            sql_pass=h.hexdigest()
            table=re.sub(r"\W+",'',cust_mail)

            my_con.execute("Insert into user_info values('{}','{}',1)".format(sql_mail,sql_pass))
            my_con.execute("Create table {}(category varchar(100),app varchar(100),user_id varbinary(255),pass varbinary(255))".format(table))
            sql.commit()

            creation.destroy()
            register_win=ctk.CTkToplevel(login)
            register_win.title("Registration Successful")
            register_win.geometry("290x100")
            register_label=ctk.CTkLabel(master=register_win,text="Registration Successful",font=('Century Gothic',20,"bold"))
            register_label.place(x=34,y=5)
            def switch():
                register_win.destroy()
                login.deiconify()
            register_button=ctk.CTkButton(master=register_win,text="Sign-in",width=100,corner_radius=6,command=switch)
            register_button.place(x=95,y=50)
            register_win.mainloop()

        create_submit=ctk.CTkButton(master=creation,width=220,text="Register",corner_radius=6,command=register,state="disabled")
        create_submit.place(x=180,y=500)

        def clear():
            creation.destroy()
            login.deiconify()
        creation.protocol('WM_DELETE_WINDOW',clear)

        creation.mainloop()

    log_frame=ctk.CTkFrame(master=login, width=320, height=360, corner_radius=15,border_width=2, border_color="black")
    log_frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

    l1=ctk.CTkLabel(master=log_frame,text="Sign-in", font=('Century Gothic',28,"bold"))
    l1.place(x=50,y=45)

    mail_entery=ctk.CTkEntry(master=log_frame,width=220,placeholder_text="Email")
    mail_entery.place(x=50,y=110)

    masterpass_entery=ctk.CTkEntry(master=log_frame,width=220,placeholder_text="Master Password",show="*")
    masterpass_entery.place(x=50,y=160)

    #passwd show/hide
    def show_pass():
        global show_pass_flag
        if show_pass_flag==0:
            masterpass_entery.configure(show='')
            show_pass_flag+=1
        else:
            masterpass_entery.configure(show='*')
            show_pass_flag-=1

    view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
    view=ctk.CTkButton(master=log_frame,image=view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:show_pass())
    view.place(x=239,y=162)

    def forgot_password():
        cust_mail=mail_entery.get()
        h=hashlib.new("SHA256")
        h.update(cust_mail.encode())
        check_email=h.hexdigest()
        pattern=re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}")
        if pattern.match(cust_mail):
            login.iconify()
            my_con.execute("Select count(*) from user_info where email='{}'".format(check_email))
            for mail_exists in my_con:
                    if mail_exists[0]==1:
                        otp=""
                        for i in range(6):
                            otp+=str(random.randint(0,9))
                        #mailing OTP
                        server=smtplib.SMTP("smtp.gmail.com",587)
                        server.starttls()
                        server.login('','')#first parameter is the gmail id through which email is to be sent and second is the google app password for the id
                        mail_msg="Your SafePassX email verification OTP is "+otp+'.'
                        server.sendmail("",cust_mail,mail_msg)#first parameter is the gmail id through which email is to be sent
                        server.quit()
                        #print(otp)
                        mail_verify=ctk.CTkToplevel(login)
                        mail_verify.title("Email Verfication")
                        mail_verify.geometry("250x135")
                
                        mail_verify_label=ctk.CTkLabel(master=mail_verify,text="Enter OTP To Verify",font=('Century Gothic',20,"bold"))
                        mail_verify_label.place(x=35,y=10)
                        mail_verify_entery_var=ctk.StringVar()
                        mail_verify_entery=ctk.CTkEntry(master=mail_verify,textvariable=mail_verify_entery_var,width=100,justify='center',font=('Century Gothic',20,"bold"))
                        mail_verify_entery.place(x=75,y=50)
                        def email_otp_verify():
                            mail_verify.destroy()
                            if mail_verify_entery_var.get()==otp:
                                reset_win=ctk.CTkToplevel(login)
                                reset_win.title("Reset Password")
                                reset_win.geometry("520x300")
                                reset_title=ctk.CTkLabel(master=reset_win,text="Reset Password",font=('Century Gothic',30,"bold"),text_color="green")
                                reset_title.place(x=10,y=5)
                                newpass=ctk.CTkLabel(master=reset_win,text="Create New:",font=('Century Gothic',20,"bold"))
                                newpass.place(x=10,y=50)
                                newpass_entery_var=ctk.StringVar()
                                newpass_entery=ctk.CTkEntry(master=reset_win,textvariable=newpass_entery_var,width=220,show="*")
                                newpass_entery.place(x=135,y=50)
                                def verify_new_masterpass():
                                    verify_create_masterpass_flag=0
                                    cust_create_masterpass=newpass_entery_var.get()
                                    if len(cust_create_masterpass)>=12:
                                        verify_create_masterpass_flag+=1
                                    for i in cust_create_masterpass:
                                        if i.isupper():
                                            verify_create_masterpass_flag+=1
                                            break
                                    for i in cust_create_masterpass:
                                        if i in "0123456789":
                                            verify_create_masterpass_flag+=1
                                            break
                                    for i in cust_create_masterpass:
                                        l=['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}',']','|','',':',';','"',"'",'<',',','>','.','?','/','\\']
                                        if i in l:
                                            verify_create_masterpass_flag+=1
                                            break
                                    reset_win.iconify()
                                    if verify_create_masterpass_flag==4:
                                        create_masterpass_verified_win=ctk.CTkToplevel(reset_win)
                                        create_masterpass_verified_win.title("Masterpass Accepted")
                                        create_masterpass_verified_win.geometry("290x100")
                                        create_masterpass_verified_label=ctk.CTkLabel(master=create_masterpass_verified_win,text="MasterPassword Accepted",font=('Century Gothic',20,"bold"))
                                        create_masterpass_verified_label.place(x=16,y=5)
                                        def switch():
                                            create_masterpass_verified_win.destroy()
                                            reset_win.deiconify()
                                            newpass_create_checkbox.configure(variable=var1)
                                            newpass_entery.configure(state="disabled")
                                            new_button.configure(state="disabled")
                                            new_view.configure(state="disabled")
                                            newpass_confirm_entery.configure(state="normal")
                                            newpass_confirm_button.configure(state="normal")
                                        create_masterpass_verified_button=ctk.CTkButton(master=create_masterpass_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                        create_masterpass_verified_button.place(x=95,y=50)
                                        create_masterpass_verified_win.mainloop()
                                    else:
                                        create_masterpass_failed_win=ctk.CTkToplevel(reset_win)
                                        create_masterpass_failed_win.title("Masterpass Rejected")
                                        create_masterpass_failed_win.geometry("290x100")
                                        create_masterpass_failed_label=ctk.CTkLabel(master=create_masterpass_failed_win,text="MasterPassword Rejected",font=('Century Gothic',20,"bold"))
                                        create_masterpass_failed_label.place(x=20,y=5)
                                        def switch():
                                            create_masterpass_failed_win.destroy()
                                            reset_win.deiconify()
                                            newpass_entery.delete(0,"end")
                                        create_masterpass_failed_button=ctk.CTkButton(master=create_masterpass_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                        create_masterpass_failed_button.place(x=95,y=50)
                                        create_masterpass_failed_win.mainloop()

                                #passwd show/hide
                                def new_show_pass():
                                    global new_show_pass_flag
                                    if new_show_pass_flag==0:
                                        newpass_entery.configure(show='')
                                        new_show_pass_flag+=1
                                    else:
                                        newpass_entery.configure(show='*')
                                        new_show_pass_flag-=1
                                new_view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
                                new_view=ctk.CTkButton(master=reset_win,image=new_view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:new_show_pass())
                                new_view.place(x=320,y=53)
                                new_button=ctk.CTkButton(master=reset_win,text="Verify",width=50,corner_radius=6,command=verify_new_masterpass)
                                new_button.place(x=360,y=50)
                                var1=ctk.StringVar(value="on")
                                var2=ctk.StringVar(value="off")
                                newpass_create_checkbox=ctk.CTkCheckBox(master=reset_win,text="",variable=var2,onvalue="on",offvalue="off",state="disabled")
                                newpass_create_checkbox.place(x=450,y=50)
                                
                                newpass_req1=ctk.CTkLabel(master=reset_win,text="* Atleast 12 characters",font=('Century Gothic',18,"bold"),text_color="green")
                                newpass_req1.place(x=10,y=80)
                                newpass_req2=ctk.CTkLabel(master=reset_win,text="* Atleast 1 uppercase letter",font=('Century Gothic',18,"bold"),text_color="green")
                                newpass_req2.place(x=10,y=110)
                                newpass_req3=ctk.CTkLabel(master=reset_win,text="* Atleast 1 number",font=('Century Gothic',18,"bold"),text_color="green")
                                newpass_req3.place(x=10,y=140)
                                newpass_req4=ctk.CTkLabel(master=reset_win,text="* Atleast 1 symbol",font=('Century Gothic',18,"bold"),text_color="green")
                                newpass_req4.place(x=10,y=170)

                                newpass_confirm=ctk.CTkLabel(master=reset_win,text="Confirm:",font=('Century Gothic',20,"bold"))
                                newpass_confirm.place(x=30,y=210)
                                newpass_confirm_entery_var=ctk.StringVar()
                                newpass_confirm_entery=ctk.CTkEntry(master=reset_win,textvariable=newpass_confirm_entery_var,width=220,show="*",state="disabled")
                                newpass_confirm_entery.place(x=135,y=210)
        
                                def verify_confirm_masterpass():
                                    cust_confirm_masterpass=newpass_confirm_entery_var.get()
                                    cust_create_masterpass=newpass_entery_var.get()
                                    reset_win.iconify()
                                    if cust_confirm_masterpass==cust_create_masterpass:
                                        confirm_masterpass_verified_win=ctk.CTkToplevel(reset_win)
                                        confirm_masterpass_verified_win.title("Confirmation Successful")
                                        confirm_masterpass_verified_win.geometry("290x100")
                                        confirm_masterpass_verified_label=ctk.CTkLabel(master=confirm_masterpass_verified_win,text="Confirmation Successful",font=('Century Gothic',20,"bold"))
                                        confirm_masterpass_verified_label.place(x=27,y=5)
                                        def switch():
                                            confirm_masterpass_verified_win.destroy()
                                            reset_win.deiconify()
                                            newpass_confirm_checkbox.configure(variable=var1)
                                            newpass_confirm_entery.configure(state="disabled")
                                            newpass_confirm_button.configure(state="disabled")
                                            confirm_view.configure(state="disabled")
                                            new_submit.configure(state="normal")
                                        confirm_masterpass_verified_button=ctk.CTkButton(master=confirm_masterpass_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                        confirm_masterpass_verified_button.place(x=95,y=50)
                                        confirm_masterpass_verified_win.mainloop()
                                    else:
                                        confirm_masterpass_failed_win=ctk.CTkToplevel(reset_win)
                                        confirm_masterpass_failed_win.title("Confirmation Failed")
                                        confirm_masterpass_failed_win.geometry("290x100")
                                        confirm_masterpass_failed_label=ctk.CTkLabel(master=confirm_masterpass_failed_win,text="Confirmation Failed",font=('Century Gothic',20,"bold"))
                                        confirm_masterpass_failed_label.place(x=50,y=5)
                                        def switch():
                                            confirm_masterpass_failed_win.destroy()
                                            reset_win.deiconify()
                                            newpass_create_checkbox.configure(variable=var2)
                                            newpass_entery.configure(state="normal")
                                            new_button.configure(state="normal")
                                            newpass_entery.delete(0,"end")
                                            newpass_confirm_entery.delete(0,"end")
                                            newpass_confirm_entery.configure(state="disabled")
                                            newpass_confirm_button.configure(state="disabled")
                                        new_view.configure(state="normal")
                                        confirm_masterpass_failed_button=ctk.CTkButton(master=confirm_masterpass_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                        confirm_masterpass_failed_button.place(x=95,y=50)
                                        confirm_masterpass_failed_win.mainloop()

                                #passwd show/hide
                                def confirm_show_pass():
                                    global new_confirm_show_pass_flag
                                    if new_confirm_show_pass_flag==0:
                                        newpass_confirm_entery.configure(show='')
                                        new_confirm_show_pass_flag+=1
                                    else:
                                        newpass_confirm_entery.configure(show='*')
                                        new_confirm_show_pass_flag-=1
                                confirm_view_img=ctk.CTkImage(Image.open("input/view.jpg"),size=(18,13))
                                confirm_view=ctk.CTkButton(master=reset_win,image=confirm_view_img,text="",fg_color="white",width=1,height=1,corner_radius=6,command=lambda:confirm_show_pass())
                                confirm_view.place(x=320,y=213)
                                newpass_confirm_button=ctk.CTkButton(master=reset_win,text="Verify",width=50,corner_radius=6,command=verify_confirm_masterpass,state="disabled")
                                newpass_confirm_button.place(x=360,y=210)
                                newpass_confirm_checkbox=ctk.CTkCheckBox(master=reset_win,text="",variable=var2,onvalue="on",offvalue="off",state="disabled")
                                newpass_confirm_checkbox.place(x=450,y=210)

                                def reset():
                                    reset_win.destroy()
                                    cust_masterpass=newpass_entery_var.get()

                                    h=hashlib.new("SHA256")
                                    h.update(cust_masterpass.encode())
                                    sql_pass=h.hexdigest()

                                    my_con.execute("Update user_info set masterpass='{}' where email='{}'".format(sql_pass,check_email))
                                    sql.commit()

                                    pass_reset_win=ctk.CTkToplevel(login)
                                    pass_reset_win.title("Reset Successful")
                                    pass_reset_win.geometry("290x100")
                                    register_label=ctk.CTkLabel(master=pass_reset_win,text="Reset Successful",font=('Century Gothic',20,"bold"))
                                    register_label.place(x=67,y=5)
                                    def switch():
                                        pass_reset_win.destroy()
                                        login.deiconify()
                                    register_button=ctk.CTkButton(master=pass_reset_win,text="Sign-in",width=100,corner_radius=6,command=switch)
                                    register_button.place(x=95,y=50)
                                    pass_reset_win.mainloop()
                                
                                new_submit=ctk.CTkButton(master=reset_win,width=100,text="Reset",corner_radius=6,command=reset,state="disabled")
                                new_submit.place(x=200,y=255)

                                reset_win.mainloop()

                            else:
                                mail_failed_win=ctk.CTkToplevel(login)
                                mail_failed_win.title("Verification Failed")
                                mail_failed_win.geometry("230x100")
                                mail_failed_label=ctk.CTkLabel(master=mail_failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                                mail_failed_label.place(x=26,y=5)
                                def switch():
                                    mail_failed_win.destroy()
                                    login.deiconify()
                                mail_failed_button=ctk.CTkButton(master=mail_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                mail_failed_button.place(x=65,y=50)
                                mail_failed_win.mainloop()
                        mail_verify_button=ctk.CTkButton(master=mail_verify,text="Verify",width=50,corner_radius=6,command=email_otp_verify)
                        mail_verify_button.place(x=100,y=95)
                
                        def timeup():
                            if mail_verify.winfo_exists()==1:
                                mail_verify.destroy()
                                timeup_win=ctk.CTkToplevel(login)
                                timeup_win.title("Time Exceeded")
                                timeup_win.geometry("230x100")
                                timeup_label=ctk.CTkLabel(master=timeup_win,text="Time Limit Exceeded",font=('Century Gothic',20,"bold"))
                                timeup_label.place(x=17,y=5)
                                def switch():
                                    timeup_win.destroy()
                                    login.deiconify()
                                timeup_button=ctk.CTkButton(master=timeup_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                timeup_button.place(x=65,y=50)
                                timeup_win.mainloop()
                        mail_verify.after(60000,lambda:timeup())

                        def clear():
                            mail_verify.destroy()
                            login.deiconify()
                        mail_verify.protocol('WM_DELETE_WINDOW',clear)

                        mail_verify.mainloop()
                    else:
                        mail_unregistered_win=ctk.CTkToplevel(login)
                        mail_unregistered_win.title("Email Not-Found")
                        mail_unregistered_win.geometry("290x100")
                        mail_unregistered_label=ctk.CTkLabel(master=mail_unregistered_win,text="Email Not Registered",font=('Century Gothic',20,"bold"))
                        mail_unregistered_label.place(x=45,y=5)
                        def switch():
                            mail_unregistered_win.destroy()
                            login.deiconify()
                            mail_entery.delete(0,'end')
                            masterpass_entery.delete(0,'end')
                        mail_unregistered_button=ctk.CTkButton(master=mail_unregistered_win,text="OK",width=100,corner_radius=6,command=switch)
                        mail_unregistered_button.place(x=95,y=50)
                        mail_unregistered_win.mainloop()

    l2=ctk.CTkLabel(master=log_frame,text="Forgot Password?",font=('Century Gothic',12,"bold"),text_color="green")
    l2.place(x=167,y=190)
    l2.bind('<Button>',lambda e:forgot_password())

    def login_command():
        global global_mail
        global_mail=mail_entery.get()
        h=hashlib.new("SHA256")
        h.update(global_mail.encode())
        check_email=h.hexdigest()
        pattern=re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}")
        if pattern.match(global_mail):
            my_con.execute("Select count(*) from user_info where email='{}'".format(check_email))
            for mail_exists in my_con:
                    if mail_exists[0]==1:
                        my_con.execute("Select status from user_info where email='{}'".format(check_email))
                        for status in my_con:
                            if status[0]==0:
                                login.iconify()
                                account_locked_win=ctk.CTkToplevel(login)
                                account_locked_win.title("Account Locked")
                                account_locked_win.geometry("305x100")
                                account_locked_label=ctk.CTkLabel(master=account_locked_win,text="Your account is locked.",font=('Century Gothic',20,"bold"))
                                account_locked_label.place(x=40,y=5)
                                account_locked_label=ctk.CTkLabel(master=account_locked_win,text="Verify through email to unlock.",font=('Century Gothic',20,"bold"))
                                account_locked_label.place(x=5,y=30)
                                def switch():
                                    account_locked_win.destroy()
                                    otp=""
                                    for i in range(6):
                                        otp+=str(random.randint(0,9))
                                    #mailing OTP
                                    server=smtplib.SMTP("smtp.gmail.com",587)
                                    server.starttls()
                                    server.login('','')#first parameter is the gmail id through which email is to be sent and second is the google app password for the id
                                    mail_msg="Your SafePassX email verification OTP is "+otp+'.'
                                    server.sendmail("",global_mail,mail_msg)#first parameter is the gmail id through which email is to be sent
                                    server.quit()
                                    #print(otp)
                                    mail_verify=ctk.CTkToplevel(login)
                                    mail_verify.title("Email Verfication")
                                    mail_verify.geometry("250x135")

                                    mail_verify_label=ctk.CTkLabel(master=mail_verify,text="Enter OTP To Verify",font=('Century Gothic',20,"bold"))
                                    mail_verify_label.place(x=35,y=10)
                                    mail_verify_entery_var=ctk.StringVar()
                                    mail_verify_entery=ctk.CTkEntry(master=mail_verify,textvariable=mail_verify_entery_var,width=100,justify='center',font=('Century Gothic',20,"bold"))
                                    mail_verify_entery.place(x=75,y=50)
                                    def email_otp_verify():
                                        mail_verify.destroy()
                                        if mail_verify_entery_var.get()==otp:
                                            mail_verified_win=ctk.CTkToplevel(login)
                                            mail_verified_win.title("Verification Successful")
                                            mail_verified_win.geometry("250x100")
                                            mail_verified_label=ctk.CTkLabel(master=mail_verified_win,text="Account Is Unlocked.",font=('Century Gothic',20,"bold"))
                                            mail_verified_label.place(x=23,y=5)
                                            def switch():
                                                mail_verified_win.destroy()
                                                my_con.execute("Update user_info set status=1 where email='{}'".format(check_email))
                                                sql.commit()
                                                login.deiconify()
                                            mail_verified_button=ctk.CTkButton(master=mail_verified_win,text="OK",width=100,corner_radius=6,command=switch)
                                            mail_verified_button.place(x=75,y=50)
                                            mail_verified_win.mainloop()
                                        else:
                                            mail_failed_win=ctk.CTkToplevel(login)
                                            mail_failed_win.title("Verifaction Failed")
                                            mail_failed_win.geometry("230x100")
                                            mail_failed_label=ctk.CTkLabel(master=mail_failed_win,text="Verification Failed",font=('Century Gothic',20,"bold"))
                                            mail_failed_label.place(x=26,y=5)
                                            def switch():
                                                mail_failed_win.destroy()
                                                login.deiconify()
                                                mail_entery.delete(0,'end')
                                                masterpass_entery.delete(0,'end')
                                            mail_failed_button=ctk.CTkButton(master=mail_failed_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                            mail_failed_button.place(x=65,y=50)
                                            mail_failed_win.mainloop()
                                    mail_verify_button=ctk.CTkButton(master=mail_verify,text="Verify",width=50,corner_radius=6,command=email_otp_verify)
                                    mail_verify_button.place(x=100,y=95)

                                    def timeup():
                                        if mail_verify.winfo_exists()==1:
                                            mail_verify.destroy()
                                            timeup_win=ctk.CTkToplevel(login)
                                            timeup_win.title("Time Exceeded")
                                            timeup_win.geometry("230x100")
                                            timeup_label=ctk.CTkLabel(master=timeup_win,text="Time Limit Exceeded",font=('Century Gothic',20,"bold"))
                                            timeup_label.place(x=17,y=5)
                                            def switch():
                                                timeup_win.destroy()
                                                login.deiconify()
                                                mail_entery.delete(0,'end')
                                                masterpass_entery.delete(0,'end')
                                            timeup_button=ctk.CTkButton(master=timeup_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                            timeup_button.place(x=65,y=50)
                                            timeup_win.mainloop()
                                    mail_verify.after(60000,lambda:timeup())

                                    mail_verify.mainloop()
                                account_locked_button=ctk.CTkButton(master=account_locked_win,text="Verify",width=100,corner_radius=6,command=switch)
                                account_locked_button.place(x=100,y=65)
                                account_locked_win.mainloop()
                            else:
                                global global_pass
                                global_pass=masterpass_entery.get()
                                if len(global_pass)>=12:
                                    h=hashlib.new("SHA256")
                                    h.update(global_pass.encode())
                                    check_pass=h.hexdigest()
                                    my_con.execute("Select masterpass from user_info where email='{}'".format(check_email))
                                    for masterpass in my_con:
                                        if masterpass[0]==check_pass:
                                            login.destroy()
                                            my_con.execute("Update user_info set status=1 where email='{}'".format(check_email))
                                            sql.commit()
                                            main_application()
                                        else:
                                            my_con.execute("Select status from user_info where email='{}'".format(check_email))
                                            for status in my_con:
                                                if status[0]==1:
                                                    my_con.execute("Update user_info set status=2 where email='{}'".format(check_email))
                                                    login.iconify()
                                                    account_1_win=ctk.CTkToplevel(login)
                                                    account_1_win.title("Account Locked")
                                                    account_1_win.geometry("305x100")
                                                    account_1_label=ctk.CTkLabel(master=account_1_win,text="Incorrect Password",font=('Century Gothic',20,"bold"))
                                                    account_1_label.place(x=60,y=5)
                                                    account_1_label=ctk.CTkLabel(master=account_1_win,text="You have 2 more tries left.",font=('Century Gothic',20,"bold"))
                                                    account_1_label.place(x=25,y=30)
                                                    def switch():
                                                        account_1_win.destroy()
                                                        login.deiconify()
                                                        masterpass_entery.delete(0,'end')
                                                    account_1_button=ctk.CTkButton(master=account_1_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                                    account_1_button.place(x=100,y=65)
                                                    account_1_win.mainloop()
                                                elif status[0]==2:
                                                    my_con.execute("Update user_info set status=3 where email='{}'".format(check_email))
                                                    login.iconify()
                                                    account_2_win=ctk.CTkToplevel(login)
                                                    account_2_win.title("Account Locked")
                                                    account_2_win.geometry("305x100")
                                                    account_2_label=ctk.CTkLabel(master=account_2_win,text="Incorrect Password",font=('Century Gothic',20,"bold"))
                                                    account_2_label.place(x=60,y=5)
                                                    account_2_label=ctk.CTkLabel(master=account_2_win,text="You have 1 more try left.",font=('Century Gothic',20,"bold"))
                                                    account_2_label.place(x=35,y=30)
                                                    def switch():
                                                        account_2_win.destroy()
                                                        login.deiconify()
                                                        masterpass_entery.delete(0,'end')
                                                    account_2_button=ctk.CTkButton(master=account_2_win,text="Try Again",width=100,corner_radius=6,command=switch)
                                                    account_2_button.place(x=100,y=65)
                                                    account_2_win.mainloop()
                                                elif status[0]==3:
                                                    my_con.execute("Update user_info set status=0 where email='{}'".format(check_email))
                                                    sql.commit()
                                                    login.iconify()
                                                    account_locked_win=ctk.CTkToplevel(login)
                                                    account_locked_win.title("Account Locked")
                                                    account_locked_win.geometry("305x100")
                                                    account_locked_label=ctk.CTkLabel(master=account_locked_win,text="Incorrect Password",font=('Century Gothic',20,"bold"))
                                                    account_locked_label.place(x=60,y=5)
                                                    account_locked_label=ctk.CTkLabel(master=account_locked_win,text="Your account is locked.",font=('Century Gothic',20,"bold"))
                                                    account_locked_label.place(x=40,y=30)
                                                    def switch():
                                                        account_locked_win.destroy()
                                                        login.deiconify()
                                                        masterpass_entery.delete(0,'end')
                                                        mail_entery.delete(0,'end')
                                                    account_locked_button=ctk.CTkButton(master=account_locked_win,text="OK",width=100,corner_radius=6,command=switch)
                                                    account_locked_button.place(x=100,y=65)
                                                    account_locked_win.mainloop()
                    else:
                        login.iconify()
                        mail_unregistered_win=ctk.CTkToplevel(login)
                        mail_unregistered_win.title("Email Not-Found")
                        mail_unregistered_win.geometry("290x100")
                        mail_unregistered_label=ctk.CTkLabel(master=mail_unregistered_win,text="Email Not Registered",font=('Century Gothic',20,"bold"))
                        mail_unregistered_label.place(x=45,y=5)
                        def switch():
                            mail_unregistered_win.destroy()
                            login.deiconify()
                            mail_entery.delete(0,'end')
                            masterpass_entery.delete(0,'end')
                        mail_unregistered_button=ctk.CTkButton(master=mail_unregistered_win,text="OK",width=100,corner_radius=6,command=switch)
                        mail_unregistered_button.place(x=95,y=50)
                        mail_unregistered_win.mainloop()

    login_button=ctk.CTkButton(master=log_frame,width=220,text="Login",corner_radius=6,command=login_command)
    login_button.place(x=50,y=240)

    l3=ctk.CTkLabel(master=log_frame,text="Don't have an account?", font=('Century Gothic',15,"bold"))
    l3.place(x=28,y=290)

    l4=ctk.CTkLabel(master=log_frame,text="Create One.", font=('Century Gothic',15,"bold"),text_color="green")
    l4.place(x=208,y=290)
    l4.bind('<Button>',lambda e:create_one())

    login.mainloop()
sign_in()