<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, session, redirect, send_file
import psycopg2
import smtplib
import os
import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "esma_secret"

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

# ===== PRODUCTOS =====
productos = {
    "Bebidas": {"Producto 1":1,"Producto 2":1},
    "Comida rápida": {"Producto 3":1,"Producto 4":1},
    "Snacks": {"Producto 5":1},
    "Dulces": {"Producto 6":1},
    "Otros": {"Producto 7":1}
}

# ===== DB =====
def get_conn():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS compras(
        id SERIAL PRIMARY KEY,
        nombre TEXT,
        correo TEXT,
        producto TEXT,
        cantidad INTEGER,
        total REAL,
        fecha TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id SERIAL PRIMARY KEY,
        usuario TEXT,
        password TEXT
    )""")

    c.execute("SELECT * FROM admin")
    if not c.fetchone():
        c.execute("INSERT INTO admin VALUES (DEFAULT,'admin','1234')")

    conn.commit()
    conn.close()

init_db()

# ===== EMAIL =====
def enviar_email(destino,nombre,producto,cantidad,total,total_dia,total_acumulado,fecha):
    html=f"""
    <h2>Bar de Cadetes</h2>
    <p>{nombre}</p>
    <p>{producto} x{cantidad}</p>
    <p>Compra: ${total}</p>
    <p>Hoy: ${total_dia}</p>
    <p>Acumulado: ${total_acumulado}</p>
    """
    msg=MIMEMultipart()
    msg["From"]=EMAIL_USER
    msg["To"]=destino
    msg["Subject"]="Compra ESMA"
    msg.attach(MIMEText(html,"html"))

    s=smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    s.login(EMAIL_USER,EMAIL_PASS)
    s.send_message(msg)
    s.quit()

# ===== AUTOCOMPLETE =====
@app.route("/get_cliente/<nombre>")
def get_cliente(nombre):
    conn=get_conn()
    c=conn.cursor()
    c.execute("SELECT correo FROM compras WHERE nombre=%s ORDER BY id DESC LIMIT 1",(nombre,))
    r=c.fetchone()
    conn.close()
    return jsonify({"correo":r[0] if r else ""})

# ===== HOME =====
@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        nombre=request.form["cliente"]
        correo=request.form["correo"]
        producto=request.form["producto"]
        cantidad=int(request.form["cantidad"])
        precio=float(request.form["precio"])
        fecha=datetime.now().strftime("%Y-%m-%d")

        total=cantidad*precio

        conn=get_conn()
        c=conn.cursor()

        c.execute("INSERT INTO compras(nombre,correo,producto,cantidad,total,fecha) VALUES(%s,%s,%s,%s,%s,%s)",
        (nombre,correo,producto,cantidad,total,fecha))
        conn.commit()

        c.execute("SELECT SUM(total) FROM compras WHERE nombre=%s AND fecha=%s",(nombre,fecha))
        total_dia=c.fetchone()[0] or 0

        c.execute("SELECT SUM(total) FROM compras WHERE nombre=%s",(nombre,))
        total_acumulado=c.fetchone()[0] or 0

        conn.close()

        enviar_email(correo,nombre,producto,cantidad,total,total_dia,total_acumulado,fecha)

    return render_template("index.html",productos=productos)

# ===== LOGIN =====
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        user=request.form["user"]
        pw=request.form["pass"]

        conn=get_conn()
        c=conn.cursor()
        c.execute("SELECT * FROM admin WHERE usuario=%s AND password=%s",(user,pw))
        if c.fetchone():
            session["admin"]=True
            return redirect("/admin")

    return render_template("login.html")

# ===== ADMIN =====
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    inicio=request.args.get("inicio") or datetime.now().strftime("%Y-%m-01")
    fin=request.args.get("fin") or datetime.now().strftime("%Y-%m-%d")

    conn=get_conn()
    c=conn.cursor()

    c.execute("SELECT nombre,SUM(total) FROM compras WHERE fecha BETWEEN %s AND %s GROUP BY nombre ORDER BY SUM(total) DESC",(inicio,fin))
    datos=c.fetchall()

    c.execute("SELECT fecha,SUM(total) FROM compras WHERE fecha BETWEEN %s AND %s GROUP BY fecha ORDER BY fecha",(inicio,fin))
    stats=c.fetchall()

    fechas=[x[0] for x in stats]
    totales=[float(x[1]) for x in stats]

    c.execute("SELECT producto,SUM(cantidad) FROM compras GROUP BY producto ORDER BY SUM(cantidad) DESC LIMIT 5")
    top=c.fetchall()

    conn.close()

    return render_template("admin.html",datos=datos,fechas=fechas,totales=totales,top_productos=top)

# ===== EXPORT =====
@app.route("/exportar")
def exportar():
    if not session.get("admin"):
        return redirect("/login")

    conn=get_conn()
    df=pd.read_sql("SELECT * FROM compras",conn)
    conn.close()
    df.to_excel("reporte.xlsx",index=False)
    return send_file("reporte.xlsx",as_attachment=True)

# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===== RUN =====
if __name__=="__main__":
=======
from flask import Flask, render_template, request, jsonify, session, redirect, send_file
import psycopg2
import smtplib
import os
import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "esma_secret"

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

# ===== PRODUCTOS =====
productos = {
    "Bebidas": {"Producto 1":1,"Producto 2":1},
    "Comida rápida": {"Producto 3":1,"Producto 4":1},
    "Snacks": {"Producto 5":1},
    "Dulces": {"Producto 6":1},
    "Otros": {"Producto 7":1}
}

# ===== DB =====
def get_conn():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS compras(
        id SERIAL PRIMARY KEY,
        nombre TEXT,
        correo TEXT,
        producto TEXT,
        cantidad INTEGER,
        total REAL,
        fecha TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id SERIAL PRIMARY KEY,
        usuario TEXT,
        password TEXT
    )""")

    c.execute("SELECT * FROM admin")
    if not c.fetchone():
        c.execute("INSERT INTO admin VALUES (DEFAULT,'admin','1234')")

    conn.commit()
    conn.close()

init_db()

# ===== EMAIL =====
def enviar_email(destino,nombre,producto,cantidad,total,total_dia,total_acumulado,fecha):
    html=f"""
    <h2>Bar de Cadetes</h2>
    <p>{nombre}</p>
    <p>{producto} x{cantidad}</p>
    <p>Compra: ${total}</p>
    <p>Hoy: ${total_dia}</p>
    <p>Acumulado: ${total_acumulado}</p>
    """
    msg=MIMEMultipart()
    msg["From"]=EMAIL_USER
    msg["To"]=destino
    msg["Subject"]="Compra ESMA"
    msg.attach(MIMEText(html,"html"))

    s=smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    s.login(EMAIL_USER,EMAIL_PASS)
    s.send_message(msg)
    s.quit()

# ===== AUTOCOMPLETE =====
@app.route("/get_cliente/<nombre>")
def get_cliente(nombre):
    conn=get_conn()
    c=conn.cursor()
    c.execute("SELECT correo FROM compras WHERE nombre=%s ORDER BY id DESC LIMIT 1",(nombre,))
    r=c.fetchone()
    conn.close()
    return jsonify({"correo":r[0] if r else ""})

# ===== HOME =====
@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        nombre=request.form["cliente"]
        correo=request.form["correo"]
        producto=request.form["producto"]
        cantidad=int(request.form["cantidad"])
        precio=float(request.form["precio"])
        fecha=datetime.now().strftime("%Y-%m-%d")

        total=cantidad*precio

        conn=get_conn()
        c=conn.cursor()

        c.execute("INSERT INTO compras(nombre,correo,producto,cantidad,total,fecha) VALUES(%s,%s,%s,%s,%s,%s)",
        (nombre,correo,producto,cantidad,total,fecha))
        conn.commit()

        c.execute("SELECT SUM(total) FROM compras WHERE nombre=%s AND fecha=%s",(nombre,fecha))
        total_dia=c.fetchone()[0] or 0

        c.execute("SELECT SUM(total) FROM compras WHERE nombre=%s",(nombre,))
        total_acumulado=c.fetchone()[0] or 0

        conn.close()

        enviar_email(correo,nombre,producto,cantidad,total,total_dia,total_acumulado,fecha)

    return render_template("index.html",productos=productos)

# ===== LOGIN =====
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        user=request.form["user"]
        pw=request.form["pass"]

        conn=get_conn()
        c=conn.cursor()
        c.execute("SELECT * FROM admin WHERE usuario=%s AND password=%s",(user,pw))
        if c.fetchone():
            session["admin"]=True
            return redirect("/admin")

    return render_template("login.html")

# ===== ADMIN =====
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    inicio=request.args.get("inicio") or datetime.now().strftime("%Y-%m-01")
    fin=request.args.get("fin") or datetime.now().strftime("%Y-%m-%d")

    conn=get_conn()
    c=conn.cursor()

    c.execute("SELECT nombre,SUM(total) FROM compras WHERE fecha BETWEEN %s AND %s GROUP BY nombre ORDER BY SUM(total) DESC",(inicio,fin))
    datos=c.fetchall()

    c.execute("SELECT fecha,SUM(total) FROM compras WHERE fecha BETWEEN %s AND %s GROUP BY fecha ORDER BY fecha",(inicio,fin))
    stats=c.fetchall()

    fechas=[x[0] for x in stats]
    totales=[float(x[1]) for x in stats]

    c.execute("SELECT producto,SUM(cantidad) FROM compras GROUP BY producto ORDER BY SUM(cantidad) DESC LIMIT 5")
    top=c.fetchall()

    conn.close()

    return render_template("admin.html",datos=datos,fechas=fechas,totales=totales,top_productos=top)

# ===== EXPORT =====
@app.route("/exportar")
def exportar():
    if not session.get("admin"):
        return redirect("/login")

    conn=get_conn()
    df=pd.read_sql("SELECT * FROM compras",conn)
    conn.close()
    df.to_excel("reporte.xlsx",index=False)
    return send_file("reporte.xlsx",as_attachment=True)

# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===== RUN =====
if __name__=="__main__":
>>>>>>> f2241aa1a1180f65013e192308b1329a0d3e25fc
    app.run(host="0.0.0.0",port=10000)