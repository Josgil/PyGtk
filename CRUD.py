#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MySQLdb

#Damos valor a los datos de conexión
DB_Host = "localhost"
DB_Usuario = "josgil"
DB_Pass = "josgil"
DB_Nombre = "Agenda"

#Conectar a la Base de Datos (DB)
Conexion = MySQLdb.connect(DB_Host, DB_Usuario, DB_Pass, DB_Nombre)
micursor = Conexion.cursor(MySQLdb.cursors.DictCursor)

#Asignamos los datos necesarios para luego incluir datos MySQl
I = "INSERT INTO Personas (Id,Nombre,Apellidos,Telefono,Mail) Values('" #Insert
S = "','" #Separador
SN1 = "',"
SN2 = ",'"
F = "')" #Final


class GUI(Gtk.Window):
    """Clase principal"""
    builder = None

    def __init__(self):
        """Definición de inicio"""
        #Iniciamos el GTK Builder para que funcione glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interfaz1.glade")
        self.handlers = {"onDeleteWindow": self.onDeleteWindow,
                        "onButtonPressed": self.onButtonPressed,
                        "onButtonPressedObtener": self.onButtonPressedObtener,
                        "onAboutDialog": self.onAboutDialog,
                        "onCloseAbout": self.onCloseAbout}

        #Conectamos las señales e iniciamos la aplicaciones
        self.builder.connect_signals(self.handlers)
        self.window = self.builder.get_object("window1")
        #self.button1 = self.builder.get_objet("button1")
        self.window.connect("delete-event", Gtk.main_quit)
        self.about = self.builder.get_object("aboutdialog1")
        self.window.show_all()

    def onAboutDialog(self, *args):
        self.about.show_all()

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def CreateTable(self, button):
        nueva_tabla = ("""CREATE TABLE Personas (
            Id INT,
            Nombre CHAR(20),
            Apellido CHAR(20),
            Telefono INT(9),
            mail CHAR(20))""")
        micursor.execute(nueva_tabla)

    def onButtonPressed(self, window):
        entry1 = self.builder.get_object("entry1")
        entry2 = self.builder.get_object("entry2")
        entry3 = self.builder.get_object("entry3")
        entry4 = self.builder.get_object("entry4")
        entry5 = self.builder.get_object("entry5")

        entry1.get_text()
        entry2.get_text()
        entry3.get_text()
        entry4.get_text()
        entry5.get_text()

        text1 = entry1.get_text()
        text2 = entry2.get_text()
        text3 = entry3.get_text()
        text4 = entry4.get_text()
        text5 = entry5.get_text()

        query = (I + text1 + S + text2 + S + text3 + SN1 + text4 + SN2 + text5 + F)
        print query
        micursor.execute(query)
        Conexion.commit()

        print "El ID " + text1 + "se llama " + text2 + text3
        print "su teléfono es el " + text4 + " y su mail: " + text5

    def onButtonPressedObtener(self, button):
        entry1 = self.builder.get_object("entry1")
        entry2 = self.builder.get_object("entry2")
        entry3 = self.builder.get_object("entry3")
        entry4 = self.builder.get_object("entry4")
        entry5 = self.builder.get_object("entry5")

        entry1.get_text()
        text1 = entry1.get_text()
        Campos = "id, Nombre, Apellidos, Telefono, Mail"
        query = "SELECT " + Campos + " FROM Personas WHERE id=" + text1 + ";"
        micursor.execute(query)
        registros = micursor.fetchall()

        for registro in registros:
            entry2.set_text(registro["Nombre"])
            entry3.set_text(registro["Apellidos"])
            entry4.set_text(str(registro["Telefono"]))
            entry5.set_text(registro["Mail"])

    def onButtonPressedActualizar(self, button):
        entry1 = self.builder.get_object("entry1")
        entry2 = self.builder.get_object("entry2")
        entry3 = self.builder.get_object("entry3")
        entry4 = self.builder.get_object("entry4")
        entry5 = self.builder.get_object("entry5")

        entry1.get_text()
        entry2.get_text()
        entry3.get_text()
        entry4.get_text()
        entry5.get_text()

        text1 = entry1.get_text()
        text2 = entry2.get_text()
        text3 = entry3.get_text()
        text4 = entry4.get_text()
        text5 = entry5.get_text()

        Actualizar = ("Nombre = '" + text2 + "', Apellidos = '" + text3 +
        "', Telefono = '" + text4 + "', Mail = '" + text5 + "'")
        print Actualizar
        query = "UPDATE Personas SET " + Actualizar + " WHERE id=" + text1 + ";"
        print query
        micursor.execute(query)
        Conexion.commit()

    def onCloseAbout(self, *args):
        self.about.hide()

def main():
    window = GUI()
    Gtk.main()
    return 0

if __name__ == "__main__":
    main()
