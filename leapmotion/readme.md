*GUI_LeapMotion Specification*
3/6/2018 S.Hirose

1.Raspberry-pi-Send-Data
	List:
	send = [MotorFrontRight,MotorFrontLeft,MotorBackRight,MotorBackLeft,
	        LED0,LED1,LED2,LED3,LED4,LED5,LED6,LED7,LED8]

	                    Motor
	        FrontLeft           FrontRight
	        Back Left           Back Right

			            LED
			            
			    LED0    LED1    LED2
			    LED3    LED4    LED5
			    LED6    LED7    LED8

2.Variables

	led_status : LEDのデータ（現在状態）List[ [now] for i in range(9)]
				 userが決めたLED_patternを格納する
				 0 1 2
				 3 4 5
				 6 7 8
	
	Mode	   :　Modeの番号によって機能が変化する．
	 Modeは主にLeapMotionでの機能の切り替わりに利用する

	Mode : menu のイメージ

		Mode == 0~99 ：　LED

		Mode==0
			LEDモード　（LeapMotion側でLEDモードに切り替わる）
		Mode==1
			点灯パターンが変わっても，全部点灯した状態を保つ
		Mode==2
			手の高さによってLEDの点灯状態が変化する
		Mode==3
			SwipeによってLEDの点灯状態が変化する
		Mode==4
			手のぐーぱーによってLEDの点灯状態が変化する
		Mode==5
			:
			:
			：

		機能を追加したらMode==5~99にLEDの制御に関する動作が変わる

	--------------------------------------------------------------
	
		Mode==100
			モーター駆動（GO!)　：　手の角度に対してローバー動きが変わる
		Mode==101
			モーター駆動（GO!)　：　手のベクトルに対してローバー動きが変わる
		旋回はMode==100,101に含まれると思う

			:
			:

		機能を追加したらMode==100~199にモーターの制御に関する動作が変わる

	-------------------------------------------------------------

		Mode==200
			隠しコマンド01 : 音楽（？)　

			:
			:

		機能を追加したらMode==200~299に隠しコマンドに関する動作をする


	status     : すべてのデータ(現在状態)List[[now] for i in range(14)]
		これをSendする(Send Dataは上を参照)

	LED_GO	   : LEDの点灯方法を変化させる変数

		LED_GO==0
			普通に全部点灯（Mode==1と違うのは，点灯パターンが変われば，点灯状態が変化する所）
		LED_GO==1
			右回転
		LED_GO==2
			左回転
		LED_GO==3
			点滅

			:
			:
			:

		機能を追加したらLED_GOの値を増やす

	Cycle   : 点滅および回転周期（1回転にかかる時間) 	** 単位はミリ秒
	Cycle_t : 点滅および回転を続ける時間　			** 単位は秒
	tail    : LEDを回転点灯させるときの尾の光の強さ（実装はするかわからない）　** 単位は%
			(一つ前の明るさに対して[tail]%の予定）
			
