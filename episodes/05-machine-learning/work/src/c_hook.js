// ================= 小图标：猫、狗、杯子、球、沙发、书、显示器 =================
function cat(x,y,s,col=INK,alpha=1){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);X.fillStyle=col;
 // 身体 + 尾巴
 X.beginPath();X.ellipse(0,52,44,34,0,0,Math.PI*2);X.fill();
 X.strokeStyle=col;X.lineWidth=10;X.lineCap='round';X.beginPath();X.moveTo(40,62);X.quadraticCurveTo(82,58,70,10);X.stroke();
 // 头 + 耳朵
 X.beginPath();X.arc(0,-6,38,0,Math.PI*2);X.fill();
 X.beginPath();X.moveTo(-34,-20);X.lineTo(-30,-62);X.lineTo(-8,-38);X.closePath();X.fill();
 X.beginPath();X.moveTo(34,-20);X.lineTo(30,-62);X.lineTo(8,-38);X.closePath();X.fill();
 // 眼睛 + 胡子
 X.fillStyle=PAPER;X.beginPath();X.ellipse(-13,-8,5,8,0,0,Math.PI*2);X.ellipse(13,-8,5,8,0,0,Math.PI*2);X.fill();
 X.strokeStyle=PAPER;X.lineWidth=2.5;X.beginPath();
 for(const d of [-1,1]){X.moveTo(d*14,8);X.lineTo(d*46,2);X.moveTo(d*14,13);X.lineTo(d*46,16);}X.stroke();X.restore();}
function dog(x,y,s,col=MUTE,alpha=1){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);X.fillStyle=col;
 X.beginPath();X.ellipse(0,52,46,32,0,0,Math.PI*2);X.fill();X.beginPath();X.arc(0,-6,36,0,Math.PI*2);X.fill();
 X.beginPath();X.ellipse(-36,0,13,30,0.3,0,Math.PI*2);X.ellipse(36,0,13,30,-0.3,0,Math.PI*2);X.fill();
 X.fillStyle=PAPER;X.beginPath();X.arc(-12,-10,5,0,Math.PI*2);X.arc(12,-10,5,0,Math.PI*2);X.fill();
 X.beginPath();X.ellipse(0,10,9,6,0,0,Math.PI*2);X.fill();X.restore();}
function cup(x,y,s,col=MUTE,alpha=1){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);X.fillStyle=col;
 X.beginPath();X.roundRect(-36,-30,62,84,10);X.fill();X.strokeStyle=col;X.lineWidth=10;X.beginPath();X.arc(30,10,20,-Math.PI/2,Math.PI/2);X.stroke();
 X.strokeStyle=col;X.lineWidth=5;X.lineCap='round';for(const dx of [-16,4]){X.beginPath();X.moveTo(dx,-44);X.quadraticCurveTo(dx+10,-58,dx,-72);X.stroke();}X.restore();}
function ball(x,y,s,col=MUTE,alpha=1){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);X.fillStyle=col;
 X.beginPath();X.arc(0,20,48,0,Math.PI*2);X.fill();X.strokeStyle=PAPER;X.lineWidth=4;X.beginPath();X.arc(0,20,48,-0.3,Math.PI+0.3,true);X.stroke();
 X.beginPath();X.moveTo(0,-28);X.lineTo(0,68);X.stroke();X.restore();}
function sofa(x,y,s,col=MUTE,alpha=1){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);X.fillStyle=SOFT;X.strokeStyle=col;X.lineWidth=4;
 X.beginPath();X.roundRect(-70,-30,140,62,14);X.fill();X.stroke();                // 靠背
 X.beginPath();X.roundRect(-80,20,160,40,12);X.fill();X.stroke();                  // 坐垫
 X.beginPath();X.roundRect(-92,0,26,62,10);X.roundRect(66,0,26,62,10);X.fill();X.stroke();
 X.lineWidth=6;X.lineCap='round';X.beginPath();X.moveTo(-70,62);X.lineTo(-70,78);X.moveTo(70,62);X.lineTo(70,78);X.stroke();X.restore();}
// 一张带标签的训练图
function tile(x,y,w,kind,lab,on,alpha=1,withSofa=false){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;
 X.fillStyle=CARD;X.beginPath();X.roundRect(x-w/2,y-w/2,w,w,14);X.fill();X.lineWidth=3;X.strokeStyle=on?RED:SOFT;X.stroke();
 const s=w/230;
 if(withSofa){sofa(x,y+w*0.18,s*1.15,MUTE);if(kind==='cat')cat(x,y-w*0.1,s*0.95,INK);}
 else if(kind==='cat')cat(x-s*10,y-w*0.06,s*1.15,INK);else if(kind==='dog')dog(x,y-w*0.08,s*1.15,MUTE);else if(kind==='cup')cup(x,y-w*0.04,s*1.15,MUTE);else if(kind==='ball')ball(x,y-w*0.1,s*1.05,MUTE);
 X.restore();
 if(lab)tag(lab,x,y+w/2+4,on?RED:MUTE,on,Math.round(w*0.15),alpha);}
function book(x,y,s,alpha){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);
 X.fillStyle=SOFT;X.beginPath();X.roundRect(-150,-190,300,380,16);X.fill();X.fillStyle=RED;X.fillRect(-150,-190,26,380);
 X.fillStyle=INK;X.font=`900 50px ${SERIF}`;X.textAlign='center';X.fillText('猫的',16,-70);X.fillText('说明书',16,-6);
 X.strokeStyle=MUTE;X.lineWidth=4;for(let i=0;i<4;i++){X.beginPath();X.moveTo(-70,50+i*32);X.lineTo(110-i%2*40,50+i*32);X.stroke();}X.restore();VIS.push('猫的说明书');}

// ================= 开场：说明书？→ 指着猫看 → 机器学习 =================
function hook(t){
 const out=eio(P(t,E('L03')+0.1,S('L04')+0.35));if(out>=1)return;
 X.save();X.globalAlpha=1-out;X.translate(0,-out*160);
 // L01 说明书 → 不会
 const bk=eo(P(t,S('L01')+0.1,S('L01')+0.6)),bkOut=eio(P(t,S('L02')-0.1,S('L02')+0.4));
 if(bkOut<1){X.save();X.globalAlpha*=1-bkOut;
  text('教小孩认猫',500,560+(1-bk)*20,56,INK,SERIF,'center',900,bk);
  book(500,860+(1-bk)*30,1,bk);
  cross(500,860,120,P(t,at('L01','？')+0.05,at('L01','？')+0.45));
  const no=eo(P(t,at('L01','？')+0.15,at('L01','？')+0.5));text('不会',500,1150,64,RED,SERIF,'center',900,no);
  X.restore();}
 // L02 一只一只猫：这是猫
 const kinds=['cat','cat','cat'],t0=S('L02')+0.3,tc=at('L02','：');
 if(t>=S('L02')-0.1&&t<E('L03')+0.5){
  const many=eio(P(t,at('L02','。')+0.1,at('L02','，')+0.3)),up=eio(P(t,S('L03')-0.1,S('L03')+0.5));
  X.save();X.globalAlpha*=1-up;X.translate(0,-up*150);
  kinds.forEach((k,i)=>{const e=spring(t-(t0+i*0.45));if(e<=0)return;const x=lerp(260+i*240,230+i*270,many);
   X.save();X.translate(x,760);X.scale(cl(e,0,1.1)*(1-many*0.18),cl(e,0,1.1)*(1-many*0.18));tile(0,0,200,k,t>=tc?'这是猫':'',true,cl(e*2));X.restore();});
  // 看多了：后面铺满小卡片
  if(many>0){for(let r=0;r<2;r++)for(let c=0;c<5;c++){const i=r*5+c,e=eo(cl(many*3-i*0.12));if(e<=0)continue;
   tile(180+c*160,990+r*140,120,i%4===3?'dog':'cat','',false,e*0.55);}
   const ok=eo(P(t,at('L02','，')+0.3,E('L02')));if(ok>0){mixed([['自己就',INK],['认得了',RED]],500,600,56,SERIF,900,ok);}}
  X.restore();}
 // L03 机器学习
 const big=eo(P(t,S('L03')+0.15,S('L03')+0.65));
 if(big>0){text('机器学习',500,840+(1-big)*30,150,RED,SERIF,'center',900,big);
  const k=eo(P(t,at('L03','，'),at('L03','，')+0.4));mixed([['让电脑',INK],['也这样学',RED]],500,960,56,SERIF,900,k,(1-k)*20);}
 X.restore();
}
