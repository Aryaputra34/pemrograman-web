-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 27 Nov 2022 pada 12.33
-- Versi server: 10.4.22-MariaDB
-- Versi PHP: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `watchlist`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `guru`
--

CREATE TABLE `guru` (
  `nip` int(11) NOT NULL,
  `nama_guru` varchar(30) NOT NULL,
  `alamat` varchar(30) NOT NULL,
  `tmp_lahir` varchar(30) DEFAULT NULL,
  `gender` varchar(30) DEFAULT NULL,
  `agama` varchar(30) DEFAULT NULL,
  `telepon` varchar(30) DEFAULT NULL,
  `pendidikan` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `guru`
--

INSERT INTO `guru` (`nip`, `nama_guru`, `alamat`, `tmp_lahir`, `gender`, `agama`, `telepon`, `pendidikan`, `status`) VALUES
(1234, 'Hendra', 'Jakarta Timur', 'Sukabumi', 'Laki - laki', 'Islam', '088845784596', 'S2', 'Aktif'),
(3210, 'Deny', 'Jakarta Selatan', 'Tangerang', 'Laki - laki', 'Islam', '081546578456', 'S2', 'Aktif');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kelas`
--

CREATE TABLE `kelas` (
  `id_kelas` int(11) NOT NULL,
  `kelas` varchar(30) NOT NULL,
  `nip` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `kelas`
--

INSERT INTO `kelas` (`id_kelas`, `kelas`, `nip`) VALUES
(1, 'Kelas 1', 1234),
(2, 'kelas 2', 3210);

-- --------------------------------------------------------

--
-- Struktur dari tabel `list`
--

CREATE TABLE `list` (
  `no` int(11) NOT NULL,
  `nama` varchar(30) NOT NULL,
  `progres` varchar(10) DEFAULT '0%',
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `list`
--

INSERT INTO `list` (`no`, `nama`, `progres`, `created`, `updated`) VALUES
(1, 'One Piece', '60%', '2022-10-26 01:42:21', '2022-10-26 01:42:21'),
(2, 'Dragon Ball', '75%', '2022-10-26 01:42:21', '2022-10-26 01:42:21'),
(3, 'Naruto', '40%', '2022-10-26 01:42:21', '2022-10-26 01:42:21'),
(4, 'Bleach', '90%', '2022-10-26 01:42:21', '2022-10-26 01:42:21'),
(5, 'Black Clover', '100%', '2022-10-26 01:42:21', '2022-10-26 01:42:21'),
(62, 'Boruto', '60%', '2022-11-02 06:35:37', '2022-11-02 07:06:48'),
(71, 'Chainsaw Man', '40%', '2022-11-02 07:18:28', '2022-11-02 07:18:28');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mapel`
--

CREATE TABLE `mapel` (
  `id_mapel` int(11) NOT NULL,
  `nama_mapel` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `mapel`
--

INSERT INTO `mapel` (`id_mapel`, `nama_mapel`) VALUES
(1, 'Matematika'),
(2, 'Fisika'),
(3, 'Biologi'),
(4, 'Kimia');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mengajar`
--

CREATE TABLE `mengajar` (
  `nip` int(11) DEFAULT NULL,
  `id_mapel` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `mengajar`
--

INSERT INTO `mengajar` (`nip`, `id_mapel`) VALUES
(3210, 1),
(3210, 2),
(3210, 3),
(3210, 4);

-- --------------------------------------------------------

--
-- Struktur dari tabel `orang_tua`
--

CREATE TABLE `orang_tua` (
  `kd_ortu` int(11) NOT NULL,
  `nama_ortu` varchar(30) NOT NULL,
  `alamat` varchar(30) DEFAULT NULL,
  `telepon` varchar(30) DEFAULT NULL,
  `pekerjaan` varchar(30) DEFAULT NULL,
  `agama` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `orang_tua`
--

INSERT INTO `orang_tua` (`kd_ortu`, `nama_ortu`, `alamat`, `telepon`, `pekerjaan`, `agama`, `status`) VALUES
(10002, 'Angelina Jolie', 'Jakarta Selatan', '081546536456', 'Rumah Tangga', 'Katolik', 'Orang tua kandung');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pengguna`
--

CREATE TABLE `pengguna` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `pengguna`
--

INSERT INTO `pengguna` (`username`, `password`) VALUES
('admin', 'admin'),
('aryaputra34', 'inipassword'),
('blacksitt', '123');

-- --------------------------------------------------------

--
-- Struktur dari tabel `siswa`
--

CREATE TABLE `siswa` (
  `nis` int(11) NOT NULL,
  `nama_siswa` varchar(30) NOT NULL,
  `alamat` varchar(30) DEFAULT NULL,
  `tempat_lahir` varchar(30) DEFAULT NULL,
  `tgl_lahir` varchar(30) DEFAULT NULL,
  `gender` varchar(30) DEFAULT NULL,
  `agama` varchar(30) DEFAULT NULL,
  `id_kelas` int(11) DEFAULT NULL,
  `kd_ortu` int(11) DEFAULT NULL,
  `tgl_daftar` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `siswa`
--

INSERT INTO `siswa` (`nis`, `nama_siswa`, `alamat`, `tempat_lahir`, `tgl_lahir`, `gender`, `agama`, `id_kelas`, `kd_ortu`, `tgl_daftar`) VALUES
(12341, 'Angel Prasanti', 'Jakarta Selatan', 'Jakarta Selatan', '06/04/2002', 'Perempuan', 'Katolik', 1, 10002, '5 Juli 2021');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `guru`
--
ALTER TABLE `guru`
  ADD PRIMARY KEY (`nip`);

--
-- Indeks untuk tabel `kelas`
--
ALTER TABLE `kelas`
  ADD PRIMARY KEY (`id_kelas`),
  ADD KEY `nip` (`nip`);

--
-- Indeks untuk tabel `list`
--
ALTER TABLE `list`
  ADD PRIMARY KEY (`no`);

--
-- Indeks untuk tabel `mapel`
--
ALTER TABLE `mapel`
  ADD PRIMARY KEY (`id_mapel`);

--
-- Indeks untuk tabel `mengajar`
--
ALTER TABLE `mengajar`
  ADD UNIQUE KEY `id_mapel` (`id_mapel`),
  ADD KEY `nip` (`nip`) USING BTREE;

--
-- Indeks untuk tabel `orang_tua`
--
ALTER TABLE `orang_tua`
  ADD PRIMARY KEY (`kd_ortu`);

--
-- Indeks untuk tabel `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`username`);

--
-- Indeks untuk tabel `siswa`
--
ALTER TABLE `siswa`
  ADD PRIMARY KEY (`nis`),
  ADD UNIQUE KEY `id_kelas` (`id_kelas`),
  ADD KEY `kd_ortu` (`kd_ortu`) USING BTREE;

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `guru`
--
ALTER TABLE `guru`
  MODIFY `nip` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=123456791;

--
-- AUTO_INCREMENT untuk tabel `kelas`
--
ALTER TABLE `kelas`
  MODIFY `id_kelas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1117;

--
-- AUTO_INCREMENT untuk tabel `list`
--
ALTER TABLE `list`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT untuk tabel `mapel`
--
ALTER TABLE `mapel`
  MODIFY `id_mapel` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT untuk tabel `orang_tua`
--
ALTER TABLE `orang_tua`
  MODIFY `kd_ortu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14214;

--
-- AUTO_INCREMENT untuk tabel `siswa`
--
ALTER TABLE `siswa`
  MODIFY `nis` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2107421241;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `kelas`
--
ALTER TABLE `kelas`
  ADD CONSTRAINT `kelas_ibfk_1` FOREIGN KEY (`nip`) REFERENCES `guru` (`nip`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `mengajar`
--
ALTER TABLE `mengajar`
  ADD CONSTRAINT `mengajar_ibfk_1` FOREIGN KEY (`nip`) REFERENCES `guru` (`nip`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `mengajar_ibfk_2` FOREIGN KEY (`id_mapel`) REFERENCES `mapel` (`id_mapel`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `siswa`
--
ALTER TABLE `siswa`
  ADD CONSTRAINT `siswa_ibfk_1` FOREIGN KEY (`id_kelas`) REFERENCES `kelas` (`id_kelas`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `siswa_ibfk_2` FOREIGN KEY (`kd_ortu`) REFERENCES `orang_tua` (`kd_ortu`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- selesai
