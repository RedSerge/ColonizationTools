var f:file of byte;c,a,i,ux,uy,ub:byte;p,j,k:integer;
type bits=array [0..7] of byte;
var bs,bshrt:bits;mistakes:integer;fn:string;

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

type r = record
  x:byte;
  y:byte;
  b:byte;
end;
var z:array [0..254] of r;
begin
fn:='0';
if paramcount>0 then fn:=paramstr(1);
write('#',fn,': ');
fn:='colony0'+fn[1]+'.sav';
assign(f,fn);
reset(f);
seek(f,46);
read(f,c);
if c=0 then exit;
dec(c);
seek(f,44);
read(f,a);
if a=0 then exit;
dec(a);

for i:=0 to c do begin
  seek(f,390+202*i);
  read(f,z[i].x);
  read(f,z[i].y);
  seek(f,390+202*i+26);
  read(f,z[i].b);
end;

mistakes:=0;
p:=390+202*(c+1);
for i:=0 to a do begin
  seek(f,p+28*i);
  read(f,ux);
  read(f,uy);
  seek(f,p+28*i+3);
  read(f,ub);
  bit(ub,bs);
  for j:=0 to 7 do if j<4 then bshrt[j]:=0 else bshrt[j]:=bs[j];
  unbit(ub,bshrt);
  if (ub>=0) and (ub<=3) then begin
    for j:=0 to c do if (z[j].x=ux) and (z[j].y=uy) and (z[j].b<>ub) then begin
      ub:=z[j].b;
      bit(ub,bshrt);
      for k:=0 to 3 do bshrt[k]:=bs[k];
      unbit(ub,bshrt);
      seek(f,p+28*i+3);
      write(f,ub);
      inc(mistakes);
    end;
  end;
end;
close(f);
if mistakes=0 then writeln('File is correct.')
else writeln(mistakes,' mistake(s) corrected.');
end.