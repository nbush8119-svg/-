// ================= 方法标题 =================
function title(t){
 const a=S('L04'),i=eo(P(t,a,a+0.6)),o=eio(P(t,S('L05')-0.25,S('L05')+0.35));if(i<=0||o>=1)return;
 X.save();X.globalAlpha=i*(1-o);
 text('今天的方法',500,620+(1-i)*30,44,MUTE,SANS,'center',500);
 text('费曼学习法',500,790+(1-i)*30,130,INK,SERIF,'center',900);
 const f=eo(P(t,at('L04','，')+0.2,at('L04','，')+0.7));mixed([['四步，把',RED],['机器学习',RED],['讲透',RED]],500,930+(1-f)*24,56,SERIF,700,f);
 X.restore();
}
// ================= 四步进度条 =================
const STEPS=['一 选概念','二 讲给孩子','三 找卡点','四 简化'];
function tracker(t){
 const a0=at('L04','，')+0.1,enter=[0,0.35,0.7,1.05].map(d=>a0+d);
 let act=-1;if(t>=S('L05'))act=0;if(t>=S('L06'))act=1;if(t>=S('L13'))act=2;if(t>=S('L17'))act=3;if(t>=A.end)act=4;
 const xs=[175,385,595,805],y=292;
 for(let i=0;i<4;i++){const e=eo(P(t,enter[i],enter[i]+0.35))*(1-eio(P(t,A.end+0.3,A.end+0.9)));if(e<=0)continue;
  X.save();X.globalAlpha=e;X.translate(0,(1-e)*-30);
  const w=198,h=62;X.beginPath();X.roundRect(xs[i]-w/2,y-h/2,w,h,h/2);
  const done=i<act,on=i===act;
  if(on){X.fillStyle=RED;X.fill();}else{X.fillStyle=PAPER;X.fill();X.lineWidth=3;X.strokeStyle=done?INK:SOFT;X.stroke();}
  X.font=`700 28px ${SANS}`;X.textAlign='center';X.textBaseline='middle';X.fillStyle=on?CARD:(done?INK:MUTE);
  X.fillText(done?'✓'+STEPS[i].slice(1):STEPS[i],xs[i],y+2);X.restore();VIS.push(STEPS[i]);}
}
// ================= 费曼卡片 =================
function card(t){
 const s2=S('L05'),ci=eio(P(t,s2-0.15,s2+0.75)),co=eio(P(t,A.end,A.end+0.7));if(ci<=0||co>=1)return;
 const x0=lerp(320,130,ci),x1=lerp(680,870,ci),y0=lerp(720,380,ci)-co*220,y1=lerp(900,1205,ci)-co*220;
 X.save();X.globalAlpha=1-co;
 const z=1+0.035*eio(P(t,s2+1,S('L17')))-0.02*eio(P(t,S('L17'),S('L19')));X.translate(500,800);X.scale(z,z);X.translate(-500,-800);
 X.fillStyle='rgba(0,0,0,0.45)';X.beginPath();X.roundRect(x0+10,y0+14,x1-x0,y1-y0,22);X.fill();
 X.fillStyle=CARD;X.beginPath();X.roundRect(x0,y0,x1-x0,y1-y0,22);X.fill();X.lineWidth=3;X.strokeStyle=SOFT;X.stroke();
 if(ci<0.98){X.restore();return;}
 X.translate(0,-co*220);
 text('费曼卡片 No.05 · B7.2',170,440,30,MUTE,SANS,'left',500);
 text('作者自我认知',830,440,30,MUTE,SANS,'right',500);
 X.strokeStyle='#1E232B';X.lineWidth=2;for(let y=560;y<1190;y+=70){X.beginPath();X.moveTo(160,y);X.lineTo(840,y);X.stroke();}
 text('概念',170,512,36,INK,SANS,'left',700);
 X.strokeStyle=INK;X.lineWidth=3;X.beginPath();X.moveTo(160,535);X.lineTo(840,535);X.stroke();
 const wt=at('L05','：'),w=P(t,wt,wt+1.1);
 if(w>0){X.save();X.beginPath();X.rect(250,440,eo(w)*420,110);X.clip();mixed([['机器学习',RED]],445,522,70,SERIF,900);X.restore();}
 const hint=env(t,s2+0.6,wt);if(hint.a>0)text('↑ 写在最上方',540,512+hint.dy,34,MUTE,SANS,'left',500,hint.a);
 body(t);
 X.restore();
}
function label(t,a,b,segs,y=618,size=48){const e=env(t,a,b);if(e.a>0)mixed(segs,500,y,size,SERIF,700,e.a,e.dy);}
function person(x,y,s,col,alpha=1,arm=0){X.save();X.globalAlpha*=alpha;X.translate(x,y);X.scale(s,s);X.fillStyle=col;
 X.beginPath();X.arc(0,-70,48,0,Math.PI*2);X.fill();X.beginPath();X.roundRect(-60,-10,120,150,40);X.fill();
 X.strokeStyle=col;X.lineWidth=18;X.lineCap='round';
 X.beginPath();X.moveTo(-52,20);X.lineTo(-100,lerp(110,-30,arm));X.moveTo(52,20);X.lineTo(100,lerp(110,-30,arm));X.stroke();
 X.beginPath();X.moveTo(-28,130);X.lineTo(-36,230);X.moveTo(28,130);X.lineTo(36,230);X.stroke();X.restore();}
function cross(x,y,s,k,col=RED){if(k<=0)return;stroke([[x-s,y-s],[x+s,y+s]],eo(cl(k*2)),8,col);stroke([[x+s,y-s],[x-s,y+s]],eo(cl(k*2-1)),8,col);}
function check(x,y,s,k){stroke([[x-s,y],[x-s*0.3,y+s*0.7],[x+s,y-s*0.8]],k,9,RED);}
