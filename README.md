## chiron  
### main  repository  
## 2017 meister  

### 送信側  
`teamet@JETxx:$ssh <user-name>@<ip-address>`   

`~> cd ~/2017.meister/pigpio`   
`2/pigpio> python3 main.py`    

### 受信側   
#### 動作確認用プログラム    
`teamet@JETxx:$cd 2017.meister/socket`    
`python3 UdpClient.py`    

```    
{"right"：50、 "left"：30}    
```    
jsonのデータは "right"と "left"を持っています。キーの各値はpwmの値を意味します。    
