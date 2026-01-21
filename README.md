# GoBGP RPM Package

GoBGP v4.2.0 の RPM パッケージビルド用リポジトリです。

## yum リポジトリとして利用

```bash
# リポジトリ追加
sudo curl -o /etc/yum.repos.d/GoBGP.repo \
  https://ryskn.github.io/GoBGP/GoBGP.repo

# インストール
sudo dnf install gobgp
```

## 手動ビルド手順

### 1. 必要なパッケージのインストール

```bash
sudo dnf install -y rpm-build rpmdevtools golang git
```

### 2. リポジトリのクローン

```bash
git clone https://github.com/ryskn/GoBGP.git ~/rpmbuild
cd ~/rpmbuild
```

### 3. ソースのダウンロード

```bash
spectool -g -R SPECS/GoBGP.spec
```

または手動でダウンロード:

```bash
curl -L -o SOURCES/v4.2.0.tar.gz https://github.com/osrg/gobgp/archive/refs/tags/v4.2.0.tar.gz
```

### 4. RPM のビルド

```bash
rpmbuild -ba SPECS/GoBGP.spec
```

### 5. インストール

```bash
sudo dnf install RPMS/$(uname -m)/gobgp-4.2.0-1.el9.$(uname -m).rpm
```

## インストール後

```bash
# 設定ファイルを編集
sudo vim /etc/gobgpd/gobgpd.conf

# サービス起動
sudo systemctl enable --now gobgpd
```

## ファイル構成

| パス | 説明 |
|-----|------|
| `/usr/sbin/gobgpd` | GoBGP デーモン |
| `/usr/bin/gobgp` | GoBGP CLI |
| `/etc/gobgpd/gobgpd.conf` | 設定ファイル |
| `/usr/lib/systemd/system/gobgpd.service` | systemd サービス |

## 参考

- [GoBGP GitHub](https://github.com/osrg/gobgp)
- [GoBGP ドキュメント](https://github.com/osrg/gobgp/blob/master/docs/sources/configuration.md)
