var f:file of byte;
type bits=array [0..7] of byte;
var bs:bits;

const rebels:word = 80;

type wordrec = record
  lo, hi: byte;
end;

procedure bit(var b:byte;var somebits:bits);
var n:byte;
begin
  for n:=0 to 7 do somebits[n]:=(b shr (7-n)) and 1;
end;

procedure unbit(var b:byte;var somebits:bits);
var n:byte;base:byte;
begin
  base:=1;b:=0;
  for n:=7 downto 0 do begin
    if somebits[n]<>0 then b:=b+base;
    base:=base*2;
  end;
end;

var cities,units,player:byte;players:array [0..3] of integer;i:integer;
var pos:longint;b:byte;var wc:wordrec;w1,w2,wp:word;fn:string;

begin
fn:='0';
if paramcount>0 then fn:=paramstr(1);
write('#',fn,': ');
fn:='colony0'+fn[1]+'.sav';
assign(f,fn);
reset(f);
players[0]:=207;players[1]:=259;players[2]:=311;players[3]:=363;
for i:=3 downto -1 do begin
 if i<0 then begin
   writeln('No human player found.');
   exit;
 end;
 seek(f,players[i]);
 read(f,player);
 if player=0 then begin
   player:=i;
   break;
 end;
end;
seek(f,46);
read(f,cities);
if cities=0 then begin
  writeln('No colonies found.');
  exit;
end;
seek(f,44);
read(f,units);
pos:=$186;
wp:=0;
seek(f,pos+cities*202+units*28+player*316+9);
read(f,b);
bit(b,bs);
writeln('You request the independence from the Motherland.');
if bs[5]<>0 then writeln('(Simon Bolivar detected - be aware that his presence is not helpful).');
writeln;
dec(cities);
for i:=0 to cities do begin
  seek(f,pos+i*202+26);
  read(f,b);
  if b<>player then continue;
  seek(f,pos+i*202+31);
  read(f,b);
  seek(f,pos+i*202+194);
  read(f,wc.lo);
  read(f,wc.hi);
  w1:=word(wc);
  seek(f,pos+i*202+198);
  read(f,wc.lo);
  read(f,wc.hi);
  w2:=word(wc);
  b:=trunc(b*(w1/w2));
  wp:=wp+b;
end;
writeln(wp,' colonists strongly support the idea of the independence.');
if wp<rebels then
  writeln('You need at least ',rebels,' rebel colonists to request the independence.')
else begin
  b:=0;
  seek(f,$6a);
  for i:=1 to 4 do write(f,b);
  seek(f,$70);
  for i:=1 to 2 do write(f,b);
  writeln('Parliament supports your aspirations. You can declare the independence without');
  writeln('resistance right now - except for the Tories in your own colonies...');
end;
close(f);
end.