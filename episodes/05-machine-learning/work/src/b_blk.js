function blk(s,x,y,col,alpha=1,size=56,fill=CARD,w0=0){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.font=`900 ${size}px ${SERIF}`;
 const w=Math.max(w0,X.measureText(s).width+size*0.9),h=size*1.7;X.beginPath();X.roundRect(x-w/2,y-h/2,w,h,16);
 X.fillStyle=fill;X.fill();X.lineWidth=4;X.strokeStyle=col;X.stroke();
 X.fillStyle=fill===CARD?col:CARD;X.textAlign='center';X.textBaseline='middle';X.fillText(s,x,y+3);X.restore();VIS.push(s);return w;}
function bubble(x,y,w,h,alpha,col=SOFT,tailLeft=true){if(alpha<=0)return;X.save();X.globalAlpha*=alpha;X.fillStyle=col;X.beginPath();X.roundRect(x-w/2,y-h/2,w,h,28);X.fill();
 X.beginPath();const tx=tailLeft?x-w/2+60:x+w/2-60;X.moveTo(tx-16,y+h/2-4);X.lineTo(tx+(tailLeft?-34:34),y+h/2+30);X.lineTo(tx+20,y+h/2-4);X.fill();X.restore();}
