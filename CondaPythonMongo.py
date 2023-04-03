
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId
from tkinter.messagebox import askyesno

#Conexion con la base de datos en este caso atlas 

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_USER="admin"
MONGO_PASSWORD="aaa1234"

DATABASE="Veterinaria"
COLLECTION="MASCOTA"
#mongodb+srv://<username>:<password>@cluster0.e9w0im2.mongodb.net/?retryWrites=true&w=majority

URI="mongodb://"+ MONGO_HOST+":"+ MONGO_PUERTO
#"mongodb+srv://" + MONGO_USER+":"+ MONGO_PASSWORD+ "@cluster0.e9w0im2.mongodb.net/?retryWrites=true&w=majority"



client=pymongo.MongoClient(URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
basedatos=client[DATABASE]
coleccion=basedatos[COLLECTION]
id_mascota=""
print("Conexion a Mongo exitosa")

try:
    client=pymongo.MongoClient(URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    basedatos=client[DATABASE]
    coleccion=basedatos[COLLECTION]
    for documento in coleccion.find():
      print(documento["nombre"]+" "+documento["raza"]+ " "+documento["tipo"])
    client.close()
except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print(errorTiempo)
except pymongo.errors.ConectionFailure as errorConexion:
    print("Fallo al conectarse a mongodb"+ errorConexion)      



def mostrardatos():
    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find():
            tabla.insert('',0,text=documento["_id"],values=(documento["nombre"],documento["raza"],documento["tipo"]))
        #cliente.server_info()
        #print("Conexion a Mongo exitosa")
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo extendido"+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb"+errorConexion)  


def crearRegistro():
    if len(nombre.get())!=0 and len(raza.get())!=0 and len(tipo.get())!=0:
        try:
            documento={"nombre": nombre.get(),"raza":raza.get(),"tipo":tipo.get()} 
            coleccion.insert(documento)
            nombre.delete(0,END)
            raza.delete(0,END)
            tipo.delete(0,END)
        except pymongo.errors.ConectionFailure as error:
             print(error) 
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")                  
    mostrardatos()


def dobleClickTabla(event):
    #Se solicita el campo del texto
    global id_mascota
    id_mascota=str(tabla.item(tabla.selection())["text"])
    #print(id_mascota)
    documento=coleccion.find({"_id":ObjectId(id_mascota)})[0]
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    raza.delete(0,END)
    raza.insert(0,documento["raza"])
    tipo.delete(0,END)
    tipo.insert(0,documento["tipo"])
    crear["state"]="disabled"
    editar["state"]="normal"
    eliminar["state"]="normal"





def editarRegistro():
    documento={"nombre": nombre.get(),"raza":raza.get(),"tipo":tipo.get()} 
    coleccion.update_one({"_id":ObjectId(id_mascota)},{"$set":{"nombre": nombre.get(),"raza":raza.get(),"tipo":tipo.get()}})
    crear["state"]="normal"
    editar["state"]="disabled"
    eliminar["state"]="disabled"


def confirm():
    answer = askyesno(title='confirmation',
                    message='Are you sure that you want to erase this register?')
    if answer:
        TRUE
    else: 
        FALSE  


def eliminarRegistro():
    CONF = confirm()
    #if(confirm()):
    if(CONF == TRUE):
        coleccion.delete_one({"_id":ObjectId(id_mascota)})
        crear["state"]="normal"
        eliminar["state"]="disabled"
        editar["state"]="disabled"
    else:
        return

ventana =Tk()
tabla=ttk.Treeview(ventana,columns=("ID", "NOMBRE","RAZA","TIPO"))
tabla.grid(row=1,column=0,columnspan=4,padx=20,pady=20)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="NOMBRE")
tabla.heading("RAZA",text="RAZA")
tabla.heading("TIPO",text="TIPO")
tabla.bind("<Double-Button-1>",dobleClickTabla)



#nombre
Label(ventana,text="Nombre").grid(row=2,column=0)
nombre=Entry(ventana)
nombre.grid(row=2,column=1)

#tipo
Label(ventana,text="TIPO").grid(row=3,column=0)
tipo=Entry(ventana)
tipo.grid(row=3,column=1)

#raza
Label(ventana,text="RAZA").grid(row=4,column=0)
raza=Entry(ventana)
raza.grid(row=4,column=1)

#Boton Crear

crear=Button(ventana,text="Agregar Mascota",command=crearRegistro,bg="blue",fg="white")
crear.grid(row=5,columnspan=2)

#Boton Editar command -> llama a la funcion 
editar=Button(ventana,text="Editar Mascota",command=editarRegistro,bg="yellow")
editar.grid(row=6,columnspan=2)
editar["state"]="disabled"

#Boton Elinar command -> llama a la funcion 
eliminar=Button(ventana,text="Eliminar Mascota",command=eliminarRegistro,bg="red")
eliminar.grid(row=7,columnspan=2)
eliminar["state"]="disabled"



m = Menu(ventana, tearoff = 0)
m.add_command(label ="Edit")
m.add_command(label ="Erase")
m.add_separator()
m.add_command(label ="Copy")
  
#def do_popup(event):
#    try:
#       m.tk_popup(event.x_root, event.y_root)
#$    finally:
#        m.grab_release()
#  
#ventana. .identify_row.bind("<Button-3>", do_popup)

#grab record values

#temp_label.config(text=selected)

mostrardatos()
ventana.mainloop()

