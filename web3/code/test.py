from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from auth import tampil
from ast import pattern
import mysql.connector
application = Flask(__name__)
application.secret_key = "super secret key"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='watchlist')

@application.route('/')
@application.route('/index')
def index():
    hidden = "hidden"
    if 'loggedin' in session and session['username'] == 'admin':
        return render_template('index.html', hidden="hidden")
    if 'loggedin' in session:
        return render_template('index.html', hidden=hidden, hidden3=hidden)

    return render_template('index.html', hidden3="hidden", hidden2=hidden)



# untuk dashboard
# READ

@application.route('/dashboard')
def dashboard():
    if 'loggedin' in session and session['username'] == 'admin':
        # User is loggedin show them the home page
        return render_template('dashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('index',gagal="gagal"))


# HALAMAN LOGIN
@application.route('/Login', methods=['GET','POST'])
def login():
    
    # Memeriksa apakah "username" dan "password" POST telah di isi (input pengguna)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # memasukkan data form ke variabel agar lebih mudah di akses
        username = request.form['username']
        password = request.form['password']

        # Cek apakah akun ada pada database sql atau tidak
        db = getMysqlConnection()
        cur = db.cursor()
        cur.execute('SELECT * FROM pengguna WHERE username = %s AND password = %s', (username, password,))
        # mengecek apakah sudah ada di database atau belum
        account = cur.fetchone()

        # Jika akun ada pada database tabel pengguna
        if account:
            # Membuat data sesi, data ini dapat diakses di route lain
            session['loggedin'] = True
            session['id'] = account[1]
            session['username'] = account[0]
            # Redirect ke landing page
            hidden = "hidden"
            if 'loggedin' in session and session['username'] == 'admin':
                return render_template('index.html', hidden=hidden)

            return render_template('index.html', hidden=hidden, hidden3=hidden)
        else:
            # Jika akun tidak ada atau username/password salah
            gagal = "username atau password anda salah!!"
            return render_template('login.html', gagal=gagal)
            
    return render_template('login.html')

    

@application.route('/Logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return render_template('index.html', hidden2="hidden")

@application.route('/Register', methods=['GET', 'POST'])
def register():
    msg = ''
    # cek apakah username,password, password2 sudah dikirim melalui POST (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password2' in request.form:
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        db = getMysqlConnection()
        cur = db.cursor()
        cur.execute('SELECT * FROM pengguna WHERE username = %s', (username,))
        account = cur.fetchone()
        # Jika username sudah ada pada database
        if account:
            msg = 'Account already exists!'
        # Jika terdapat kesalahan pada re-type password
        elif password != password2:
            msg = 'Invalid password!'
        # Jika pengguna belum mengisi form username ataupun password
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # jika semua ketentuan sudah terpenuhi
            cur.execute('INSERT INTO pengguna VALUES (%s, %s)', (username, password,))
            db.commit()
            msg = 'You have successfully registered!'  
        
    # Pemberitahuan keterangan 
    return render_template('register.html', keterangan=msg)


@application.route('/Database', methods=['GET','POST'])
def database():
    print(request.method)
    if request.method == "GET":
        db = getMysqlConnection()
        try:
            # Mengambil database siswa
            sqlstr = "SELECT * from siswa"
            cur = db.cursor()
            cur.execute(sqlstr)
            output_siswa = cur.fetchall()
            # Mengambil database orang tua
            sqlstr = "SELECT * from orang_tua"
            cur.execute(sqlstr)
            output_ortu = cur.fetchall()
            # Mengambil database guru
            sqlstr = "SELECT * from guru"
            cur.execute(sqlstr)
            output_guru = cur.fetchall()
            # Mengambil database kelas
            sqlstr = "SELECT * from kelas"
            cur.execute(sqlstr)
            output_kelas = cur.fetchall()
            # Mengambil database mata pelajaran
            sqlstr = "SELECT * from mapel"
            cur.execute(sqlstr)
            output_mapel = cur.fetchall()
            # Mengambil database pengguna
            sqlstr = "SELECT * from pengguna"
            cur.execute(sqlstr)
            output_user = cur.fetchall()
            # Mengambil database Mengajar
            sqlstr = "SELECT * from mengajar"
            cur.execute(sqlstr)
            output_mengajar = cur.fetchall()
            # Mengambil nama guru
            sqlstr = "SELECT nama_guru from guru"
            cur.execute(sqlstr)
            output_namaguru = cur.fetchall()

        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
            return render_template('database.html', datasiswa=output_siswa, dataortu=output_ortu, dataguru=output_guru, datakelas=output_kelas, datamapel=output_mapel, datauser=output_user, datamengajar=output_mengajar, namaguru=output_namaguru)

@application.route('/Database/Orangtua', methods=['GET','POST'])
def databaseOrtu():
    print(request.method)
    if request.method == "GET":
        db = getMysqlConnection()
        try:
            sqlstr = "SELECT * from orang_tua"
            cur = db.cursor()
            cur.execute(sqlstr)
            output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
            return render_template('databaseOrtu.html', kalimat=output_json)


    
    


        
# UPDATE SISWA
@application.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    db = getMysqlConnection()
    cur = db.cursor()

    sqlstr = "SELECT kd_ortu from orang_tua"
    cur.execute(sqlstr)
    output_id_ortu = cur.fetchall()
    sqlstr = "SELECT * from kelas"
    cur.execute(sqlstr)
    output_id_kelas = cur.fetchall()

    strid = str(id)
    cur.execute('SELECT * FROM siswa WHERE nis='+strid+'')
    data = cur.fetchone()
    if request.method == 'POST':
        nis = str(id)
        nama = request.form['nama']
        alamat = request.form['alamat']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        gender = request.form['gender']
        agama = request.form['agama']
        id_kelas = request.form['id_kelas']
        kd_ortu = request.form['kd_ortu']
        tanggal_daftar = request.form['tanggal_daftar']
        sqlstr = "UPDATE `siswa` SET `nama_siswa` = '"+nama+"', `alamat` = '"+alamat+"', `tempat_lahir` = '"+tempat_lahir+"', `tgl_lahir` = '"+tanggal_lahir+"', `gender` = '"+gender+"', `agama` = '"+agama+"', `id_kelas` = '"+id_kelas+"', `kd_ortu` = '"+kd_ortu+"', `tgl_daftar` = '"+tanggal_daftar+"' WHERE `siswa`.`nis` = '"+nis+"';"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template(
            'edit.html', 
            data=data, 
            sukses=sukses, 
            disabled=disabled
        )
    else:
        cur.close()
        db.close()
        return render_template(
            'edit.html', 
            data=data, 
            disabled='',
            output_id_kelas=output_id_kelas,
            output_id_ortu=output_id_ortu
        ) 



# DELETE DATABASE SISWA
@application.route('/delete/<int:id>', methods=['GET'])
def delete(id):

    if request.method == 'GET':
        db = getMysqlConnection()
        idString = str(id)
        sqlstr = "DELETE FROM siswa WHERE nis="+idString+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()

        return redirect(url_for('database'))


# CREATE DATABASE SISWA
@application.route('/Profile/siswa', methods=['GET','POST'])
def profile():
    if request.method == 'GET':
        db = getMysqlConnection()
        cur = db.cursor()

        sqlstr = "SELECT kd_ortu from orang_tua"
        cur.execute(sqlstr)
        id_ortu = cur.fetchall()

        sqlstr = "SELECT * from kelas"
        cur.execute(sqlstr)
        id_kelas = cur.fetchall()


        return render_template('profile.html', id_ortu=id_ortu, id_kelas=id_kelas)
    if request.method == 'POST':
        # Mengambil data form
        db = getMysqlConnection()
        cur = db.cursor()
        nis = request.form['nis']
        nama = request.form['nama']
        alamat = request.form['alamat']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        gender = request.form['gender']
        agama = request.form['agama']
        id_kelas = request.form['id_kelas']
        kd_ortu = request.form['kd_ortu']
        tanggal_daftar = request.form['tanggal_daftar']
        # memasukkan data form ke dalam database siswa
        sqlstr = "INSERT INTO siswa (`nis`, `nama_siswa`, `alamat`, `tempat_lahir`, `tgl_lahir`, `gender`, `agama`, `id_kelas`, `kd_ortu`, `tgl_daftar`) VALUES ('"+nis+"', '"+nama+"', '"+alamat+"', '"+tempat_lahir+"', '"+tanggal_lahir+"', '"+gender+"', '"+agama+"', '"+id_kelas+"', '"+kd_ortu+"', '"+tanggal_daftar+"')"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        return render_template('profile.html')
    else:
        cur.close()
        db.close()
        return render_template('profile.html')

# PROFILE UTS Create
@application.route('/Profile/Ortu', methods=['GET','POST'])
def profileOrtu():
    if request.method == 'GET':
        return render_template('profileOrtu.html')
    if request.method == 'POST':
        db = getMysqlConnection()
        cur = db.cursor()
        kd_ortu = request.form['kd_ortu']
        nama = request.form['nama']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        status = request.form['status']
        
        sqlstr = "INSERT INTO orang_tua (`kd_ortu`, `nama_ortu`, `alamat`, `telepon`, `pekerjaan`, `agama`, `status`) VALUES ('"+kd_ortu+"', '"+nama+"', '"+alamat+"', '"+telepon+"', '"+pekerjaan+"', '"+agama+"', '"+status+"') "
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        return render_template('profileOrtu.html')
    else:
        cur.close()
        db.close()
        return render_template('profileOrtu.html')

# UPDATE ORANG TUA
@application.route('/editOrtu/<int:id>', methods=['GET','POST'])
def editOrtu(id):
    db = getMysqlConnection()
    cur = db.cursor()
    strid = str(id)
    cur.execute('SELECT * FROM orang_tua WHERE kd_ortu='+strid+'')
    data = cur.fetchone()
    if request.method == 'POST':
        kd_ortu = request.form['kd_ortu']
        nama = request.form['nama']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        status = request.form['status']
        sqlstr = "UPDATE `orang_tua` SET `kd_ortu` = '"+kd_ortu+"', `nama_ortu` = '"+nama+"', `alamat` = '"+alamat+"', `telepon` = '"+telepon+"', `pekerjaan` = '"+pekerjaan+"', `agama` = '"+agama+"', `status` = '"+status+"' WHERE `orang_tua`.`kd_ortu` = '"+strid+"'; "
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template(
            'editOrtu.html', 
            data=data, 
            sukses=sukses, 
            disabled=disabled
        )
    else:
        cur.close()
        db.close()
        return render_template(
            'editOrtu.html', 
            data=data, 
            disabled=''
        ) 

#DELETE ORANG TUA
# Delete
@application.route('/deleteOrtu/<int:id>', methods=['GET'])
def deleteOrtu(id):

    if request.method == 'GET':
        db = getMysqlConnection()
        idString = str(id)
        sqlstr = "DELETE FROM orang_tua WHERE kd_ortu="+idString+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()

        return redirect(url_for('database'))

# UPDATE GURU
@application.route('/editGuru/<int:id>', methods=['GET','POST'])
def editGuru(id):
    db = getMysqlConnection()
    cur = db.cursor()
    strid = str(id)
    cur.execute('SELECT * FROM guru WHERE nip='+strid+'')
    data = cur.fetchone()
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        alamat = request.form['alamat']
        tempat_lahir = request.form['tempat_lahir']
        gender = request.form['gender']
        agama = request.form['agama']
        telepon = request.form['telepon']
        pendidikan = request.form['pendidikan']
        status = request.form['status']
        sqlstr = "UPDATE `guru` SET `nip` = '"+nip+"', `nama_guru` = '"+nama+"', `alamat` = '"+alamat+"', `tmp_lahir` = '"+tempat_lahir+"', `gender` = '"+gender+"', `agama` = '"+agama+"', `telepon` = '"+telepon+"', `pendidikan` = '"+pendidikan+"', `status` = '"+status+"' WHERE `guru`.`nip` = '"+strid+"';"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template(
            'editGuru.html', 
            data=data, 
            sukses=sukses, 
            disabled=disabled
        )
    else:
        cur.close()
        db.close()
        return render_template(
            'editGuru.html', 
            data=data, 
            disabled=''
        ) 

#DELETE GURU
@application.route('/deleteGuru/<int:id>', methods=['GET'])
def deleteGuru(id):

    if request.method == 'GET':
        db = getMysqlConnection()
        idString = str(id)
        sqlstr = "DELETE FROM guru WHERE nip="+idString+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()

        return redirect(url_for('database'))


# CREATE DATABASE GURU
@application.route('/Profile/guru', methods=['GET','POST'])
def profileGuru():
    if request.method == 'GET':
        return render_template('profileGuru.html')
    if request.method == 'POST':
        db = getMysqlConnection()
        cur = db.cursor()
        nip = request.form['nip']
        nama = request.form['nama']
        alamat = request.form['alamat']
        tempat_lahir = request.form['tempat_lahir']
        gender = request.form['gender']
        agama = request.form['agama']
        telepon = request.form['telepon']
        pendidikan = request.form['pendidikan']
        status = request.form['status']
        
        sqlstr = "INSERT INTO guru (`nip`, `nama_guru`, `alamat`, `tmp_lahir`, `gender`, `agama`, `telepon`, `pendidikan`, `status`) VALUES ('"+nip+"', '"+nama+"', '"+alamat+"', '"+tempat_lahir+"', '"+gender+"', '"+agama+"', '"+telepon+"', '"+pendidikan+"', '"+status+"')"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template('profileGuru.html')
    else:
        cur.close()
        db.close()
        return render_template('profileGuru.html')

# UPDATE KELAS
@application.route('/editKelas/<int:id>', methods=['GET','POST'])
def editKelas(id):
    db = getMysqlConnection()
    cur = db.cursor()
    sqlstr = "SELECT nip from guru"
    cur.execute(sqlstr)
        
    id_kelas = cur.fetchall()
    strid = str(id)
    cur.execute('SELECT * FROM kelas WHERE id_kelas='+strid+'')
    data = cur.fetchone()
    if request.method == 'POST':
        id_kelas = request.form['id_kelas']
        kelas = request.form['nama']
        nip = request.form['nip']
        sqlstr = "UPDATE `kelas` SET `id_kelas` = '"+id_kelas+"', `kelas` = '"+kelas+"', `nip` = '"+nip+"' WHERE `kelas`.`id_kelas` = '"+strid+"';"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template(
            'editKelas.html', 
            data=data, 
            sukses=sukses, 
            disabled=disabled,
            id=id_kelas
        )
    else:
        cur.close()
        db.close()
        return render_template(
            'editKelas.html', 
            data=data, 
            disabled='',
            id=id_kelas
        ) 

#DELETE KELAS
@application.route('/deleteKelas/<int:id>', methods=['GET'])
def deleteKelas(id):

    if request.method == 'GET':
        db = getMysqlConnection()
        idString = str(id)
        sqlstr = "DELETE FROM kelas WHERE id_kelas="+idString+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()

        return redirect(url_for('database'))

# CREATE DATABASE KELAS
@application.route('/Profile/kelas', methods=['GET','POST'])
def profileKelas():
    if request.method == 'GET':
        db = getMysqlConnection()
        cur = db.cursor()

        sqlstr = "SELECT nip from guru"
        cur.execute(sqlstr)
        
        id_kelas = cur.fetchall()


        return render_template('profileKelas.html', id=id_kelas)
    if request.method == 'POST':
        db = getMysqlConnection()
        cur = db.cursor()
        id_kelas = request.form['id_kelas']
        kelas = request.form['nama']
        nip = request.form['nip']
        
        sqlstr = "INSERT INTO kelas (`id_kelas`, `kelas`, `nip`) VALUES ('"+id_kelas+"', '"+kelas+"', '"+nip+"')"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        return render_template('profileKelas.html')
    else:
        cur.close()
        db.close()
        return render_template('profileKelas.html')

# UPDATE DATABASE MATA PELAJARAN
@application.route('/editMapel/<int:id>', methods=['GET','POST'])
def editMapel(id):
    db = getMysqlConnection()
    cur = db.cursor()
    strid = str(id)
    cur.execute('SELECT * FROM mapel WHERE id_mapel='+strid+'')
    data = cur.fetchone()
    if request.method == 'POST':
        id_mapel = request.form['id_mapel']
        nama = request.form['nama']
        sqlstr = "UPDATE `mapel` SET `id_mapel` = '"+id_mapel+"', `nama_mapel` = '"+nama+"' WHERE `mapel`.`id_mapel` = '"+strid+"';"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template(
            'editMapel.html', 
            data=data, 
            sukses=sukses, 
            disabled=disabled
        )
    else:
        cur.close()
        db.close()
        return render_template(
            'editMapel.html', 
            data=data, 
            disabled=''
        ) 

#DELETE DATABASE MATA PELAJARAN
@application.route('/deleteMapel/<int:id>', methods=['GET'])
def deleteMapel(id):

    if request.method == 'GET':
        db = getMysqlConnection()
        idString = str(id)
        sqlstr = "DELETE FROM mapel WHERE id_mapel="+idString+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()

        return redirect(url_for('database'))

# CREATE DATABASE MATA PELAJARAN
@application.route('/Profile/mapel', methods=['GET','POST'])
def profileMapel():
    if request.method == 'GET':
        return render_template('profileMapel.html')
    if request.method == 'POST':
        db = getMysqlConnection()
        cur = db.cursor()
        id_mapel = request.form['id_mapel']
        nama = request.form['nama']
        
        sqlstr = "INSERT INTO mapel (`id_mapel`, `nama_mapel`) VALUES ('"+id_mapel+"', '"+nama+"')"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        return render_template('profileMapel.html')
    else:
        cur.close()
        db.close()
        return render_template('profileMapel.html')


# UPDATE DATABASE PENGGUNA
@application.route('/editUser/<string:id>', methods=['GET','POST'])
def editUser(id):
    db = getMysqlConnection()
    cur = db.cursor()
    
    sqlstr = "SELECT * FROM pengguna WHERE username='"+id+"'"
    cur.execute(sqlstr)
    data = cur.fetchone()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sqlstr = "UPDATE `pengguna` SET `username` = '"+username+"', `password` = '"+password+"' WHERE `pengguna`.`username` = '"+id+"';"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template(
            'editUser.html', 
            data=data, 
            sukses=sukses, 
            disabled=disabled
        )
    else:
        cur.close()
        db.close()
        return render_template(
            'editUser.html', 
            data=data, 
            disabled=''
        ) 
        

#DELETE DATABASE MATA PELAJARAN
@application.route('/deleteUser/<int:id>', methods=['GET'])
def deleteUser(id):

    if request.method == 'GET':
        db = getMysqlConnection()
        idString = str(id)
        sqlstr = "DELETE FROM pengguna WHERE nis="+idString+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()

        return redirect(url_for('database'))

@application.route('/informasi/<int:id>')
# ID Default halaman informasi adalah 0
def informasi(id):
    # Cek apakah sudah login
    if not 'loggedin' in session:
        # Jika belum maka akan masuk ke halaman login
        return render_template('login.html')

    # Jika sudah login
    db = getMysqlConnection()
    cur = db.cursor()
    # Memasukkan isi data username di session ke variabel username
    username = session['username']

    hidden = ""

    if session['username'] != 'admin':
        hidden = "hidden"

    if id == 0 :
        cur.execute("SELECT * from kelas")
        data_kelas = cur.fetchall()
        db.close()
        cur_id = str(data_kelas[0][0])
        cur_kelas = data_kelas[0][1]
    else :
        idStr = str(id)
        cur.execute("SELECT * from kelas where id_kelas='"+idStr+"'")
        data_kelas = cur.fetchall()
        db.close() 
        cur_id = str(data_kelas[0][0])
        cur_kelas = data_kelas[0][1]
    # ambil data kelas
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from kelas")
    data_kelas_all = cur.fetchall()
    db.close()
    # ambil data kelas berdasarkan id yang akan ditampilkan
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * FROM `siswa` WHERE `id_kelas`='"+cur_id+"'")
    data_siswa = cur.fetchall()
    db.close()
    # menampilkan halaman informasi
    return render_template(
        'informasi.html',
        nama_akun="admin",
        username=username,
        data_siswa=data_siswa,
        data_kelas=data_kelas_all,
        cur_kelas=cur_kelas,
        hidden=hidden
    )



# CREATE DATABASE MENGAJAR
@application.route('/Profile/mengajar', methods=['GET','POST'])
def profileMengajar():
    if request.method == 'GET':
        db = getMysqlConnection()
        cur = db.cursor()
        # Mengambil id mapel
        sqlstr = "SELECT * from mapel"
        cur.execute(sqlstr)
        output_id_mapel = cur.fetchall()

        # Mengambil nip guru
        sqlstr = "SELECT nip from guru"
        cur.execute(sqlstr)
        output_nip = cur.fetchall()

        return render_template('profileMengajar.html', id_mapel=output_id_mapel, nip=output_nip)
    if request.method == 'POST':
        db = getMysqlConnection()
        cur = db.cursor()
        input_id_mapel = request.form.getlist('id_mapel')
        nip = request.form['nip']
        
        for i in input_id_mapel:
            cur.execute('INSERT INTO mengajar VALUES (%s, %s)', (nip, i[0],))
            db.commit()

        
        cur.close()
        db.close()
        return render_template('profileMengajar.html')
    else:
        cur.close()
        db.close()
        return render_template('profileMengajar.html')


#DELETE DATABASE MENGAJAR
@application.route('/deleteMengajar/<int:id>', methods=['GET'])
def deleteMengajar(id):

    if request.method == 'GET':
        db = getMysqlConnection()
        idString = str(id)
        sqlstr = "DELETE FROM mengajar WHERE nip="+idString+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()

        return redirect(url_for('database'))

# EDIT DATABASE MENGAJAR
@application.route('/editMengajar/<int:id>', methods=['GET','POST'])
def editMengajar(id):

    strid = str(id)
    db = getMysqlConnection()
    cur = db.cursor()

    # Mengambil id mapel
    sqlstr = "SELECT * from mapel"
    cur.execute(sqlstr)
    output_id_mapel = cur.fetchall()

    # Mengambil nip guru
    sqlstr = "SELECT nip from mengajar where nip =' "+strid+" ' "
    cur.execute(sqlstr)
    output_nip = cur.fetchall()

    if request.method == 'GET':
        return render_template('editMengajar.html', id_mapel=output_id_mapel, nip=output_nip)
    if request.method == 'POST':
        db = getMysqlConnection()
        cur = db.cursor()
        sqlstr = "DELETE FROM mengajar WHERE nip="+strid+""
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
        
        input_id_mapel = request.form.getlist('id_mapel')
        nip = request.form['nip']
        
        for i in input_id_mapel:
            cur.execute('INSERT INTO mengajar VALUES (%s, %s)', (nip, i[0],))
            db.commit()

        
        cur.close()
        db.close()
        return render_template('editMengajar.html', id_mapel=output_id_mapel, nip=output_nip, disabled="disabled")
    else:
        cur.close()
        db.close()
        return render_template('editMengajar.html', id_mapel=output_id_mapel, nip=output_nip)


# @application.route('/informasi')
# def informasi():
#     if 'loggedin' in session and session['username'] == 'admin':
#         return render_template('informasi.html')

#     return redirect(url_for('login'))

@application.route('/index2')
def index2():
    hidden = "hidden"
    if 'loggedin' in session and session['username'] == 'admin':
        return render_template('index.html', hidden="hidden")
    if 'loggedin' in session:
        return render_template('index.html', hidden=hidden, hidden3=hidden)

    return render_template('index.html', hidden3="hidden", hidden2=hidden)
    


@application.route('/hello')
def hello_world():
    return "<p>hellow world</p>"

@application.route('/person/')
def hello():
    # Menggunakan dictionary = True pada db.cursor() agar dapat memasukkan string ke dalam index isi['string]
    # jika tidak menggunakan dictionay, maka index harus berupa angka isi[0] == isi['id_mapel]
    db = getMysqlConnection()
    cur = db.cursor(dictionary=True)

    sqlstr = "SELECT * from mapel"
    cur.execute(sqlstr)
    data = cur.fetchall()
    output_mapel = []
    content = {}

    for isi in data:
        content = {'$tabel' :["mapel"],'id_mapel' : isi['id_mapel'], 'nama_mapel' : isi['nama_mapel']}
        output_mapel.append(content)
        content = {}

    sqlstr = "SELECT * from kelas"
    cur.execute(sqlstr)
    data = cur.fetchall()
    output_kelas = []
    content = {}

    for isi in data:
        content = {'$tabel' :["kelas"],'id_kelas' : isi['id_kelas'], 'kelas' : isi['kelas'], 'nip' : isi['nip']}
        output_kelas.append(content)
        content = {}

    sqlstr = "SELECT * from guru"
    cur.execute(sqlstr)
    data = cur.fetchall()
    output_guru = []
    content = {}

    for isi in data:
        content = {'$tabel' :["guru"],'nip' : isi['nip'], 'nama_guru' : isi['nama_guru'], 'alamat' : isi['alamat'], 'tmp_lahir' : isi['tmp_lahir'], 'gender' : isi['gender'], 'agama' : isi['agama'], 'telepon' : isi['telepon'], 'pendidikan' : isi['pendidikan'], 'status' : isi['status']}
        output_guru.append(content)
        content = {}

    sqlstr = "SELECT * from mengajar"
    cur.execute(sqlstr)
    data = cur.fetchall()
    output_mengajar = []
    content = {}

    for isi in data:
        content = {'$tabel' :["mengajar"],'nip' : isi['nip'], 'id_mapel' : isi['id_mapel']}
        output_mengajar.append(content)
        content = {}

    sqlstr = "SELECT * from orang_tua"
    cur.execute(sqlstr)
    data = cur.fetchall()
    output_orang_tua = []
    content = {}

    for isi in data:
        content = {'$tabel' :["orang tua"],'kd_ortu' : isi['kd_ortu'], 'nama_ortu' : isi['nama_ortu'], 'alamat' : isi['alamat'], 'telepon' : isi['telepon'], 'pekerjaan' : isi['pekerjaan'], 'agama' : isi['agama'], 'status' : isi['status']}
        output_orang_tua.append(content)
        content = {}

    sqlstr = "SELECT * from pengguna"
    cur.execute(sqlstr)
    data = cur.fetchall()
    output_pengguna = []
    content = {}

    for isi in data:
        content = {'$tabel' :["pengguna"],'username' : isi['username'], 'password' : isi['password']}
        output_pengguna.append(content)
        content = {}
    
    sqlstr = "SELECT * from siswa"
    cur.execute(sqlstr)
    data = cur.fetchall()
    output_siswa = []
    content = {}

    for isi in data:
        content = {'$tabel' :["siswa"],'nis' : isi['nis'], 'nama_siswa' : isi['nama_siswa'], 'alamat' : isi['alamat'], 'tempat_lahir' : isi['tempat_lahir'], 'tgl_lahir' : isi['tgl_lahir'], 'gender' : isi['gender'], 'agama' : isi['agama'], 'id_kelas' : isi['id_kelas'], 'kd_ortu' : isi['kd_ortu'], 'tgl_daftar' : isi['tgl_daftar']}
        output_siswa.append(content)
        content = {}


    return jsonify(output_mapel, output_kelas, output_guru, output_mengajar, output_orang_tua, output_pengguna, output_siswa)

if __name__ == '__main__':
    application.run(debug=True)