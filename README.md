![](https://github.com/TakaoNarikawa/Univ-CS-WSGI/blob/master/logo.png?raw=true)

![](https://github.com/TakaoNarikawa/Univ-CS-WSGI/blob/master/screenshots/real-fake.png?raw=true)

## 概要

コンピュータ科学科実験 WSGI 課題

Python WCGI を用いて Web アプリケーションを作成した

GAN（Generative Adversarial Network）の Descriminator が行っていることを、
人間にチャレンジさせてみようというアプリケーションである。

## Requirement

```
Python 3.6 or higher
```

## Getting Started

```sh
$ cd cgi-bin
$ python3 -m run [-h] [--port PORT] [--dbname DBNAME]
```


## Reference

`cgi-bin/real_imgs/` に存在する画像は [NVlabs / ffhq-dataset](https://github.com/NVlabs/ffhq-dataset) によって生成されたものを使用した。

`cgi-bin/fake_imgs/` に存在する画像は [NVlabs / stylegan2](https://github.com/NVlabs/stylegan2) によって生成されたものを使用した。

```
@article{Karras2019stylegan2,
  title   = {Analyzing and Improving the Image Quality of {StyleGAN}},
  author  = {Tero Karras and Samuli Laine and Miika Aittala and Janne Hellsten and Jaakko Lehtinen and Timo Aila},
  journal = {CoRR},
  volume  = {abs/1912.04958},
  year    = {2019},
}
```
