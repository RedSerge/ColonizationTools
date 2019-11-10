function bit(var b:byte;n:byte):byte;
begin
  bit:=(b shr (7-n)) and 1;
end;

var f:file of byte;c:byte;var fn:string;

begin
fn:='0';
if paramcount>0 then fn:=paramstr(1);
fn:='colony0'+fn[1]+'.sav';
assign(f,fn);
reset(f);
seek(f,18);
read(f,c);
if bit(c,3)=1 then if c mod 2=0 then inc(c) else dec(c);
seek(f,18);
write(f,c);
close(f);
write('#',fn,': ');
if c mod 2=0 then writeln('tory.') else writeln('rebel.');
end.