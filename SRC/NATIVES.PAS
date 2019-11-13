var a,c,t,i,j,d:byte;fn,fc,fd:string;f:file of byte;p:longint;code:integer;
begin
fn:='0';fc:='9';fd:='1';
if paramcount>0 then fn:=paramstr(1);
if paramcount>1 then fc:=paramstr(2);
if paramcount>2 then fd:=paramstr(3);
val(fc,j,code);
if code<>0 then j:=9;
val(fd,d,code);
if code<>0 then d:=1;
write('#',fn,': ');
fn:='colony0'+fn[1]+'.sav';
assign(f,fn);
reset(f);
seek(f,46);
read(f,c);
seek(f,44);
read(f,a);
seek(f,42);
read(f,t);
if t=0 then exit;
p:=$186+202*c+28*a+4*316+4;
a:=0;
for i:=1 to t do begin
  seek(f,p);
  read(f,c);
  if c<=d then begin
    seek(f,p);
    write(f,j);
    inc(a);
  end;
  p:=p+18;
end;
writeln(a,' tribe(s) enforced.');
close(f);
end.