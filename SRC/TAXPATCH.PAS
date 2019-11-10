var a:array [1..9] of byte;f:file of byte;p,b:byte;c,x:shortint;fn:string;
var code:integer;t:file of longint;pos:longint;
begin
fn:='0';
if paramcount>0 then fn:=paramstr(1);
val(fn,x,code);
if code<>0 then begin
  writeln('Invalid argument.');
  exit;
end;
assign(t,'taxation.pos');
{$I-}
reset(t);
read(t,pos);
close(t);
{$I+}
code:=IOResult;
a[1]:=$7e;a[2]:=$19;a[3]:=$8a;a[4]:=$47;a[5]:=$01;
a[6]:=$8b;a[7]:=$c8;a[8]:=$98;a[9]:=$2d;
p:=1;
assign(f,'viceroy.exe');
reset(f);
if code=0 then seek(f,pos);
while not eof(f) do begin
  read(f,b);
  if a[p]=b then begin
    inc(p);
    if p>9 then begin
      b:=byte(x);
      write(f,b);
      pos:=filepos(f)-10;
      seek(f,pos-1);
      read(f,b);
      c:=shortint(b);
      seek(f,pos-1);
      b:=byte(x);
      write(f,b);
      writeln('Current taxes bound: ',c,' %');
      writeln('Updated taxes bound: ',x,' %');
      {$I-}
      if code<>0 then begin
        rewrite(t);
        write(t,pos);
        close(t);
      end;
      {$I+}
      break;
    end;
  end else p:=1;
end;
close(f);
end.